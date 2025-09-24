# 🚀 Airflow IoT Demo - Complete Hands-on Tutorial

## ✅ Project Successfully Created!

Hands-on tutorial project untuk demonstrasi ETL vs ELT pipelines menggunakan Apache Airflow 2.x dengan skenario IoT sensor data aggregation.

### 📁 Project Structure
```
airflow-iot-demo/
├── dags/
│   ├── etl_iot_pipeline.py       # ETL Pipeline (Transform in Memory)
│   └── elt_iot_pipeline.py       # ELT Pipeline (Transform in Database)
├── data/
│   ├── sensors.csv               # Sensor metadata (8 sensors)
│   └── readings.csv              # Temperature readings (28 records)
├── docker-compose.yml            # Docker environment setup
├── init_postgres.sh              # Database initialization
├── .env                          # Environment variables
├── test.sh                       # Testing script
└── README.md                     # Documentation
```

### 🐳 Environment Status
- ✅ **Docker Services**: Running
- ✅ **PostgreSQL**: Connected (`dwh` database ready)
- ✅ **Airflow UI**: Accessible at http://localhost:8080
- ✅ **Redis**: Running (Celery broker)
- ✅ **Data Files**: Loaded (8 sensors, 28 readings)

### 📊 Demo Scenarios

#### ETL Pipeline (`etl_iot_pipeline`)
1. **Extract**: Reads CSV files into pandas DataFrames
2. **Transform**: Joins, groups, aggregates in memory using pandas
3. **Load**: Inserts transformed data to `daily_sensor_summary_etl`

#### ELT Pipeline (`elt_iot_pipeline`)  
1. **Extract/Load**: Loads raw CSV data to staging tables
2. **Transform**: SQL-based transformation in PostgreSQL database
3. **Result**: Creates `daily_sensor_summary_elt` using SQL aggregation

### 🎯 How to Run Demo

1. **Access Airflow UI**:
   ```
   URL: http://localhost:8080
   Username: admin
   Password: admin
   ```

2. **Enable & Trigger DAGs**:
   - Find `etl_iot_pipeline` and `elt_iot_pipeline`
   - Toggle them ON (unpause)
   - Click "Trigger DAG" for each

3. **Compare Results**:
   ```bash
   # Connect to database
   docker compose exec postgres psql -U airflow -d dwh
   
   # Check ETL results
   SELECT * FROM daily_sensor_summary_etl;
   
   # Check ELT results  
   SELECT * FROM daily_sensor_summary_elt;
   
   # Compare counts
   SELECT 'ETL' as pipeline, COUNT(*) FROM daily_sensor_summary_etl
   UNION ALL
   SELECT 'ELT' as pipeline, COUNT(*) FROM daily_sensor_summary_elt;
   ```

### 🔧 Useful Commands

```bash
# Check service status
docker compose ps

# Follow all logs
docker compose logs -f

# Check specific service logs
docker compose logs airflow-webserver
docker compose logs airflow-scheduler

# Connect to database
docker compose exec postgres psql -U airflow -d dwh

# Stop environment
docker compose down

# Restart environment
docker compose down && docker compose up -d

# Clean restart (removes all data!)
docker compose down -v && docker compose up -d
```

### 🧪 Testing & Verification

```bash
# Run comprehensive test
./test.sh

# Manual verification
docker compose exec postgres psql -U airflow -d dwh -c "
SELECT 
    location,
    date,
    avg_temp,
    min_temp,
    max_temp,
    reading_count
FROM daily_sensor_summary_etl 
ORDER BY location, date;
"
```

### 📈 Expected Results

After running both pipelines, you should see:

1. **8 unique locations**: Room101, Room102, Room201, Room202, Lobby, Kitchen, Conference_Room, Server_Room
2. **2 dates**: 2025-09-23 and 2025-09-24  
3. **Daily aggregations**: AVG, MIN, MAX temperature per location per day
4. **Identical results** from both ETL and ELT approaches

### 🎓 Learning Objectives

| Aspect | ETL (Transform in Memory) | ELT (Transform in Database) |
|--------|--------------------------|----------------------------|
| **Processing** | Python/pandas | SQL |
| **Resource Usage** | Airflow worker RAM | Database CPU/RAM |
| **Scalability** | Limited by worker memory | Limited by DB resources |
| **Complexity** | Good for business logic | Good for set operations |
| **Data Movement** | Transform → Load | Load → Transform |

### 🔍 Troubleshooting

1. **DAGs not appearing**: Wait 1-2 minutes for DAG parsing
2. **Database connection issues**: Check `docker compose logs postgres`
3. **Memory issues**: Increase Docker memory allocation
4. **Port conflicts**: Change ports in `docker-compose.yml`

### 🏁 Success Criteria

✅ Both pipelines complete successfully  
✅ Same number of records in both summary tables  
✅ Identical aggregation results  
✅ Different execution patterns observed  

---

## 🎉 Demo is Ready!

Environment berhasil dibuat dan siap untuk hands-on demonstration. 

**Next Step**: Buka http://localhost:8080 dan mulai explore perbedaan antara ETL dan ELT patterns!