"""
ETL IoT Pipeline: Extract, Transform (in pandas), Load to DWH
This pipeline demonstrates the ETL pattern where transformation happens 
in memory using pandas before loading to the data warehouse.
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
import os

# Configuration
DATA_DIR = "/opt/airflow/data"
POSTGRES_CONN_ID = "postgres_default"

def extract_data(**context):
    """
    Extract data from CSV files into pandas DataFrames
    """
    print("🔄 Starting data extraction...")
    
    # Read sensors data
    sensors_path = os.path.join(DATA_DIR, "sensors.csv")
    sensors_df = pd.read_csv(sensors_path)
    print(f"📊 Extracted {len(sensors_df)} sensor records")
    
    # Read readings data with timestamp parsing
    readings_path = os.path.join(DATA_DIR, "readings.csv")
    readings_df = pd.read_csv(readings_path)
    readings_df['timestamp'] = pd.to_datetime(readings_df['timestamp'])
    print(f"📊 Extracted {len(readings_df)} reading records")
    
    # Store in XCom for next task
    context['ti'].xcom_push(key='sensors', value=sensors_df.to_json(date_format='iso'))
    context['ti'].xcom_push(key='readings', value=readings_df.to_json(date_format='iso'))
    
    print("✅ Data extraction completed!")

def transform_data(**context):
    """
    Transform data using pandas - join, group, and aggregate
    """
    print("🔄 Starting data transformation...")
    
    # Get data from XCom
    sensors_json = context['ti'].xcom_pull(key='sensors')
    readings_json = context['ti'].xcom_pull(key='readings')
    
    sensors_df = pd.read_json(sensors_json)
    readings_df = pd.read_json(readings_json)
    
    print(f"📊 Processing {len(sensors_df)} sensors and {len(readings_df)} readings")
    
    # Join sensors and readings
    merged_df = readings_df.merge(sensors_df, on='sensor_id', how='inner')
    print(f"📊 Joined data: {len(merged_df)} records")
    
    # Add date column for grouping
    merged_df['date'] = merged_df['timestamp'].dt.date
    
    # Group by location and date, calculate aggregates
    summary_df = (
        merged_df.groupby(['location', 'date'])['temperature']
        .agg(['mean', 'min', 'max', 'count'])
        .reset_index()
        .rename(columns={
            'mean': 'avg_temp', 
            'min': 'min_temp', 
            'max': 'max_temp',
            'count': 'reading_count'
        })
    )
    
    # Round temperature values
    summary_df['avg_temp'] = summary_df['avg_temp'].round(2)
    summary_df['min_temp'] = summary_df['min_temp'].round(2)
    summary_df['max_temp'] = summary_df['max_temp'].round(2)
    
    print(f"📊 Transformed to {len(summary_df)} daily summaries")
    print("📋 Sample of transformed data:")
    print(summary_df.head())
    
    # Store transformed data in XCom
    context['ti'].xcom_push(key='summary', value=summary_df.to_json(date_format='iso'))
    
    print("✅ Data transformation completed!")

def load_data(**context):
    """
    Load transformed data into PostgreSQL data warehouse
    """
    print("🔄 Starting data loading...")
    
    # Get transformed data from XCom
    summary_json = context['ti'].xcom_pull(key='summary')
    summary_df = pd.read_json(summary_json)
    
    print(f"📊 Loading {len(summary_df)} records to data warehouse")
    
    # Get PostgreSQL connection
    postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    engine = postgres_hook.get_sqlalchemy_engine()
    
    # Load data to PostgreSQL
    summary_df.to_sql(
        'daily_sensor_summary_etl', 
        engine, 
        if_exists='replace', 
        index=False,
        method='multi'
    )
    
    print("✅ Data loading completed!")
    print(f"📋 Loaded to table: daily_sensor_summary_etl")

# Default arguments
default_args = {
    'owner': 'data-engineer',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 24),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
with DAG(
    dag_id='etl_iot_pipeline',
    default_args=default_args,
    description='IoT ETL Pipeline - Transform in Memory',
    schedule_interval=None,  # Manual trigger
    catchup=False,
    tags=['iot', 'etl', 'demo'],
) as dag:

    # Create target table
    create_table = PostgresOperator(
        task_id='create_etl_table',
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="""
        DROP TABLE IF EXISTS daily_sensor_summary_etl;
        CREATE TABLE daily_sensor_summary_etl (
            location VARCHAR(100),
            date DATE,
            avg_temp DECIMAL(5,2),
            min_temp DECIMAL(5,2),
            max_temp DECIMAL(5,2),
            reading_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
    )

    # ETL Tasks
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
        provide_context=True,
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load_data,
        provide_context=True,
    )

    # Verify data
    verify_data = PostgresOperator(
        task_id='verify_etl_data',
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="""
        SELECT 
            'ETL Pipeline Results' as pipeline,
            COUNT(*) as total_records,
            COUNT(DISTINCT location) as locations,
            COUNT(DISTINCT date) as dates,
            ROUND(AVG(avg_temp), 2) as overall_avg_temp
        FROM daily_sensor_summary_etl;
        """,
        autocommit=True,
    )

    # Task dependencies
    create_table >> extract_task >> transform_task >> load_task >> verify_data