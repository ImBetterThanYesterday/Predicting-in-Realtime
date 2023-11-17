import pandas as pd
from kafka import KafkaConsumer
from json import  loads
import os
import joblib
import psycopg2

def create_table():
    # Conexión a la base de datos PostgreSQL
    connection = psycopg2.connect(
                host="localhost",
                port = "5435",
                database="postgres",
                user="postgres",
                password="mysecretpass"
            )
    cursor = connection.cursor()

    # Creación de la tabla si no existe
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS prediction_table_final (
        gdp DOUBLE PRECISION,
        social_support DOUBLE PRECISION,
        healthy_life_expectancy DOUBLE PRECISION,
        freedom DOUBLE PRECISION,
        score DOUBLE PRECISION,
        prediction DOUBLE PRECISION
    );
    '''

    print("Creando la tabla...")
    cursor.execute(create_table_query)
    connection.commit()
    print("Tabla creada con éxito.")

    # Cierre de la conexión
    cursor.close()
    connection.close()

def kafka_consumer():
    consumer = KafkaConsumer(
        'kafka_final',
        enable_auto_commit=True,
        group_id='my-group-1',
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['localhost:9092']
    )

    try:
        # Obtiene la ruta del script actual
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Une la ruta del script con el nombre del archivo
        modelo_exportado = os.path.join(script_dir, "model_final.pkl")

        # Carga el modelo
        model = joblib.load(modelo_exportado)

        for m in consumer:
            # Normaliza los datos
            datos_test = pd.json_normalize(data=m.value)
            # Guarda la columna 'score' para después
            score_column = datos_test['score']
            # Elimina la columna 'score' de tus datos de prueba
            datos_test = datos_test.drop('score', axis=1)
            # Realiza predicciones
            predicciones = model.predict(datos_test)
            # Agrega la columna 'score' de nuevo a los datos
            datos_test['score'] = score_column
            # Agrega las predicciones a los datos originales
            datos_test['prediction'] = predicciones
            # Imprime los datos con las predicciones
            print(datos_test)

             # Conexión a la base de datos PostgreSQL
            connection = psycopg2.connect(
                host="localhost",
                port = "5435",
                database="postgres",
                user="postgres",
                password="mysecretpass"
            )
            cursor = connection.cursor()

            # Inserta los datos en la tabla
            print("Insertando datos en la tabla...")
            for index, row in datos_test.iterrows():
                cursor.execute(
                    "INSERT INTO prediction_table_final VALUES (%s, %s, %s, %s, %s, %s);",
                    (row['gdp'], row['Social support'], row['healthy_life_expectancy'],
                     row['freedom'], row['score'],row['prediction'])
                )

            connection.commit()
            print("Datos insertados con éxito.")


            # Cierre de la conexión
            cursor.close()
            connection.close()

    except FileNotFoundError:
        print(f"El archivo 'model_final.pkl' no se encontró en {script_dir}.")

if __name__ == "__main__":
    create_table()
    kafka_consumer()