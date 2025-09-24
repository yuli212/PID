"""
ELT IoT Pipeline: Extract/Load raw data, Transform in SQL
This pipeline demonstrates the ELT pattern where raw data is loaded first,
then transformation happens in the data warehouse using SQL.
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

def load_sensors_to_staging(**context):
    """
    Load raw sensors data directly to staging table
    """
    print("🔄 Loading sensors data to staging...")
    
    # Read CSV file
    sensors_path = os.path.join(DATA_DIR, "sensors.csv")
    sensors_df = pd.read_csv(sensors_path)
    
    print(f"📊 Loading {len(sensors_df)} sensor records")
    
    # Get PostgreSQL connection and load data
    postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    engine = postgres_hook.get_sqlalchemy_engine()
    
    # Load raw data to staging table
    sensors_df.to_sql(
        'raw_sensors', 
        engine, 
        if_exists='replace', 
        index=False,
        method='multi'
    )
    
    print("✅ Sensors data loaded to raw_sensors staging table!")

def load_readings_to_staging(**context):
    """
    Load raw readings data directly to staging table
    """
    print("🔄 Loading readings data to staging...")
    
    # Read CSV file
    readings_path = os.path.join(DATA_DIR, "readings.csv")
    readings_df = pd.read_csv(readings_path)
    
    print(f"📊 Loading {len(readings_df)} reading records")
    
    # Get PostgreSQL connection and load data
    postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    engine = postgres_hook.get_sqlalchemy_engine()
    
    # Load raw data to staging table
    readings_df.to_sql(
        'raw_readings', 
        engine, 
        if_exists='replace', 
        index=False,
        method='multi'
    )
    
    print("✅ Readings data loaded to raw_readings staging table!")

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
    dag_id='elt_iot_pipeline',
    default_args=default_args,
    description='IoT ELT Pipeline - Transform in Database',
    schedule_interval=None,  # Manual trigger
    catchup=False,
    tags=['iot', 'elt', 'demo'],
) as dag:

    # Create staging tables
    create_staging_tables = PostgresOperator(
        task_id='create_staging_tables',
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="""
        -- Drop existing staging tables
        DROP TABLE IF EXISTS raw_sensors CASCADE;
        DROP TABLE IF EXISTS raw_readings CASCADE;
        
        -- Create sensors staging table
        CREATE TABLE raw_sensors (
            sensor_id INTEGER,
            location VARCHAR(100)
        );
        
        -- Create readings staging table  
        CREATE TABLE raw_readings (
            reading_id INTEGER,
            sensor_id INTEGER,
            temperature DECIMAL(5,2),
            timestamp TIMESTAMP
        );
        """,
    )

    # Load tasks - Extract and Load in one step
    load_sensors_task = PythonOperator(
        task_id='load_sensors',
        python_callable=load_sensors_to_staging,
        provide_context=True,
    )

    load_readings_task = PythonOperator(
        task_id='load_readings',
        python_callable=load_readings_to_staging,
        provide_context=True,
    )

    # Transform in SQL - This is where ELT differs from ETL
    transform_in_sql = PostgresOperator(
        task_id='transform_in_sql',
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="""
        -- Drop existing summary table
        DROP TABLE IF EXISTS daily_sensor_summary_elt;
        
        -- Create and populate summary table using SQL transformation
        CREATE TABLE daily_sensor_summary_elt AS
        WITH daily_stats AS (
            SELECT
                s.location,
                DATE(r.timestamp) AS date,
                AVG(r.temperature) AS avg_temp,
                MIN(r.temperature) AS min_temp,
                MAX(r.temperature) AS max_temp,
                COUNT(r.temperature) AS reading_count
            FROM raw_readings r
            INNER JOIN raw_sensors s ON r.sensor_id = s.sensor_id
            WHERE r.temperature IS NOT NULL
            GROUP BY s.location, DATE(r.timestamp)
        )
        SELECT
            location,
            date,
            ROUND(avg_temp, 2) AS avg_temp,
            ROUND(min_temp, 2) AS min_temp,
            ROUND(max_temp, 2) AS max_temp,
            reading_count,
            CURRENT_TIMESTAMP AS created_at
        FROM daily_stats
        ORDER BY location, date;
        
        -- Add indexes for better performance
        CREATE INDEX idx_daily_summary_elt_location ON daily_sensor_summary_elt(location);
        CREATE INDEX idx_daily_summary_elt_date ON daily_sensor_summary_elt(date);
        """,
    )

    # Data quality checks
    quality_checks = PostgresOperator(
        task_id='data_quality_checks',
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="""
        -- Check for data completeness
        DO $$
        DECLARE
            staging_sensors_count INTEGER;
            staging_readings_count INTEGER;
            summary_count INTEGER;
        BEGIN
            SELECT COUNT(*) INTO staging_sensors_count FROM raw_sensors;
            SELECT COUNT(*) INTO staging_readings_count FROM raw_readings;
            SELECT COUNT(*) INTO summary_count FROM daily_sensor_summary_elt;
            
            RAISE NOTICE 'Data Quality Report:';
            RAISE NOTICE '- Raw sensors: % records', staging_sensors_count;
            RAISE NOTICE '- Raw readings: % records', staging_readings_count;
            RAISE NOTICE '- Daily summaries: % records', summary_count;
            
            -- Basic validation
            IF staging_sensors_count = 0 THEN
                RAISE EXCEPTION 'No sensor data found in staging';
            END IF;
            
            IF staging_readings_count = 0 THEN
                RAISE EXCEPTION 'No readings data found in staging';
            END IF;
            
            IF summary_count = 0 THEN
                RAISE EXCEPTION 'No summary data generated';
            END IF;
            
            RAISE NOTICE 'All data quality checks passed!';
        END $$;
        """,
    )

    # Verify final results
    verify_results = PostgresOperator(
        task_id='verify_elt_results',
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="""
        SELECT 
            'ELT Pipeline Results' as pipeline,
            COUNT(*) as total_records,
            COUNT(DISTINCT location) as locations,
            COUNT(DISTINCT date) as dates,
            ROUND(AVG(avg_temp), 2) as overall_avg_temp,
            MIN(date) as earliest_date,
            MAX(date) as latest_date
        FROM daily_sensor_summary_elt;
        """,
        autocommit=True,
    )

    # Task dependencies
    create_staging_tables >> [load_sensors_task, load_readings_task] >> transform_in_sql >> quality_checks >> verify_results