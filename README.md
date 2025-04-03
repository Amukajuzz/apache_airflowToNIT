# Weather ETL with Apache Airflow

## Overview
This project uses **Apache Airflow** to fetch weather data from the OpenWeather API and store it in a **PostgreSQL** database. The data includes temperature, humidity, weather description, and timestamp.

## Project Structure
```
weather-etl/
│── dags/               # Airflow DAGs (Python scripts defining workflows)
│── plugins/            # Custom plugins (if needed)
│── logs/               # Airflow logs
│── .env                # Environment variables (API keys, database credentials)
│── docker-compose.yaml # Docker configuration for Airflow and PostgreSQL
│── README.md           # Project documentation
```

## Prerequisites
Ensure you have the following installed:
- **Docker & Docker Compose**
- **Python 3.9+**
- **Apache Airflow 2.10.5**
- **PostgreSQL 16**

## Installation & Setup
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/weather-etl.git
cd weather-etl
```

### 2. Create & Configure `.env` File
Create a `.env` file and add your credentials:
```ini
POSTGRES_HOST=host.docker.internal
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432

API_KEY=your_openweathermap_api_key
CITY=Astana
```

### 3. Start the Project with Docker
Run the following command to start Airflow and PostgreSQL:
```bash
docker-compose up -d
```

### 4. Access the Airflow Web UI
Go to **http://localhost:8080** and log in:
- **Username**: admin
- **Password**: admin

Activate the `weather_etl` DAG to start fetching and storing weather data.

## DAG Workflow
1. **Fetch Weather Data**: Calls the OpenWeather API and retrieves weather data.
2. **Save to Database**: Stores the fetched data into PostgreSQL.
