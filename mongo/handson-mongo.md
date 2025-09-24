# Hands-on: Menyimpan Data IoT ke MongoDB & Querying via MongoShell

## Prerequisites

- Docker dan Docker Compose terinstall (Docker Desktop atau OrbStack)
- Python 3.7+ terinstall
- Text editor (VS Code, Sublime, dll)
- Terminal/Command Prompt

## 1. Setup MongoDB dengan Docker

### 1.1 Buat Docker Compose File

Buat file `docker-compose.yml`:

```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:7.0
    container_name: mongodb-iot
    restart: always
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
      MONGO_INITDB_DATABASE: iot_db
    volumes:
      - mongodb_data:/data/db
      - ./init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js:ro
    networks:
      - iot-network

  mongo-express:
    image: mongo-express:1.0.0
    container_name: mongo-express-iot
    restart: always
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: password123
      ME_CONFIG_MONGODB_URL: mongodb://admin:password123@mongodb:27017/
      ME_CONFIG_BASICAUTH_USERNAME: admin
      ME_CONFIG_BASICAUTH_PASSWORD: password123
      ME_CONFIG_BASICAUTH: true
    depends_on:
      - mongodb
    networks:
      - iot-network

volumes:
  mongodb_data:

networks:
  iot-network:
    driver: bridge
```

### 1.2 Buat Script Inisialisasi Database

Buat file `init-mongo.js`:

```javascript
// Beralih ke database iot_db
db = db.getSiblingDB('iot_db');

// Buat user untuk aplikasi
db.createUser({
  user: 'iot_user',
  pwd: 'iot_password',
  roles: [
    {
      role: 'readWrite',
      db: 'iot_db'
    }
  ]
});

// Buat collection untuk sensor data
db.createCollection('sensor_data');
db.createCollection('devices');
db.createCollection('alerts');

// Insert sample devices
db.devices.insertMany([
  {
    device_id: 'ESP32_001',
    device_name: 'Temperature Sensor Living Room',
    location: 'Living Room',
    device_type: 'temperature_humidity',
    status: 'active',
    created_at: new Date(),
    last_seen: new Date()
  },
  {
    device_id: 'ESP32_002',
    device_name: 'Motion Sensor Bedroom',
    location: 'Bedroom',
    device_type: 'motion',
    status: 'active',
    created_at: new Date(),
    last_seen: new Date()
  },
  {
    device_id: 'ESP32_003',
    device_name: 'Light Sensor Garden',
    location: 'Garden',
    device_type: 'light',
    status: 'active',
    created_at: new Date(),
    last_seen: new Date()
  }
]);

print('Database initialization completed!');
```

### 1.3 Jalankan MongoDB

```bash
# Jalankan container
docker-compose up -d

# Cek status container
docker-compose ps

# Lihat logs MongoDB untuk memastikan inisialisasi berhasil
docker-compose logs mongodb

# Tunggu sampai melihat pesan "Database initialization completed!"
```

### 1.4 Verifikasi Setup

```bash
# Test koneksi ke MongoDB
docker exec -it mongodb-iot mongosh --eval "db.adminCommand('ping')"

# Akses Mongo Express di browser
# Buka http://localhost:8081
# Anda akan melihat database iot_db dengan collections yang sudah dibuat
```

## 2. Simulasi Data IoT

### 2.1 Buat Script Python untuk Generate Data

Buat file `iot_data_generator.py`:

```python
import pymongo
import random
import time
from datetime import datetime, timedelta
import json

# Connection ke MongoDB
client = pymongo.MongoClient("mongodb://iot_user:iot_password@localhost:27017/iot_db")
db = client.iot_db

def generate_temperature_data(device_id):
    """Generate data sensor suhu dan kelembaban"""
    return {
        'device_id': device_id,
        'timestamp': datetime.utcnow(),
        'sensor_type': 'temperature_humidity',
        'data': {
            'temperature': round(random.uniform(20.0, 35.0), 2),
            'humidity': round(random.uniform(40.0, 80.0), 2),
            'heat_index': round(random.uniform(25.0, 40.0), 2)
        },
        'location': 'Living Room',
        'battery_level': random.randint(60, 100),
        'signal_strength': random.randint(-80, -30)
    }

def generate_motion_data(device_id):
    """Generate data sensor gerak"""
    return {
        'device_id': device_id,
        'timestamp': datetime.utcnow(),
        'sensor_type': 'motion',
        'data': {
            'motion_detected': random.choice([True, False]),
            'motion_intensity': random.randint(1, 10) if random.choice([True, False]) else 0
        },
        'location': 'Bedroom',
        'battery_level': random.randint(70, 100),
        'signal_strength': random.randint(-75, -35)
    }

def generate_light_data(device_id):
    """Generate data sensor cahaya"""
    return {
        'device_id': device_id,
        'timestamp': datetime.utcnow(),
        'sensor_type': 'light',
        'data': {
            'light_intensity': random.randint(0, 1000),
            'uv_index': round(random.uniform(0, 11), 1)
        },
        'location': 'Garden',
        'battery_level': random.randint(50, 100),
        'signal_strength': random.randint(-70, -40)
    }

def generate_alert(device_id, alert_type, message):
    """Generate alert jika ada kondisi tertentu"""
    return {
        'device_id': device_id,
        'timestamp': datetime.utcnow(),
        'alert_type': alert_type,
        'severity': random.choice(['low', 'medium', 'high']),
        'message': message,
        'acknowledged': False,
        'created_at': datetime.utcnow()
    }

def main():
    print("Starting IoT Data Generator...")
    
    try:
        while True:
            # Generate data untuk setiap device
            temp_data = generate_temperature_data('ESP32_001')
            motion_data = generate_motion_data('ESP32_002')
            light_data = generate_light_data('ESP32_003')
            
            # Insert data ke MongoDB
            db.sensor_data.insert_one(temp_data)
            db.sensor_data.insert_one(motion_data)
            db.sensor_data.insert_one(light_data)
            
            # Generate alerts berdasarkan kondisi tertentu
            if temp_data['data']['temperature'] > 30:
                alert = generate_alert('ESP32_001', 'high_temperature', 
                                     f"High temperature detected: {temp_data['data']['temperature']}°C")
                db.alerts.insert_one(alert)
                
            if motion_data['data']['motion_detected'] and motion_data['data']['motion_intensity'] > 7:
                alert = generate_alert('ESP32_002', 'motion_detected', 
                                     f"High motion intensity detected: {motion_data['data']['motion_intensity']}")
                db.alerts.insert_one(alert)
                
            if light_data['data']['light_intensity'] < 100:
                alert = generate_alert('ESP32_003', 'low_light', 
                                     f"Low light detected: {light_data['data']['light_intensity']} lux")
                db.alerts.insert_one(alert)
            
            print(f"Data inserted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(10)  # Generate data setiap 10 detik
            
    except KeyboardInterrupt:
        print("\nData generator stopped.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
```

### 2.2 Install Dependencies dan Jalankan Generator

```bash
# Install pymongo
pip install pymongo

# Jalankan generator (akan berjalan terus-menerus)
python iot_data_generator.py

# Generator akan menampilkan output seperti:
# Starting IoT Data Generator...
# Data inserted at 2025-09-18 06:17:07
# Data inserted at 2025-09-18 06:17:17
# ...

# Untuk menghentikan generator, tekan Ctrl+C
```

### 2.3 Verifikasi Data Generation

```bash
# Buka terminal baru dan connect ke MongoDB
docker exec -it mongodb-iot mongosh -u admin -p password123 --authenticationDatabase admin

# Di MongoDB shell:
use iot_db
db.auth('iot_user', 'iot_password')

# Cek jumlah data yang sudah ter-generate
db.sensor_data.countDocuments()

# Lihat data terbaru
db.sensor_data.find().sort({timestamp: -1}).limit(5).pretty()
```

## 3. MongoDB Shell Commands

### 3.1 Connect ke MongoDB Shell

```bash
# Connect ke MongoDB container dengan admin credentials
docker exec -it mongodb-iot mongosh -u admin -p password123 --authenticationDatabase admin

# Atau connect langsung tanpa kredensial admin (akan perlu authenticate manual)
docker exec -it mongodb-iot mongosh
```

**Catatan Penting:**
- Perintah `docker exec` dijalankan di terminal bash/zsh, BUKAN di dalam MongoDB shell
- Untuk keluar dari MongoDB shell, ketik `exit` atau tekan Ctrl+D
- Jika sudah berada di MongoDB shell, jangan gunakan perintah `docker exec` lagi

### 3.2 Basic Commands

```javascript
// Beralih ke database iot_db
use iot_db

// Authenticate sebagai iot_user
db.auth('iot_user', 'iot_password')

// Lihat collections
show collections

// Lihat devices
db.devices.find().pretty()

// Count total sensor data
db.sensor_data.countDocuments()
```

## 4. Querying Data IoT

### 4.1 Basic Queries

```javascript
// Ambil 10 data sensor terbaru
db.sensor_data.find().sort({timestamp: -1}).limit(10).pretty()

// Filter berdasarkan device_id
db.sensor_data.find({device_id: "ESP32_001"}).pretty()

// Filter berdasarkan sensor_type
db.sensor_data.find({sensor_type: "temperature_humidity"}).pretty()

// Filter berdasarkan range waktu (1 jam terakhir)
db.sensor_data.find({
  timestamp: {
    $gte: new Date(Date.now() - 60*60*1000)
  }
}).pretty()

// Filter berdasarkan suhu > 25°C
db.sensor_data.find({
  "data.temperature": {$gt: 25}
}).pretty()
```

### 4.2 Advanced Queries

```javascript
// Aggregation: Rata-rata suhu per device
db.sensor_data.aggregate([
  {$match: {sensor_type: "temperature_humidity"}},
  {$group: {
    _id: "$device_id",
    avg_temperature: {$avg: "$data.temperature"},
    avg_humidity: {$avg: "$data.humidity"},
    count: {$sum: 1}
  }},
  {$sort: {avg_temperature: -1}}
])

// Agregasi data per hari
db.sensor_data.aggregate([
  {$match: {sensor_type: "temperature_humidity"}},
  {$group: {
    _id: {
      year: {$year: "$timestamp"},
      month: {$month: "$timestamp"},
      day: {$dayOfMonth: "$timestamp"}
    },
    avg_temp: {$avg: "$data.temperature"},
    min_temp: {$min: "$data.temperature"},
    max_temp: {$max: "$data.temperature"},
    count: {$sum: 1}
  }},
  {$sort: {"_id.year": -1, "_id.month": -1, "_id.day": -1}}
])

// Find motion events dalam 24 jam terakhir
db.sensor_data.find({
  sensor_type: "motion",
  "data.motion_detected": true,
  timestamp: {
    $gte: new Date(Date.now() - 24*60*60*1000)
  }
}).sort({timestamp: -1})

// Time series analysis: Data per jam
db.sensor_data.aggregate([
  {$match: {
    sensor_type: "temperature_humidity",
    timestamp: {$gte: new Date(Date.now() - 24*60*60*1000)}
  }},
  {$group: {
    _id: {
      year: {$year: "$timestamp"},
      month: {$month: "$timestamp"},
      day: {$dayOfMonth: "$timestamp"},
      hour: {$hour: "$timestamp"}
    },
    avg_temperature: {$avg: "$data.temperature"},
    avg_humidity: {$avg: "$data.humidity"},
    readings_count: {$sum: 1}
  }},
  {$sort: {"_id.year": 1, "_id.month": 1, "_id.day": 1, "_id.hour": 1}}
])
```

### 4.3 Alert Queries

```javascript
// Semua alerts yang belum di-acknowledge
db.alerts.find({acknowledged: false}).sort({timestamp: -1})

// Alerts berdasarkan severity
db.alerts.find({severity: "high"}).sort({timestamp: -1})

// Count alerts per device
db.alerts.aggregate([
  {$group: {
    _id: "$device_id",
    total_alerts: {$sum: 1},
    high_severity: {$sum: {$cond: [{$eq: ["$severity", "high"]}, 1, 0]}},
    latest_alert: {$max: "$timestamp"}
  }},
  {$sort: {total_alerts: -1}}
])

// Acknowledge alert
db.alerts.updateOne(
  {_id: ObjectId("YOUR_ALERT_ID")},
  {$set: {acknowledged: true, acknowledged_at: new Date()}}
)
```

### 4.4 Performance Queries

```javascript
// Buat index untuk performance
db.sensor_data.createIndex({device_id: 1, timestamp: -1})
db.sensor_data.createIndex({sensor_type: 1, timestamp: -1})
db.sensor_data.createIndex({timestamp: -1})
db.alerts.createIndex({device_id: 1, timestamp: -1})

// Lihat execution plan
db.sensor_data.find({device_id: "ESP32_001"}).explain("executionStats")

// Device status dengan last_seen update
db.devices.updateOne(
  {device_id: "ESP32_001"},
  {$set: {last_seen: new Date()}}
)

// Find devices yang tidak aktif (tidak ada data > 5 menit)
db.devices.aggregate([
  {$lookup: {
    from: "sensor_data",
    localField: "device_id",
    foreignField: "device_id",
    as: "recent_data",
    pipeline: [
      {$match: {timestamp: {$gte: new Date(Date.now() - 5*60*1000)}}},
      {$limit: 1}
    ]
  }},
  {$match: {"recent_data": {$size: 0}}},
  {$project: {device_id: 1, device_name: 1, last_seen: 1}}
])
```

## 5. Data Maintenance

### 5.1 Cleanup Commands

```javascript
// Delete data older than 30 days
db.sensor_data.deleteMany({
  timestamp: {$lt: new Date(Date.now() - 30*24*60*60*1000)}
})

// Archive old data to separate collection
db.sensor_data.aggregate([
  {$match: {timestamp: {$lt: new Date(Date.now() - 7*24*60*60*1000)}}},
  {$out: "sensor_data_archive"}
])

// Delete archived data from main collection
db.sensor_data.deleteMany({
  timestamp: {$lt: new Date(Date.now() - 7*24*60*60*1000)}
})
```

### 5.2 Backup Commands

```bash
# Backup database
docker exec mongodb-iot mongodump --db iot_db --out /data/backup

# Restore database
docker exec mongodb-iot mongorestore --db iot_db /data/backup/iot_db
```

## 6. Monitoring & Web Interface

### 6.1 Akses Mongo Express

Buka browser dan akses `http://localhost:8081` untuk interface web MongoDB.

**Kredensial Login Mongo Express:**
- **Username:** `admin`
- **Password:** `password123`

Setelah login, Anda akan melihat:
- Database `iot_db` dengan collections: `devices`, `sensor_data`, `alerts`
- Interface untuk browse dan query data secara visual
- Tools untuk manage database dan collections

**Tips:**
- Klik pada database `iot_db` untuk melihat collections
- Klik pada collection untuk melihat data dalam format JSON
- Gunakan fitur "View" untuk melihat data dalam format tabel

### 6.2 Monitoring Queries

```javascript
// Database stats
db.stats()

// Collection stats
db.sensor_data.stats()

// Current operations
db.currentOp()

// Server status
db.serverStatus()
```

## 7. Tips & Best Practices

1. **Indexing**: Selalu buat index pada field yang sering di-query
2. **TTL Collections**: Gunakan TTL index untuk auto-delete data lama
3. **Sharding**: Pertimbangkan sharding untuk data yang sangat besar
4. **Aggregation Pipeline**: Gunakan untuk analisis data kompleks
5. **Connection Pooling**: Gunakan connection pooling untuk aplikasi production

### Quick Reference Commands

```javascript
// Essential MongoDB Shell Commands
show dbs                           // List all databases
use database_name                  // Switch to database
show collections                   // List collections in current database
db.collection.find().limit(5)     // Show first 5 documents
db.collection.countDocuments()     // Count documents
db.collection.drop()              // Delete collection
db.dropDatabase()                 // Delete current database

// Data Types and Queries
db.collection.find({field: "value"})                    // Exact match
db.collection.find({number_field: {$gt: 10}})          // Greater than
db.collection.find({array_field: {$in: ["val1", "val2"]}}) // In array
db.collection.find({}, {field1: 1, field2: 1})         // Projection

// Useful Aggregation Operators
$match, $group, $sort, $limit, $project, $lookup, $unwind
```

## 8. Penugasan Praktik

### Task 1: Extend IoT Data Generator

**Instruksi:**
1. Modifikasi script `iot_data_generator.py` untuk menambahkan 2 sensor baru:
   - **Soil Moisture Sensor** (device_id: ESP32_004)
     - Data: soil_moisture (0-100%), soil_temperature (15-30°C), ph_level (5.5-8.0)
     - Location: "Greenhouse"
   - **Air Quality Sensor** (device_id: ESP32_005)
     - Data: pm2_5 (0-500 µg/m³), pm10 (0-500 µg/m³), co2_level (400-5000 ppm)
     - Location: "Office"

2. Tambahkan 2 device baru ke init-mongo.js
3. Generate data selama minimal 5 menit
4. Lakukan basic queries untuk semua sensor

### Task 2: MongoDB Queries Practice

**Lakukan queries berikut dan screenshot hasilnya:**

1. Count total documents di setiap collection
2. Find semua devices dengan status 'active'
3. Aggregate rata-rata temperature, motion events, dan light intensity
4. Find data dalam 1 jam terakhir
5. Count alerts berdasarkan severity level
6. Find top 5 highest temperature readings
7. Aggregate data per device_id dengan count
8. Find motion detection events
9. Check devices yang memiliki battery_level < 70%
10. Create dan test custom index untuk performance

**Deliverable:**
- Modified iot_data_generator.py
- Screenshot hasil generate data (minimal 1000 records)
- 10 screenshot contoh queries dengan hasil outputnya
- Analisis sederhana tentang data yang dihasilkan (dalam bentuk document/comment)



## Troubleshooting

### Docker Issues
```bash
# Restart containers
docker-compose restart

# View logs
docker-compose logs -f mongodb

# Connect to container
docker exec -it mongodb-iot bash

# Check MongoDB process
docker exec mongodb-iot ps aux | grep mongo
```

### OrbStack Issues
```bash
# Check OrbStack status
orb status

# Restart OrbStack if needed
orb restart

# For OrbStack users, if docker command not found:
which docker
```

### Common Connection Issues
```bash
# Test MongoDB connection
docker exec -it mongodb-iot mongosh --eval "db.adminCommand('ping')"

# Check if ports are accessible
netstat -an | grep 27017
netstat -an | grep 8081
```

## Cleanup

```bash
# Stop dan remove containers
docker-compose down

# Remove volumes (hati-hati, akan menghapus data!)
docker-compose down -v

# Remove images
docker rmi mongo:7.0 mongo-express:1.0.0
```
