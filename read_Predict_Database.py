import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import psycopg2

def fetch_data_from_db():
    # Configura la conexión a la base de datos PostgreSQL
    connection = psycopg2.connect(
        host="localhost",
        port="5435",
        database="postgres",
        user="postgres",
        password="mysecretpass"
    )

    # Crea un cursor para ejecutar consultas
    cursor = connection.cursor()

    # Realiza una consulta SQL para obtener todos los datos de la tabla
    query = "SELECT * FROM prediction_table"
    cursor.execute(query)

    # Obtén todos los resultados como una lista de tuplas
    data = cursor.fetchall()

    # Obtén los nombres de las columnas
    column_names = [desc[0] for desc in cursor.description]

    # Crea un DataFrame de pandas con los datos y nombres de columnas
    df = pd.DataFrame(data, columns=column_names)

    # Cierra el cursor y la conexión a la base de datos
    cursor.close()
    connection.close()

    return df

# Llama a la función para obtener los datos desde la base de datos
datos_desde_db = fetch_data_from_db()
datos_desde_db = datos_desde_db.drop_duplicates()
print(datos_desde_db)

# Supongamos que 'y_true' son los valores reales y 'y_pred' son las predicciones
y_true = datos_desde_db['score']
y_pred = datos_desde_db['prediction']

# Calcula las métricas de rendimiento
mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
rmse = mean_squared_error(y_true, y_pred, squared=False)  # Calcula la raíz cuadrada del MSE
r_squared = r2_score(y_true, y_pred)

# Imprime las métricas
print(f'Mean Absolute Error (MAE): {mae}')
print(f'Mean Squared Error (MSE): {mse}')
print(f'Root Mean Squared Error (RMSE): {rmse}')
print(f'R-squared: {r_squared}')

