# Predicting-in-Realtime


happiness scores across countries through a Multiple Regression Model and Kafka Streaming.

This project is designed to develop a regression machine learning model that predicts happiness scores in various countries based on data extracted from five distinct CSV files. The workflow covers the entire spectrum, encompassing Exploratory Data Analysis (EDA), Extract, Transform, Load (ETL) processes, model training, real-time streaming of transformed data using Kafka, and an evaluation of model performance.

The dataset utilized in this endeavor originates from Kaggle, presenting happiness information from diverse countries across different years. It comprises multiple variables contributing to the assessment of a country's happiness.

## Getting Started
To start using the project, follow these steps:

1.Clone the repository 
```bash
https://github.com/ImBetterThanYesterday/Predicting-in-Realtime.git
```

2. Make sure Docker is running and run the PostgreSQL container:
```bash
sudo docker run -d --name=postgres -p 5435:5432 -v postgres-volume:/var/lib/postgresql/data -e POSTGRES_PASSWORD=mysecretpass postgres
```

3. in your IDE install the following dependencies
```bash
 pip install -r requeriments.txt
```
## Setting up Kafka:

Run Docker Compose:
```bash
docker-compose up
```
Access Kafka Container:
```bash
docker exec -it kafka bash 
```
Create Kafka Topic:
```bash
kafka-topics --bootstrap-server kafka --create --topic kafka_final 
```

This command sets up a Kafka topic that will be used for streaming happiness data.

Running the Strem:

Open two new terminals and run the following command in each terminal:
```bash
python kafka_producer.py
```
```bash
python kafka_consumer.py
```
If you want to read the results from the Database, you can run:
```bash
python read_Predict_Database.py
```

