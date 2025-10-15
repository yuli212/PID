# 📚 PANDUAN PRAKTIKUM: ETL vs ELT dengan Apache Airflow

## 🎯 Tujuan Pembelajaran

Setelah menyelesaikan praktikum ini, mahasiswa diharapkan dapat:

1. **Memahami konsep fundamental** perbedaan antara ETL dan ELT
2. **Mengimplementasikan pipeline** ETL dan ELT menggunakan Apache Airflow
3. **Menganalisis performa** dan use case yang tepat untuk masing-masing approach
4. **Mengelola data warehouse** dengan PostgreSQL
5. **Mengoperasikan containerized environment** dengan Docker

---

## 📋 Prerequisites

### Software yang Dibutuhkan
- **Docker Desktop** (versi terbaru)
- **Text Editor/IDE** (VS Code, IntelliJ, dll)
- **Web Browser** (Chrome, Firefox, dll)
- **Terminal/Command Prompt**

### Pengetahuan Dasar
- Konsep database dan SQL
- Pemahaman dasar Python dan pandas
- Familiar dengan command line
- Konsep containerization (Docker)

---

## 🏗️ Arsitektur Sistem

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Source Data   │    │   Apache        │    │  Data Warehouse │
│   (CSV Files)   │───▶│   Airflow       │───▶│   (PostgreSQL)  │
│                 │    │                 │    │                 │
│ • sensors.csv   │    │ • ETL Pipeline  │    │ • Summary ETL   │
│ • readings.csv  │    │ • ELT Pipeline  │    │ • Summary ELT   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Komponen Sistem
- **Airflow Webserver**: Interface untuk monitoring dan kontrol
- **Airflow Scheduler**: Menjalankan task sesuai schedule
- **Airflow Worker**: Mengeksekusi task individual
- **PostgreSQL**: Database untuk metadata Airflow dan data warehouse
- **Redis**: Message broker untuk distributed task execution

---

## 📊 Skenario Praktikum

### Context: Smart Building IoT System
Anda bekerja sebagai **Data Engineer** di perusahaan yang mengelola sistem IoT untuk smart building. Sistem ini mengumpulkan data suhu dari berbagai sensor yang tersebar di gedung.

### Data Sources
1. **sensors.csv**: Metadata sensor (sensor_id, location)
2. **readings.csv**: Time-series data suhu (reading_id, sensor_id, temperature, timestamp)

### Business Requirement
Membuat **daily summary report** yang menampilkan:
- Average temperature per location per day
- Minimum temperature per location per day  
- Maximum temperature per location per day
- Number of readings per location per day

---

## 🚀 Langkah-Langkah Praktikum

### STEP 1: Setup Environment

#### 1.1 Clone/Download Project
```bash
# Buat direktori project
mkdir airflow-iot-demo
cd airflow-iot-demo

# Atau gunakan project yang sudah ada
cd /Users/ekosakti/Code/PID/airflow/airflow-iot-demo
```

#### 1.2 Verifikasi File Structure
```bash
ls -la
```

Pastikan struktur folder seperti ini:
```
airflow-iot-demo/
├── dags/
│   ├── etl_iot_pipeline.py
│   └── elt_iot_pipeline.py
├── data/
│   ├── sensors.csv
│   └── readings.csv
├── docker-compose.yml
├── init_postgres.sh
├── .env
├── README.md
└── PANDUAN_PRAKTIKUM.md
```

#### 1.3 Set Permissions
```bash
chmod +x init_postgres.sh
chmod +x start.sh
chmod +x check.sh
```

### STEP 2: Start Docker Environment

#### 2.1 Start Services
```bash
docker compose up -d
```

#### 2.2 Check Service Status
```bash
docker compose ps
```

Expected output:
```
NAME                     STATUS
airflow-init            exited (0)
airflow-scheduler       running
airflow-webserver       running (healthy)
airflow-worker          running
postgres                running
redis                   running
```

#### 2.3 Wait for Initialization
```bash
# Check if Airflow is ready
curl -f http://localhost:8080/health

# Or use the status check script
./check.sh
```

### STEP 3: Access Airflow UI

#### 3.1 Open Web Interface
- **URL**: http://localhost:8080
- **Username**: `admin`
- **Password**: `admin`

#### 3.2 Explore Interface
1. **DAGs**: Lihat daftar available pipelines
2. **Admin > Connections**: Verifikasi koneksi database
3. **Admin > Variables**: Check environment variables

### STEP 4: Analyze Source Data

#### 4.1 Inspect CSV Files
```bash
# Check sensors data
head -5 data/sensors.csv
wc -l data/sensors.csv

# Check readings data  
head -10 data/readings.csv
wc -l data/readings.csv
```

#### 4.2 Data Analysis Questions
**📝 TUGAS**: Jawab pertanyaan berikut:
1. Berapa jumlah sensor yang ada?
2. Berapa jumlah total readings?
3. Sensor di lokasi mana yang memiliki suhu tertinggi?
4. Berapa rentang tanggal data yang tersedia?

### STEP 5: Jalankan ETL Pipeline

#### 5.1 Enable DAG
1. Di Airflow UI, cari DAG `etl_iot_pipeline`
2. Toggle switch untuk mengaktifkan DAG
3. Klik pada DAG name untuk melihat detail

#### 5.2 Trigger Manual Run
1. Klik tombol "Trigger DAG" (play button)
2. Confirm execution
3. Monitor progress di Graph View

#### 5.3 Analyze ETL Execution
**📝 TUGAS**: Monitor dan catat:
1. **Execution Time**: Berapa lama setiap task?
2. **Task Dependencies**: Bagaimana urutan eksekusi?
3. **Logs**: Check logs untuk setiap task
4. **XCom**: Lihat data yang dipassing antar task

#### 5.4 Verify ETL Results
```bash
# Connect to database
docker compose exec postgres psql -U airflow -d dwh

# Check ETL results
SELECT * FROM daily_sensor_summary_etl ORDER BY location, date;

# Count records
SELECT COUNT(*) FROM daily_sensor_summary_etl;
```

### STEP 6: Jalankan ELT Pipeline

#### 6.1 Enable and Trigger ELT DAG
1. Enable `elt_iot_pipeline` DAG
2. Trigger manual execution
3. Monitor di Graph View

#### 6.2 Analyze ELT Execution
**📝 TUGAS**: Bandingkan dengan ETL:
1. **Task Structure**: Apa perbedaan struktur task?
2. **Data Flow**: Bagaimana data mengalir?
3. **Transformation**: Dimana transformasi terjadi?

#### 6.3 Verify ELT Results
```bash
# Check staging tables
SELECT COUNT(*) FROM raw_sensors;
SELECT COUNT(*) FROM raw_readings;

# Check final results
SELECT * FROM daily_sensor_summary_elt ORDER BY location, date;

# Compare ETL vs ELT results
SELECT 'ETL' as pipeline, COUNT(*) as records FROM daily_sensor_summary_etl
UNION ALL
SELECT 'ELT' as pipeline, COUNT(*) as records FROM daily_sensor_summary_elt;
```

### STEP 7: Comparative Analysis

#### 7.1 Performance Comparison
**📝 TUGAS**: Buat tabel perbandingan:

| Metric | ETL Pipeline | ELT Pipeline |
|--------|-------------|-------------|
| Total Execution Time | ___ minutes | ___ minutes |
| Extract Task Time | ___ seconds | ___ seconds |
| Transform Task Time | ___ seconds | ___ seconds |
| Load Task Time | ___ seconds | ___ seconds |
| Memory Usage | High/Low | High/Low |
| Network I/O | High/Low | High/Low |

#### 7.2 Data Quality Check
```sql
-- Check if results are identical
SELECT 
    e.location,
    e.date,
    e.avg_temp as etl_avg,
    l.avg_temp as elt_avg,
    ABS(e.avg_temp - l.avg_temp) as diff
FROM daily_sensor_summary_etl e
JOIN daily_sensor_summary_elt l ON e.location = l.location AND e.date = l.date
WHERE ABS(e.avg_temp - l.avg_temp) > 0.01;
```

### STEP 8: Troubleshooting

#### 8.1 Common Issues
**Problem**: DAGs not appearing
```bash
# Check DAG parsing errors
docker compose logs airflow-scheduler | grep ERROR

# Restart scheduler
docker compose restart airflow-scheduler
```

**Problem**: Database connection failed
```bash
# Check postgres status
docker compose exec postgres pg_isready -U airflow

# Check connection in Airflow
# Admin > Connections > postgres_default
```

**Problem**: Task failed
```bash
# Check specific task logs
# Click on failed task in Graph View > Logs

# Check worker logs
docker compose logs airflow-worker
```

---

## 📝 TUGAS EVALUASI

### Tugas 1: Analisis Komparatif (30%)
Buat laporan yang membandingkan:
1. **Architecture**: Perbedaan arsitektur ETL vs ELT
2. **Performance**: Waktu eksekusi dan resource usage
3. **Scalability**: Mana yang lebih scalable untuk big data?
4. **Use Cases**: Kapan menggunakan ETL vs ELT?

### Tugas 2: Modifikasi Pipeline (40%)
1. **Tambah Data Source**: 
   - Buat file `weather.csv` dengan data cuaca
   - Modifikasi pipeline untuk include weather data
   
2. **Advanced Transformations**:
   - Tambah moving average calculation
   - Implementasi data quality checks
   - Tambah alerting untuk suhu abnormal

3. **Optimization**:
   - Implement incremental loading
   - Add data partitioning
   - Optimize SQL queries

### Tugas 3: Monitoring & Alerting (30%)
1. **Setup Monitoring**:
   - Configure email notifications
   - Setup SLA monitoring
   - Create custom metrics

2. **Error Handling**:
   - Implement retry mechanisms
   - Add data validation steps
   - Create failure notifications

---

## 🔬 EKSPERIMEN LANJUTAN

### Eksperimen 1: Scale Testing
```bash
# Generate larger dataset
python scripts/generate_data.py --sensors 100 --days 30 --readings-per-hour 4

# Compare performance with larger data
```

### Eksperimen 2: Different Data Sources
- Add MySQL source
- Add REST API data source
- Add streaming data (Kafka)

### Eksperimen 3: Advanced Transformations
- Machine learning integration
- Real-time alerting
- Data quality monitoring

---

## 📊 RUBRIK PENILAIAN

| Kriteria | Excellent (A) | Good (B) | Satisfactory (C) | Needs Improvement (D) |
|----------|---------------|----------|------------------|----------------------|
| **Technical Implementation** | All pipelines working perfectly, optimized code | Pipelines working with minor issues | Basic implementation working | Multiple technical issues |
| **Analysis & Understanding** | Deep understanding of ETL vs ELT concepts | Good understanding with examples | Basic understanding | Limited understanding |
| **Documentation** | Comprehensive documentation with insights | Good documentation | Basic documentation | Minimal documentation |
| **Problem Solving** | Innovative solutions and optimizations | Creative problem solving | Standard solutions | Basic problem solving |

---

## 🎓 KESIMPULAN PEMBELAJARAN

Setelah menyelesaikan praktikum ini, Anda akan memahami:

### Key Takeaways:
1. **ETL Pipeline**: 
   - Transform di application layer (Python/pandas)
   - Cocok untuk complex business logic
   - Resource intensive di compute layer

2. **ELT Pipeline**:
   - Transform di database layer (SQL)
   - Memanfaatkan database engine power
   - Scalable untuk big data scenarios

3. **Apache Airflow**:
   - Powerful orchestration tool
   - Supports both patterns
   - Rich monitoring dan alerting capabilities

### Best Practices:
- Pilih ETL untuk complex transformations
- Pilih ELT untuk big data dan simple aggregations
- Always implement proper monitoring
- Consider data lineage dan quality checks

### Next Steps:
- Explore Apache Spark for big data ETL
- Learn about streaming ETL/ELT
- Study data lake architectures
- Practice with cloud platforms (AWS, GCP, Azure)

---

## 📚 REFERENSI

1. [Apache Airflow Documentation](https://airflow.apache.org/docs/)
2. [ETL vs ELT: What's the Difference?](https://www.fivetran.com/blog/etl-vs-elt)
3. [Modern Data Stack](https://www.getdbt.com/analytics-engineering/transformation/)
4. [Docker Compose Reference](https://docs.docker.com/compose/)

---

**📧 Contact**: Jika ada pertanyaan atau issues, hubungi instruktur atau buat issue di repository ini.

**⭐ Selamat Belajar!**