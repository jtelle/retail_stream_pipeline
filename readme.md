

## Retail Streaming Pipeline PoC
This project is a Proof of Concept (PoC) for a real‑time retail data pipeline. It uses a decoupled architecture for ingestion, processing, persistence, and monitoring of sales transactions.

### System Architecture
The data flow follows the structure below:

- Ingestion: A Producer simulates sales transactions and sends them to an Apache Kafka topic.

- Streaming: A Python Consumer processes messages in real time.

- SQL Persistence: Processed data is efficiently stored in a SQLite database using micro‑batching techniques.

- Observability & MLflow: Business metrics and a demand‑forecasting logic are tracked through MLflow Tracking.

### Technologies Used
- Apache Kafka: Messaging broker for data streaming.

- Python 3.x: Main language for Producer and Consumer logic.

- SQLite: Relational database engine for historical persistence.

- MLflow: Platform for ML lifecycle management and metric monitoring.

- Docker & Docker Compose: Infrastructure service orchestration.

- Pandas: Used for validation and visualization of structured data.

### Key Features
1. SQL Micro‑Batching
To optimize I/O performance, the Consumer does not commit after every received message. Instead, it implements a buffer that groups 30 transactions before persisting them into the retail_history.db database. This ensures system scalability under higher data volumes.

2. Demand Forecasting Logic
The pipeline includes a symbolic inference layer that detects key products (such as MILK or YOGURT) and computes an estimate of future demand (based on a 10% increase). This metric is automatically logged in MLflow.

3. Real‑Time Monitoring
Through the MLflow interface, it is possible to visualize:

- The total value of each processed sale.

- The historical record of demand predictions.

- Parameters of the products flowing through the pipeline.


### System Architecture
The data flow follows the structure below:

1. Ingestion: A Producer simulates sales transactions and sends them to an Apache Kafka topic.

2. Streaming: A Python Consumer processes the messages in real time.

3. SQL Persistence: The processed data is efficiently stored in a SQLite database using micro‑batching techniques.

4. Observability & MLflow: Business metrics and a demand‑forecasting logic are tracked through MLflow Tracking.

### Technologies Used
- Apache Kafka: Messaging broker for data streaming.

- Python 3.x: Main language for the Producer and Consumer logic.

- SQLite: Relational database engine for historical persistence.

- MLflow: Platform for ML lifecycle management and metric monitoring.

- Docker & Docker Compose: Orchestration of infrastructure services.

- Pandas: Used for validation and visualization of structured data.

### Key Features
1. SQL Micro‑Batching
To optimize I/O performance, the Consumer does not commit after every received message. Instead, it implements a buffer that groups 30 transactions before persisting them into the retail_history.db database. This ensures the system remains scalable under higher data volumes.

2. Demand Forecasting Logic
The pipeline includes a symbolic inference layer that detects key products (such as MILK or YOGURT) and computes an estimate of future demand (based on a 10% increase). This metric is automatically logged in MLflow.

3. Real‑Time Monitoring
    Through the MLflow interface, it is possible to visualize:

    The total value of each processed sale.

    The historical record of demand predictions.

    Parameters of the products flowing through the pipeline.

### Usage Instructions
1. Start the Infrastructure:

```bash
docker-compose up -d
```
Run the Pipeline:

Start the data generator:

```bash
python producer.py
```
Start the processor:

```bash
python consumer.py
```
2. Verify Data:  
 - Run the SQL audit script to inspect the latest stored records:

```bash
python check_db.py
```
3. Access MLflow:  

Open http://localhost:5000 in your browser to view the metrics and experiment dashboard.

### Roadmap / Future Improvements
- Scalability: Migrate from SQLite to PostgreSQL for multi‑user support and distributed environments.

- ML Models: Replace the heuristic logic with advanced predictive models (Prophet/XGBoost) served through MLflow.

- Visualization: Integrate Grafana for real‑time business and infrastructure dashboards.

### Recommended Shutdown Order:
- Producer terminal: Ctrl + C.
  (Stop the data faucet first.)

- Consumer terminal: Ctrl + C.
  (Allow it to process remaining messages and close the connection.)

- MLflow / Docker terminal:
  - docker-compose down

