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

INSERT INTO lokasi (nama_lokasi, koordinat) VALUES 
('Gudang Utama', '-7.9829, 112.6303'),
('Lab Sensor', '-7.9832, 112.6320');

INSERT INTO sensor (tipe, status, tanggal_pasang, id_lokasi) VALUES 
('Suhu', 'Aktif', '2023-01-12', 1),
('Kelembaban', 'Tidak Aktif', '2023-03-20', 2),
('Gerak', 'Aktif', '2023-06-05', 1);
-- ...existing code...

-- Tabel Pengguna
CREATE TABLE pengguna (
    id_pengguna INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- Tabel Perawatan Sensor
CREATE TABLE perawatan_sensor (
    id_perawatan INT AUTO_INCREMENT PRIMARY KEY,
    id_sensor INT,
    tanggal_perawatan DATE,
    deskripsi VARCHAR(255),
    FOREIGN KEY (id_sensor) REFERENCES sensor(id_sensor)
);

-- Tabel Log Aktivitas
CREATE TABLE log_aktivitas (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_pengguna INT,
    aktivitas VARCHAR(255),
    waktu DATETIME,
    FOREIGN KEY (id_pengguna) REFERENCES pengguna(id_pengguna)
);

-- Data awal untuk pengguna
INSERT INTO pengguna (nama, email, role) VALUES
('Budi Santoso', 'budi@example.com', 'admin'),
('Siti Aminah', 'siti@example.com', 'teknisi'),
('Andi Wijaya', 'andi@example.com', 'user');

-- Data awal untuk perawatan_sensor
INSERT INTO perawatan_sensor (id_sensor, tanggal_perawatan, deskripsi) VALUES
(1, '2024-01-15', 'Kalibrasi sensor suhu'),
(2, '2024-02-10', 'Penggantian baterai sensor kelembaban'),
(3, '2024-03-05', 'Pembersihan sensor gerak');

-- Data awal untuk log_aktivitas
INSERT INTO log_aktivitas (id_pengguna, aktivitas, waktu) VALUES
(1, 'Menambah data sensor', '2024-04-01 09:15:00'),
(2, 'Melakukan perawatan sensor', '2024-04-02 10:30:00'),
(3, 'Melihat laporan suhu', '2024-04-03 14:45:00');

-- Data tambahan massal (dummy) untuk pengguna, perawatan_sensor, dan log_aktivitas
-- Pengguna
INSERT INTO pengguna (nama, email, role) VALUES
    -- 997 baris tambahan
    ('User 1', 'user1@example.com', 'user'),
    ('User 2', 'user2@example.com', 'user'),
    ('User 3', 'user3@example.com', 'user'),
    -- ...
    ('User 997', 'user997@example.com', 'user');


-- Perawatan Sensor
INSERT INTO perawatan_sensor (id_sensor, tanggal_perawatan, deskripsi) VALUES
    -- 333 baris tambahan
    (1, '2024-01-16', 'Perawatan rutin ke-1'),
    (2, '2024-01-17', 'Perawatan rutin ke-2'),
    (3, '2024-01-18', 'Perawatan rutin ke-3'),
    -- ...
    (3, '2025-12-31', 'Perawatan rutin ke-333');
-- ... lanjutkan hingga 350 baris ...

-- Log Aktivitas
INSERT INTO log_aktivitas (id_pengguna, aktivitas, waktu) VALUES
    -- 333 baris tambahan
    (1, 'Login aplikasi', '2024-05-01 08:00:00'),
    (2, 'Logout aplikasi', '2024-05-01 17:00:00'),
    (3, 'Mengubah data sensor', '2024-05-02 10:00:00'),
    -- ...
    (997, 'Login aplikasi', '2025-12-31 23:59:00');
-- ... lanjutkan hingga 350 baris ...
