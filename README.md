# Data Engineering Modules Collection

## 📋 Deskripsi

Repositori ini berisi kumpulan modul praktikum dan hands-on untuk pembelajaran Data Engineering, meliputi teknologi-teknologi utama yang digunakan dalam ekosistem data modern. Setiap modul dirancang untuk memberikan pemahaman praktis tentang implementasi solusi data engineering.

## 🏗️ Struktur Proyek

```
PID/
├── airflow/                    # Apache Airflow - Workflow Orchestration
│   ├── dags/                   # Data pipeline definitions
│   ├── data/                   # Sample datasets
│   ├── scripts/                # Utility scripts
│   └── docker-compose.yml      # Containerized setup
├── mongo/                      # MongoDB - Document Database
│   ├── mongodb-iot-handson/    # IoT data handling with MongoDB
│   └── handson-mongo.md        # MongoDB tutorial
├── Mysql/                      # MySQL - Relational Database
│   └── sensor-inventory-mysql/ # Sensor inventory management
└── README.md                   # Dokumentasi utama
```

## 🚀 Modul yang Tersedia

### 1. Apache Airflow - Data Pipeline Orchestration
**Lokasi:** `/airflow/`

Modul ini mengcover:
- ✅ ETL (Extract, Transform, Load) Pipelines
- ✅ ELT (Extract, Load, Transform) Pipelines
- ✅ IoT data processing workflows
- ✅ Automated data pipeline scheduling
- ✅ Data quality checks and monitoring

**Fitur Utama:**
- Docker-based Airflow setup
- PostgreSQL integration
- Sample IoT sensor data processing
- Real-time data pipeline monitoring

**Cara Menjalankan:**
```bash
cd airflow/
./start.sh
```

### 2. MongoDB - NoSQL Document Database
**Lokasi:** `/mongo/`

Modul ini mengcover:
- ✅ Document-based data modeling
- ✅ IoT data ingestion dan storage
- ✅ Aggregation pipelines
- ✅ Real-time data processing
- ✅ Scalable data architecture

**Fitur Utama:**
- MongoDB containerized setup
- IoT data generator
- Advanced querying techniques
- Data aggregation dan analytics

**Cara Menjalankan:**
```bash
cd mongo/mongodb-iot-handson/
docker-compose up -d
```

### 3. MySQL - Relational Database Management
**Lokasi:** `/Mysql/`

Modul ini mengcover:
- ✅ Relational data modeling
- ✅ Sensor inventory management
- ✅ Complex SQL queries
- ✅ Database optimization
- ✅ Data aggregation dan reporting

**Fitur Utama:**
- MySQL containerized setup
- Sensor inventory system
- Complex query examples
- Performance optimization techniques

**Cara Menjalankan:**
```bash
cd Mysql/sensor-inventory-mysql/
docker-compose up -d
```

## 🛠️ Prerequisites

Sebelum menjalankan modul-modul ini, pastikan Anda telah menginstall:

- **Docker & Docker Compose** (versi terbaru)
- **Python 3.8+**
- **Git** (untuk cloning repository)
- **Text Editor/IDE** (VS Code, PyCharm, dll)

## 📚 Panduan Pembelajaran

### Tahap 1: Pemahaman Dasar
1. **Database Fundamentals**
   - Mulai dengan modul MySQL untuk memahami konsep relational database
   - Pelajari basic SQL queries dan data modeling

2. **NoSQL Concepts**
   - Lanjutkan ke modul MongoDB untuk memahami document-based storage
   - Bandingkan perbedaan dengan relational approach

### Tahap 2: Data Pipeline Development
3. **Workflow Orchestration**
   - Gunakan modul Airflow untuk membangun data pipelines
   - Implementasikan ETL/ELT processes

### Tahap 3: Integration & Advanced Topics
4. **End-to-End Projects**
   - Kombinasikan ketiga teknologi
   - Buat complete data engineering solutions

## 🔧 Setup Environment

### Quick Start
```bash
# Clone repository (jika diperlukan)
git clone <repository-url>
cd PID

# Setup setiap modul sesuai kebutuhan
# Lihat README di masing-masing folder untuk detail
```

### Environment Variables
Beberapa modul memerlukan environment variables:
```bash
# Airflow
export AIRFLOW_UID=1000

# Database credentials (sesuaikan dengan setup Anda)
export DB_USER=your_username
export DB_PASSWORD=your_password
```

## 📖 Learning Resources

### Documentation Links
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

### Recommended Learning Path
1. **Week 1-2:** MySQL fundamentals dan basic queries
2. **Week 3-4:** MongoDB concepts dan document modeling
3. **Week 5-6:** Airflow setup dan basic DAG creation
4. **Week 7-8:** Advanced pipeline development
5. **Week 9-10:** Integration project

## 🎯 Use Cases

### Real-World Applications
- **IoT Data Processing:** Sensor data ingestion, transformation, dan analytics
- **E-commerce Analytics:** Customer behavior analysis dan reporting
- **Financial Data Pipelines:** Transaction processing dan fraud detection
- **Healthcare Data Management:** Patient data integration dan reporting

## 🤝 Contributing

Jika Anda ingin berkontribusi pada modul-modul ini:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 Notes & Tips

### Best Practices
- Selalu backup data sebelum menjalankan scripts
- Gunakan virtual environment untuk Python dependencies
- Monitor resource usage saat menjalankan multiple containers
- Dokumentasikan setiap perubahan yang Anda buat

### Troubleshooting
- **Docker issues:** Pastikan Docker daemon berjalan
- **Port conflicts:** Check apakah port sudah digunakan aplikasi lain
- **Memory issues:** Sesuaikan memory allocation untuk Docker

## 📞 Support

Jika Anda mengalami kesulitan:
1. Check dokumentasi di folder masing-masing modul
2. Review log files untuk error messages
3. Gunakan Docker logs untuk debugging: `docker-compose logs`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Happy Learning! 🚀**

*Dibuat untuk keperluan pembelajaran Data Engineering - Semoga bermanfaat!*
