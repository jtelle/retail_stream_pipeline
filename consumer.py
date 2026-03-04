import mlflow
import mlflow.pyfunc
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'retail_topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Retail_Streaming_Analysis")
print("👂 Escuchando ventas en tiempo real...")

for mensaje in consumer:
    venta = mensaje.value
    # Lógica de Ingeniería: Limpieza básica
    producto = venta['producto'].upper()
    total = venta['cantidad'] * venta['precio']

    print(f"🛒 PROCESANDO: {producto} | Total: {total}€")

    # --- AQUÍ ENVIAMOS A MLFLOW ---
    with mlflow.start_run():
        mlflow.log_param("producto", producto)
        mlflow.log_metric("venta_total", total)
        mlflow.log_metric("cantidad", venta['cantidad'])

    # 1. Guardar en un archivo Parquet.
