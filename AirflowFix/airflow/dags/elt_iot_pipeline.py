"""
ELT IoT Pipeline: Fully Optimized Version
This pipeline implements Incremental Loading, Data Partitioning, and Query Optimization.
"""
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
import os

# --- KONFIGURASI ---
DATA_DIR = "/opt/airflow/data"
POSTGRES_CONN_ID = "postgres_default"

# --- FUNGSI PYTHON (tidak berubah) ---
def load_sensors_to_staging(**context):
    """Load raw sensors data into a staging table."""
    print("🔄 Loading sensors data to staging...")
    sensors_path = os.path.join(DATA_DIR, "sensors.csv")
    sensors_df = pd.read_csv(sensors_path)
    postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    engine = postgres_hook.get_sqlalchemy_engine()
    sensors_df.to_sql('raw_sensors', engine, if_exists='append', index=False, method='multi')
    print("✅ Sensors data loaded!")

def load_readings_to_staging(**context):
    """Load raw readings data into a staging table."""
    print("🔄 Loading readings data to staging...")
    readings_path = os.path.join(DATA_DIR, "readings.csv")
    readings_df = pd.read_csv(readings_path)
    postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    engine = postgres_hook.get_sqlalchemy_engine()
    readings_df.to_sql('raw_readings', engine, if_exists='append', index=False, method='multi')
    print("✅ Readings data loaded!")

def load_weather_to_staging(**context):
    """Load raw weather data into a staging table."""
    print("🔄 Loading weather data to staging...")
    weather_path = os.path.join(DATA_DIR, "weather.csv")
    weather_df = pd.read_csv(weather_path)
    postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    engine = postgres_hook.get_sqlalchemy_engine()
    weather_df.to_sql('raw_weather', engine, if_exists='append', index=False, method='multi')
    print("✅ Weather data loaded!")

def check_for_anomalies(**context):
    """Check for anomalies and decide the next task to run."""
    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    # Memeriksa anomali hanya untuk data hari ini (sesuai incremental loading)
    records = hook.get_records("SELECT COUNT(*) FROM daily_sensor_summary_elt WHERE quality_flag = 'ABNORMAL' AND date = '{{ ds }}'")
    if records and records[0] and records[0][0] > 0:
        return 'send_alert_task'
    else:
        return 'no_alert_task'

def log_summary_metrics(**context):
    """Mencatat metrik penting dari tabel summary."""
    print(" Mencatat custom metrics dari daily_sensor_summary_elt...")
    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

    # Ambil jumlah baris, jumlah lokasi unik, dan rata-rata suhu
    stats = hook.get_first("""
        SELECT
            COUNT(*) AS processed_rows,
            COUNT(DISTINCT location) AS distinct_locations,
            AVG(avg_temp) AS overall_avg_temp
        FROM daily_sensor_summary_elt;
    """)

    processed_rows, distinct_locations, overall_avg_temp = stats

    # Cetak metrik ke log Airflow
    print("--- Custom Metrics ---")
    print(f"Total baris di summary: {processed_rows}")
    print(f"Jumlah lokasi unik: {distinct_locations}")
    print(f"Rata-rata suhu keseluruhan: {overall_avg_temp:.2f}")


default_args = {
    'owner': 'data-engineer',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 22), 
    'email_on_failure': False, 
    'email_on_retry': False,
    'email': ['waluyoajiub74@student.ub.ac.id'], 
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DEFINISI DAG 
with DAG(
    dag_id='elt_iot_pipeline',
    default_args=default_args,
    description='Fully Optimized ELT Pipeline',
    schedule_interval='@daily', 
    catchup=False,
    tags=['iot', 'elt', 'optimized'],
) as dag:

    create_staging_tables_task = PostgresOperator(
        task_id='create_staging_tables',
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="""
        CREATE TABLE IF NOT EXISTS raw_sensors (sensor_id INTEGER, location VARCHAR(100));
        CREATE TABLE IF NOT EXISTS raw_readings (reading_id INTEGER, sensor_id INTEGER, temperature DECIMAL(5,2), timestamp TIMESTAMP);
        CREATE TABLE IF NOT EXISTS raw_weather (date DATE, location VARCHAR(100), condition VARCHAR(50), avg_temp NUMERIC(5, 2));
        
        TRUNCATE TABLE raw_sensors, raw_readings, raw_weather;
        """,
    )
    
    load_tasks = [
        PythonOperator(task_id='load_sensors', python_callable=load_sensors_to_staging),
        PythonOperator(task_id='load_readings', python_callable=load_readings_to_staging),
        PythonOperator(task_id='load_weather', python_callable=load_weather_to_staging),
    ]

    transform_in_sql_task = PostgresOperator(
        task_id='transform_in_sql',
        postgres_conn_id=POSTGRES_CONN_ID,
        sla=timedelta(minutes=30),
        sql="""
        -- Membuat tabel utama (jika belum ada) dengan partisi
        CREATE TABLE IF NOT EXISTS daily_sensor_summary_elt (
            location VARCHAR(100),
            date DATE,
            avg_temp NUMERIC(5,2),
            min_temp NUMERIC(5,2),
            max_temp NUMERIC(5,2),
            moving_avg_3day NUMERIC(5,2),
            reading_count INTEGER,
            weather_condition VARCHAR(50),
            weather_avg_temp NUMERIC(5,2),
            quality_flag VARCHAR(10),
            created_at TIMESTAMP
        ) PARTITION BY RANGE (date);

        -- Membuat partisi untuk tanggal saat ini 
        CREATE TABLE IF NOT EXISTS summary_partition_{{ ds_nodash }}
        PARTITION OF daily_sensor_summary_elt
        FOR VALUES FROM ('{{ ds }}') TO ('{{ next_ds }}');

        -- Memasukkan data ke dalam tabel yang sudah dipartisi
        INSERT INTO daily_sensor_summary_elt
        WITH daily_stats AS (
            SELECT
                s.location,
                DATE(r.timestamp) AS date,
                AVG(r.temperature) AS avg_temp,
                MIN(r.temperature) AS min_temp,
                MAX(r.temperature) AS max_temp,
                COUNT(r.temperature) AS reading_count
            FROM raw_readings r
            JOIN raw_sensors s ON r.sensor_id = s.sensor_id
            -- Memfilter data hanya untuk rentang waktu eksekusi saat ini
            WHERE r.timestamp >= '{{ data_interval_start }}' AND r.timestamp < '{{ data_interval_end }}'
            GROUP BY s.location, DATE(r.timestamp)
        )
        SELECT
            d.location,
            d.date,
            ROUND(d.avg_temp::numeric, 2),
            ROUND(d.min_temp::numeric, 2),
            ROUND(d.max_temp::numeric, 2),
            ROUND(AVG(d.avg_temp) OVER (PARTITION BY d.location ORDER BY d.date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)::numeric, 2),
            d.reading_count,
            w.condition,
            w.avg_temp,
            CASE WHEN ROUND(d.max_temp::numeric, 2) > 25.0 THEN 'ABNORMAL' ELSE 'NORMAL' END,
            CURRENT_TIMESTAMP
        FROM daily_stats d
        LEFT JOIN raw_weather w ON d.location = w.location AND d.date = w.date;
        """,
    )

    validate_data = PostgresOperator(
        task_id='validate_data',
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="""
        DO $$
        DECLARE
            row_count INTEGER;
        BEGIN
            -- Cek apakah tabel summary memiliki data
            SELECT COUNT(*) INTO row_count FROM daily_sensor_summary_elt;
            IF row_count = 0 THEN
                RAISE EXCEPTION 'Validasi Gagal: Tabel summary kosong!';
            END IF;

            -- Cek apakah ada data cuaca yang hilang (NULL) setelah join
            SELECT COUNT(*) INTO row_count FROM daily_sensor_summary_elt WHERE weather_condition IS NULL;
            IF row_count > 0 THEN
                RAISE EXCEPTION 'Validasi Gagal: Ditemukan % baris tanpa data cuaca!', row_count;
            END IF;

            RAISE NOTICE 'Validasi Data Lolos! Semua data terisi dengan benar.';
        END $$;
        """,
)

    optimize_queries_task = PostgresOperator(
        task_id='optimize_queries',
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="""
            -- Membuat index pada tabel utama untuk percepat query
            CREATE INDEX IF NOT EXISTS idx_summary_location_date 
            ON daily_sensor_summary_elt(location, date);
        """
    )
    
    branching_task = BranchPythonOperator(task_id='branching_task', python_callable=check_for_anomalies)
    send_alert_task = DummyOperator(task_id='send_alert_task')
    no_alert_task = DummyOperator(task_id='no_alert_task')

    log_metrics_task = PythonOperator(
        task_id='log_metrics_task',
        python_callable=log_summary_metrics,
)

    create_staging_tables_task >> load_tasks
    load_tasks >> transform_in_sql_task
    transform_in_sql_task >> validate_data >> log_metrics_task >> branching_task
    branching_task >> [send_alert_task, no_alert_task]