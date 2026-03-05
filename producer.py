from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

productos = ['leche', 'pan', 'huevos', 'manzanas']

print("🚀 Caja registradora iniciada...")
while True:
    datos_venta = {
        'id_ticket': random.randint(1000, 9999),
        'producto': random.choice(productos),
        'cantidad': random.randint(1, 5),
        'precio': round(random.uniform(1.0, 10.0), 2)
    }

    # Enviamos el JSON al topic 'retail_topic'
    producer.send('retail_topic', datos_venta)
    producer.flush()
    print(f"Venta enviada: {datos_venta}")
    time.sleep(2)  # Envía una venta cada 2 segundos
