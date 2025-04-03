import os
import requests
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
CITY = os.getenv("CITY")
DB_CONN = {
    "host": os.getenv("POSTGRES_HOST"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": os.getenv("POSTGRES_PORT")
}

URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
#cd airflow-quickstart-learning/airflow-quickstart/learning-airflow




def fetch_weather():
    response = requests.get(URL)
    data = response.json()

    processed_data = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "timestamp": datetime.now().isoformat()
    }

    return processed_data


def save_to_db(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='fetch_weather')

    conn = psycopg2.connect(**DB_CONN)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            city TEXT,
            temperature FLOAT,
            humidity INT,
            weather TEXT,
            timestamp TIMESTAMP
        )
    """)

    cur.execute(
        "INSERT INTO weather (city, temperature, humidity, weather, timestamp) VALUES (%s, %s, %s, %s, %s)",
        (data["city"], data["temperature"], data["humidity"], data["weather"], data["timestamp"])
    )

    conn.commit()
    cur.close()
    conn.close()




with DAG(
        dag_id="weather_etl",
        schedule_interval="@hourly",
        start_date=datetime(2024, 1, 1),
        catchup=False
) as dag:
    fetch_task = PythonOperator(
        task_id="fetch_weather",
        python_callable=fetch_weather
    )

    save_task = PythonOperator(
        task_id="save_to_db",
        python_callable=save_to_db,
        provide_context=True
    )


    fetch_task >> save_task
