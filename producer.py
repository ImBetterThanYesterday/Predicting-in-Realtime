import pandas as pd
import numpy as np
#import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt
import json
from json import dumps, loads
#from sqlalchemy import create_engine
from time import sleep
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import joblib
from kafka import KafkaProducer, KafkaConsumer

# from kafka import KafkaProducer, KafkaConsumer
# #from confluent_kafka import Producer
# from json import dumps, loads
# import pandas as pd
# import json 
# from time import sleep

## Reading Datasetss
df_data_2015 = pd.read_csv('data/2015.csv')
df_data_2016 = pd.read_csv('data/2016.csv')
df_data_2017 = pd.read_csv('data/2017.csv')
df_data_2018 = pd.read_csv('data/2018.csv')
df_data_2019 = pd.read_csv('data/2019.csv')

## Append thecolumns 
archivos = ["Data/2015.csv","Data/2016.csv","Data/2017.csv","Data/2018.csv","Data/2019.csv"]

dataframes = []
position=0
for archivo in archivos:
    anio = archivo.split("/")[-1].split(".")[0]
    df = pd.read_csv(archivo)
    df['anio']=anio
    
    print(anio)
     # Eliminar columnas no deseadas
    columns_to_drop = [
        "Region",
        "Standard Error",
        "Lower Confidence Interval",
        "Upper Confidence Interval",
        "Dystopia Residual",
        "Whisker.high",
        "Whisker.low",
        "Dystopia.Residual"
    ]
    df = df.drop(columns=columns_to_drop, errors='ignore')
    position+=1


    df = df.rename(columns={
        'Happiness.Rank': 'Happiness Rank',
        'Overall rank': 'Happiness Rank',
        'Country or region': 'Country',
        'Score': 'score',
        'Happiness Score': 'score',
        'Happiness.Score': 'score',
        'Economy (GDP per Capita)': 'gdp',
        'GDP per capita': 'gdp',
        'Economy..GDP.per.Capita.': 'gdp',
        'Family': 'Social support',
        'Healthy life expectancy' : 'healthy_life_expectancy',
        'Health (Life Expectancy)': 'healthy_life_expectancy',
        'Health..Life.Expectancy.': 'healthy_life_expectancy',
        'Freedom to make life choices': 'freedom',
        'Freedom': 'freedom',
        'Generosity': 'generosity',
        'Perceptions of corruption': 'corruption',
        'Trust (Government Corruption)': 'corruption',
        'Trust..Government.Corruption.': 'corruption'
    })
    dataframes.append(df)

df = pd.concat(dataframes, ignore_index=True)


## Borrando el dato nulo 
df=df.dropna()
print(df)
# Seleccionar las características relevantes 'gdp', 'social_support', 'healthy_life_expectancy', 'freedom', 'corruption', y 'generosity' son características relevantes.
#gpd,Social support,healthy_life_expectancy,freedom,corruption(probablemente)
features = ['gdp', 'Social support', 'healthy_life_expectancy', 'freedom']
#### Hay que arreglar Social support por social_support

X = df[features]
y = df['score']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=30)

# Inicializar el modelo de regresión lineal
model = LinearRegression()

# Entrenar el modelo
model.fit(X_train, y_train)


# Unir X_test y y_test en un solo DataFrame
test_data = pd.concat([X_test, y_test], axis=1)
print(test_data)

def kafka_producerrr(test_data):
    ### Conexion
    producer = KafkaProducer(
                value_serializer = lambda m: dumps(m).encode('utf-8'),
                bootstrap_servers = ['localhost:9092'],
            )
    limit=30
    indexx=0
    # Iterar a través de las filas del DataFrame y convertirlas en objetos JSON
    json_objects = []
    for index, row in test_data.iterrows():
        row_dict = row.to_dict()
        #print(type(row_dict))
        producer.send("kafka_final", value=row_dict)
        print("Message sent:", row_dict)
        #sleep(1)  

kafka_producerrr(test_data)

