import mlflow
import mlflow.pyfunc
from kafka import KafkaConsumer
import json

import sqlite3

# Configuración de SQL local


def init_db():
    # Añadimos timeout=30 para que espere hasta 30 segundos si la DB está ocupada
    conn = sqlite3.connect('retail_history.db', timeout=30)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT,
            cantidad INTEGER,
            total REAL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn


db_conn = init_db()

consumer = KafkaConsumer(
    'retail_topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Retail_Streaming_Analysis")
contador_batch = 0
print("👂 Escuchando ventas en tiempo real...")

for mensaje in consumer:
    venta = mensaje.value
    # Lógica de Ingeniería: Limpieza básica
    producto = venta['producto'].upper()
    total = venta['cantidad'] * venta['precio']

    print(f"PROCESANDO: {producto} | Total: {total}€")

    # 1. Preparar la inserción (Sin commit aún)
    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO ventas (producto, cantidad, total) VALUES (?, ?, ?)",
                   (producto, venta['cantidad'], total))

    contador_batch += 1  # Aumentamos el contador

    # 2. PoC de Previsión de Demanda (Lógica de Negocio)
    demanda_predicha = None
    if producto == 'LECHE':  # O YOGUR, según tu lista
        # Simulamos que el modelo ML predice que mañana venderás un 10% más
        demanda_predicha = venta['cantidad'] * 1.10
        print(
            f"PREVISIÓN: Mañana se esperan {demanda_predicha:.2f} unidades de {producto}")

    # 3. Registro en MLflow
    with mlflow.start_run(nested=True):
        mlflow.log_param("producto", producto)
        mlflow.log_metric("venta_total", total)
        if demanda_predicha:
            mlflow.log_metric("demanda_futura_estimada", demanda_predicha)

    print(f"PROCESADO Y GUARDADO EN SQL: {producto} | Total: {total}€")

    # 4. Commit solo cada 30 mensajes
    if contador_batch >= 30:
        db_conn.commit()
        print(f"BATCH COMPLETADO: 30 registros guardados en SQL.")
        contador_batch = 0  # Reiniciamos el contador
    else:
        print(f"Mensaje en buffer ({contador_batch}/30): {producto}")
