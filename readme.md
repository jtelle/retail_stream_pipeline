### Crear el entorno (usualmente llamado 'venv' o '.venv')
python -m venv [nombre-del-entorno]

### Activarlo
#### En Windows:
venv\Scripts\activate
#### En Mac/Linux:
source venv/bin/activate

## Retail Streaming Pipeline PoC

Este proyecto es una Prueba de Concepto (PoC) de un pipeline de datos de retail en tiempo real. Utiliza una arquitectura desacoplada para la ingesta, procesamiento, persistencia y monitorización de transacciones de ventas.

### Arquitectura del Sistema

El flujo de datos sigue el siguiente esquema:

1. **Ingesta:** Un Producer simula transacciones de ventas y las envía a un tópico de Apache Kafka.
2. **Streaming:** Un Consumer en Python procesa los mensajes en tiempo real.
3. **Persistencia SQL:** Los datos procesados se almacenan de forma eficiente en una base de datos SQLite mediante técnicas de micro-batching.
4. **Observabilidad & MLflow:** Se realiza un seguimiento de métricas de negocio y una lógica de previsión de demanda integrada con MLflow Tracking.

### Tecnologías Utilizadas

* **Apache Kafka:** Broker de mensajería para el streaming de datos.
* **Python 3.x:** Lenguaje principal para la lógica del Producer y Consumer.
* **SQLite:** Motor de base de datos relacional para la persistencia histórica.
* **MLflow:** Plataforma para la gestión del ciclo de vida de ML y monitorización de métricas.
* **Docker & Docker Compose:** Orquestación de los servicios de infraestructura.
* **Pandas:** Utilizado para la validación y visualización de datos estructurados.

### Características Principales

#### 1. Micro-Batching en SQL
Para optimizar el rendimiento de I/O, el Consumer no realiza un commit por cada mensaje recibido. En su lugar, implementa un buffer que agrupa **30 transacciones** antes de persistirlas en la base de datos `retail_history.db`. Esto asegura la escalabilidad del sistema ante mayores volúmenes de datos.

#### 2. Lógica de Previsión de Demanda
El pipeline incluye una capa de inferencia simbólica que detecta productos clave (como LECHE o YOGUR) y calcula una estimación de demanda futura (basada en un incremento del 10%). Esta métrica se registra automáticamente en MLflow.

#### 3. Monitorización en Tiempo Real
A través de la interfaz de MLflow, es posible visualizar:
* El valor total de cada venta procesada.
* El histórico de predicciones de demanda.
* Parámetros de los productos que fluyen por el pipeline.

### Instrucciones de Uso

1. **Levantar Infraestructura:**
   ```bash
   docker-compose up -d
   ```
2. **Ejecutar el Pipeline:**

    - Iniciar el generador de datos:
   ```bash
   python producer.py
   ```

    - Iniciar el procesador:
   ```bash
   python consumer.py
   ```

3. **Verificar Datos:**
Ejecutar el script de auditoría SQL para ver los últimos registros guardados:

    ```bash
    python check_db.py
    ```
4. Acceder a MLflow:
Abrir http://localhost:5000 en el navegador para ver el panel de control de métricas y experimentos.

### Roadmap / Futuras Mejoras
- Escalabilidad: Migración de SQLite a PostgreSQL para soporte multi-usuario y entornos distribuidos.

- Modelos ML: Sustitución de la lógica heurística por modelos predictivos avanzados (Prophet/XGBoost) servidos desde MLflow.

- Visualización: Integración con Grafana para dashboards de negocio e infraestructura en tiempo real.
