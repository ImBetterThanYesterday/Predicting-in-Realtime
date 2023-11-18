# Predicting-in-Realtime


happiness scores across countries through a Multiple Regression Model and Kafka Streaming.

This project is designed to develop a regression machine learning model that predicts happiness scores in various countries based on data extracted from five distinct CSV files. The workflow covers the entire spectrum, encompassing Exploratory Data Analysis (EDA), Extract, Transform, Load (ETL) processes, model training, real-time streaming of transformed data using Kafka, and an evaluation of model performance.

The dataset utilized in this endeavor originates from Kaggle, presenting happiness information from diverse countries across different years. It comprises multiple variables contributing to the assessment of a country's happiness.

Getting Started
To start using the project, follow these steps:

Clone the Repository:

Clone the project repository in your development environment.
Install the Required Libraries:

Install the necessary libraries listed in the requirements.txt file. You can do this using a package manager like pip in Python. Run the following command:

```bash
pip install -r requirements.txt
```

Setup the PostgreSQL Database Connection:


}
Setting up Kafka:

Run Docker Compose:

docker-compose up
Access Kafka Container:

docker exec -it kafka bash 
Create Kafka Topic:

Inside the Kafka container, run the following command to create a Kafka topic named kafka-happiness:

kafka-topics --bootstrap-server kafka --create --topic kafka-happiness 
This command sets up a Kafka topic that will be used for streaming happiness data.

Running the Strem:

Open two new terminals and run the following command in each terminal:

python kafka_consumer.py
python kafka_producer.py
