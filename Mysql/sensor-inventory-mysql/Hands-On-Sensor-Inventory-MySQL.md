Hands-On: Sensor Inventory MySQL dengan Docker

##  Langkah-Langkah Praktik

### 1Persiapan Environment
```bash
# Pastikan Docker sudah terinstall dan berjalan
docker --version
docker-compose --version

# Buat direktori proyek
mkdir sensor-inventory-mysql
cd sensor-inventory-mysql
mkdir init
```

### 2. Membuat File Konfigurasi

**File 1: `docker-compose.yml`**
```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    container_name: sensor_inventory_mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: inventory
      MYSQL_USER: admin
      MYSQL_PASSWORD: admin123
    volumes:
      - ./init:/docker-entrypoint-initdb.d
    ports:
      - "3306:3306"

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: sensor_inventory_phpmyadmin
    restart: always
    ports:
      - "8080:80"
    environment:
      PMA_HOST: db
      MYSQL_ROOT_PASSWORD: root123
```

**File 2: `init/init.sql`**
```sql
-- Gunakan database 'inventory'
USE inventory;

-- Buat tabel Lokasi
CREATE TABLE lokasi (
    id_lokasi INT AUTO_INCREMENT PRIMARY KEY,
    nama_lokasi VARCHAR(100) NOT NULL,
    koordinat VARCHAR(50)
);

-- Buat tabel Sensor
CREATE TABLE sensor (
    id_sensor INT AUTO_INCREMENT PRIMARY KEY,
    tipe VARCHAR(50),
    status VARCHAR(20),
    tanggal_pasang DATE,
    id_lokasi INT,
    FOREIGN KEY (id_lokasi) REFERENCES lokasi(id_lokasi)
);

-- Tambahkan data awal
INSERT INTO lokasi (nama_lokasi, koordinat) VALUES 
('Gudang Utama', '-7.9829, 112.6303'),
('Lab Sensor', '-7.9832, 112.6320');

INSERT INTO sensor (tipe, status, tanggal_pasang, id_lokasi) VALUES 
('Suhu', 'Aktif', '2023-01-12', 1),
('Kelembaban', 'Tidak Aktif', '2023-03-20', 2),
('Gerak', 'Aktif', '2023-06-05', 1);
```

### 3.  Menjalankan Container
```bash
# Jalankan Docker Compose
docker compose up -d

# Verifikasi container berjalan
docker ps

# Cek logs jika ada masalah
docker compose logs
```

### 4. 🌐 Akses phpMyAdmin
1. Buka browser
2. Kunjungi: http://localhost:8080
3. Login dengan:
   - **Username**: admin
   - **Password**: admin123
   - **Server**: db

### 5. 🔍 Eksplorasi Database

**A. Melihat Struktur Database:**
```sql
-- Tampilkan semua tabel
SHOW TABLES;

-- Lihat struktur tabel lokasi
DESCRIBE lokasi;

-- Lihat struktur tabel sensor
DESCRIBE sensor;
```

**B. Query Data Existing:**
```sql
-- Tampilkan semua lokasi
SELECT * FROM lokasi;

-- Tampilkan semua sensor
SELECT * FROM sensor;

-- Join data sensor dengan lokasi
SELECT 
    s.id_sensor,
    s.tipe,
    s.status,
    s.tanggal_pasang,
    l.nama_lokasi,
    l.koordinat
FROM sensor s
JOIN lokasi l ON s.id_lokasi = l.id_lokasi;
```

### 6.  Hands-On Praktik

**A. Tambah Data Baru:**
```sql
-- Tambah lokasi baru
INSERT INTO lokasi (nama_lokasi, koordinat) VALUES 
('Ruang Server', '-7.9825, 112.6315'),
('Area Parkir', '-7.9835, 112.6325');

-- Tambah sensor baru
INSERT INTO sensor (tipe, status, tanggal_pasang, id_lokasi) VALUES 
('Cahaya', 'Aktif', '2024-01-15', 3),
('Tekanan', 'Maintenance', '2024-02-20', 4),
('pH', 'Aktif', '2024-03-10', 1);
```

**B. Update Data:**
```sql
-- Update status sensor
UPDATE sensor 
SET status = 'Maintenance' 
WHERE id_sensor = 1;

-- Update koordinat lokasi
UPDATE lokasi 
SET koordinat = '-7.9830, 112.6310' 
WHERE id_lokasi = 1;
```

**C. Query Kompleks:**
```sql
-- Hitung jumlah sensor per lokasi
SELECT 
    l.nama_lokasi,
    COUNT(s.id_sensor) as jumlah_sensor
FROM lokasi l
LEFT JOIN sensor s ON l.id_lokasi = s.id_lokasi
GROUP BY l.id_lokasi, l.nama_lokasi;

-- Cari sensor yang tidak aktif
SELECT 
    s.tipe,
    s.status,
    l.nama_lokasi
FROM sensor s
JOIN lokasi l ON s.id_lokasi = l.id_lokasi
WHERE s.status != 'Aktif';

-- Sensor yang dipasang dalam 6 bulan terakhir
SELECT 
    s.tipe,
    s.tanggal_pasang,
    l.nama_lokasi
FROM sensor s
JOIN lokasi l ON s.id_lokasi = l.id_lokasi
WHERE s.tanggal_pasang >= DATE_SUB(NOW(), INTERVAL 6 MONTH);
```

### 7.  Tugas Praktik


1. Tambah 2 lokasi baru
2. Tambah 3 sensor baru
3. Update status salah satu sensor
4. Query semua sensor aktif

1. Buat view untuk gabungan sensor dan lokasi
2. Hitung total sensor per status
3. Cari lokasi yang belum ada sensornya
4. Update tanggal pasang semua sensor suhu



### 8.  Manajemen Container

```bash
# Stop container
docker compose down

# Restart container
docker compose restart

# Lihat logs
docker compose logs -f

# Akses MySQL CLI langsung
docker exec -it sensor_inventory_mysql mysql -u admin -p

# Backup database
docker exec sensor_inventory_mysql mysqldump -u admin -p inventory > backup.sql

# Restore database
docker exec -i sensor_inventory_mysql mysql -u admin -p inventory < backup.sql
```

### 9.  Validasi Hasil

**Checklist:**
- [ ] Container MySQL berjalan di port 3306
- [ ] Container phpMyAdmin berjalan di port 8080
- [ ] Database `inventory` terbuat
- [ ] Tabel `lokasi` dan `sensor` ada dengan data
- [ ] Bisa login ke phpMyAdmin
- [ ] Query JOIN berfungsi dengan baik
- [ ] Foreign key constraint bekerja

### 10.  Troubleshooting

**Masalah Umum:**
- Port 3306 sudah digunakan → Ganti port di docker-compose.yml
- Container tidak start → Cek Docker daemon
- phpMyAdmin tidak bisa connect → Verifikasi environment variables
- Data tidak muncul → Cek file init.sql dan volume mapping

**Log Debug:**
```bash
# Cek status container
docker ps -a

# Lihat log MySQL
docker logs sensor_inventory_mysql

# Lihat log phpMyAdmin
docker logs sensor_inventory_phpmyadmin
```

### 11.  Catatan Penting

**Kredensial Database:**
- Host: localhost:3306
- Database: inventory
- Username: admin
- Password: admin123
- Root Password: root123

**URL Akses:**
- phpMyAdmin: http://localhost:8080
- MySQL Direct: localhost:3306

**Struktur Tabel:**

**Tabel Lokasi:**
- id_lokasi (INT, Primary Key, Auto Increment)
- nama_lokasi (VARCHAR(100), NOT NULL)
- koordinat (VARCHAR(50))

**Tabel Sensor:**
- id_sensor (INT, Primary Key, Auto Increment)
- tipe (VARCHAR(50))
- status (VARCHAR(20))
- tanggal_pasang (DATE)
- id_lokasi (INT, Foreign Key)


Selamat Mencoba!
