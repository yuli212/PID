# Airflow IoT ETL vs ELT Demo

Demo project yang menunjukkan perbedaan core antara ETL dan ELT pipelines menggunakan Apache Airflow 2.x dengan skenario agregasi data sensor IoT.

## 🏗️ Arsitektur

### ETL Pipeline (etl_iot_pipeline.py)
- **Extract**: Membaca data dari CSV files ke pandas DataFrames
- **Transform**: Melakukan join, grouping, dan agregasi **di memory menggunakan pandas**
- **Load**: Memasukkan hasil transformasi ke data warehouse

### ELT Pipeline (elt_iot_pipeline.py)
- **Extract/Load**: Memuat raw data langsung ke staging tables
- **Transform**: Melakukan transformasi **di dalam database menggunakan SQL**

## 📊 Data Schema

### Input Data
- `sensors.csv`: sensor_id, location
- `readings.csv`: reading_id, sensor_id, temperature, timestamp

### Output Tables
- `daily_sensor_summary_etl`: Hasil dari ETL pipeline
- `daily_sensor_summary_elt`: Hasil dari ELT pipeline

## 🚀 Cara Menjalankan

### 1. Setup Environment
```bash
cd /Users/ekosakti/Code/PID/airflow/airflow-iot-demo

# Pastikan script postgres executable
chmod +x init_postgres.sh

# Set AIRFLOW_UID untuk permission yang benar
echo "AIRFLOW_UID=$(id -u)" > .env
```

### 2. Start Docker Environment
```bash
# Start semua services
docker-compose up -d

# Cek status services
docker-compose ps

# Cek logs jika ada masalah
docker-compose logs -f
```

### 3. Access Airflow UI
- URL: http://localhost:8080
- Username: `admin`
- Password: `admin`

### 4. Jalankan Pipelines
1. Di Airflow UI, aktifkan DAGs:
   - `etl_iot_pipeline`
   - `elt_iot_pipeline`

2. Trigger manual kedua pipelines untuk melihat perbedaannya

### 5. Verifikasi Results
```bash
# Connect ke PostgreSQL container
docker-compose exec postgres psql -U airflow -d dwh

# Cek hasil ETL pipeline
SELECT * FROM daily_sensor_summary_etl ORDER BY location, date;

# Cek hasil ELT pipeline  
SELECT * FROM daily_sensor_summary_elt ORDER BY location, date;

# Bandingkan kedua hasil
SELECT 'ETL' as pipeline, COUNT(*) as records FROM daily_sensor_summary_etl
UNION ALL
SELECT 'ELT' as pipeline, COUNT(*) as records FROM daily_sensor_summary_elt;
```

## 🔍 Key Differences

| Aspect | ETL Pipeline | ELT Pipeline |
|--------|-------------|-------------|
| **Transformation Location** | In-memory (pandas) | In-database (SQL) |
| **Data Movement** | Transform then load | Load then transform |
| **Resource Usage** | Airflow worker memory | Database compute |
| **Scalability** | Limited by worker RAM | Limited by DB resources |
| **Data Validation** | During transformation | After loading |

## 🛠️ Troubleshooting

### Common Issues

1. **Permission Errors**
   ```bash
   sudo chown -R $(id -u):$(id -g) ./
   ```

2. **Port Already in Use**
   ```bash
   # Stop existing services
   docker-compose down
   
   # Check port usage
   lsof -i :8080
   lsof -i :5432
   ```

3. **Database Connection Issues**
   ```bash
   # Restart postgres service
   docker-compose restart postgres
   
   # Check postgres logs
   docker-compose logs postgres
   ```

### Reset Environment
```bash
# Stop dan remove containers
docker-compose down -v

# Remove volumes (akan menghapus semua data!)
docker volume prune

# Start fresh
docker-compose up -d
```

## 📋 Services Overview

- **airflow-webserver**: Port 8080 - Airflow UI
- **airflow-scheduler**: Menjalankan task scheduling
- **airflow-worker**: Menjalankan tasks
- **postgres**: Port 5432 - Database (airflow_db + dwh)
- **redis**: Port 6379 - Message broker untuk Celery

## 📈 Expected Results

Setelah menjalankan kedua pipelines, Anda akan melihat:

1. **Staging Tables** (dari ELT pipeline):
   - `raw_sensors`: Raw sensor data
   - `raw_readings`: Raw readings data

2. **Summary Tables** (hasil akhir):
   - `daily_sensor_summary_etl`: Agregasi per location per hari (ETL)
   - `daily_sensor_summary_elt`: Agregasi per location per hari (ELT)

3. **Performance Comparison**:
   - ETL: Transformation time in Python
   - ELT: Transformation time in SQL

## 🧪 Testing Different Scenarios

### Add More Data
Edit `data/readings.csv` untuk menambah data dan lihat bagaimana performa berubah.

### Scale Testing  
Modify CSV files dengan lebih banyak sensors dan readings untuk test scalability.

### Error Handling
Introduce data quality issues untuk test error handling di kedua pipelines.

## 📚 Learning Points

1. **ETL**: Baik untuk complex business logic, data cleansing
2. **ELT**: Baik untuk big data, leveraging database power
3. **Airflow**: Orchestration tool yang powerful untuk kedua patterns
4. **Docker**: Easy deployment dan environment consistency