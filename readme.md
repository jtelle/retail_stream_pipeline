### Crear el entorno (usualmente llamado 'venv' o '.venv')
python -m venv [nombre-del-entorno]

### Activarlo
#### En Windows:
venv\Scripts\activate
#### En Mac/Linux:
source venv/bin/activate

### Retail Real-Time Streaming Pipeline

Este proyecto implementa un pipeline de datos en tiempo real diseñado para la ingesta, procesamiento y monitoreo de transacciones de retail. Utiliza una arquitectura moderna desacoplada basada en microservicios y contenedores.

### Arquitectura del Sistema

El flujo de datos se compone de tres capas principales:
1. **Ingesta (Producer):** Un simulador de ventas en Python que genera eventos JSON y los envía a un broker de mensajería.
2. **Transporte (Apache Kafka):** Actúa como el motor de mensajería (modo KRaft) para garantizar la entrega de datos de forma asíncrona.
3. **Procesamiento y Observabilidad (Consumer + MLflow):** Un script que transforma los datos al vuelo y registra métricas de negocio en un servidor de MLflow.



### Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Infraestructura:** Docker & Docker Compose
* **Streaming:** Apache Kafka (KRaft mode)
* **Tracking/MLOps:** MLflow
* **Librerías:** `kafka-python-ng`, `pandas`, `mlflow`

### Ejecución del Proyecto

### 1. Levantar la Infraestructura
Asegúrate de tener Docker instalado y ejecuta:
```bash
docker compose up -d
```
### 2. Configurar el Entorno Python
```bash
python -m venv retail-stream-env
source retail-stream-env/bin/activate  # En Windows: .\retail-stream-env\Scripts\activate
pip install kafka-python-ng pandas mlflow
```
### 3. Iniciar el Pipeline
Abre dos terminales y ejecuta en orden:

Consumer: python consumer.py

Producer: python producer_super_sim.py

### 4. Visualización
Accede a la interfaz de MLflow en http://localhost:5000 para ver las métricas de las ventas procesadas en tiempo real.

### Características Destacadas

- Desacoplamiento: El sistema es resistente a caídas de los consumidores gracias al buffering de Kafka.

- Limpieza de datos y cálculo de totales antes del almacenamiento.

- Registro sistemático de cada transacción para auditoría y análisis posterior

## 🌟 PoC Highlights: SQL & Predictive Analytics
Esta PoC simula un entorno de producción real:
* **Persistencia SQL:** Cada mensaje de Kafka se inserta en una base de datos SQLite (`retail_history.db`) para análisis histórico.
* **Previsión de Demanda:** Implementa una lógica de inferencia que calcula la demanda futura estimada, registrando las predicciones en MLflow para monitorear el rendimiento del modelo.

Future Roadmap
1. **Cloud Integration:** Migrate the SQLite sink to a managed PostgreSQL instance (RDS/Cloud SQL).
2. **Advanced ML:** Replace the heuristic forecasting with a trained Prophet or XGBoost model served via MLflow Models.
3. **Dashboarding:** Connect Grafana or Power BI to the SQL database for real-time business intelligence.
4. **Containerization:** Orchestrate the entire pipeline using Kubernetes (K8s) for high availability.