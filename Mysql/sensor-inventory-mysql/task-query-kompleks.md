
# 🏆 TASK: Query Kompleks Data Historis Sensor Suhu

## 📋 Penugasan

Kerjakan dan dokumentasikan hasil query berikut pada database MySQL yang sudah terisi data dummy:

1. Jalankan setiap query di bawah ini, simpan hasilnya (screenshot/tabel hasil).
2. Analisis hasil query: apa insight atau temuan yang didapat dari data?
3. Jika ada error, dokumentasikan dan jelaskan cara mengatasinya.
4. Modifikasi minimal 1 query agar menghasilkan insight tambahan (misal: filter waktu, lokasi tertentu, dsb).
5. Buat ringkasan singkat (3-5 kalimat) tentang temuan utama dari seluruh query.

> **Catatan:**
> - Penugasan ini dapat dikerjakan secara individu/kelompok.
> - Sertakan file .md ini beserta hasil query dan analisis Anda saat submit.


## 1. Analisis Multi-Tabel
Tampilkan daftar 20 aktivitas terakhir (dari `log_aktivitas`) yang dilakukan oleh pengguna dengan role "teknisi", beserta nama pengguna dan deskripsi aktivitas.

```sql
SELECT l.id_log, p.nama, l.aktivitas, l.waktu
FROM log_aktivitas l
JOIN pengguna p ON l.id_pengguna = p.id_pengguna
WHERE p.role = 'teknisi'
ORDER BY l.waktu DESC
LIMIT 20;
```

---

## 2. Agregasi & Join
Hitung rata-rata suhu harian untuk setiap lokasi, dan tampilkan bersama nama lokasi serta jumlah aktivitas perawatan sensor yang dilakukan pada hari yang sama.

```sql
SELECT l.nama_lokasi, DATE(h.waktu_tercatat) AS tanggal,
       ROUND(AVG(h.suhu_celsius),2) AS rata_suhu,
       COUNT(DISTINCT p.id_perawatan) AS jumlah_perawatan
FROM historis_suhu_sensor h
JOIN sensor s ON h.id_sensor = s.id_sensor
JOIN lokasi l ON s.id_lokasi = l.id_lokasi
LEFT JOIN perawatan_sensor p ON p.id_sensor = s.id_sensor AND p.tanggal_perawatan = DATE(h.waktu_tercatat)
GROUP BY l.nama_lokasi, tanggal;
```

---

## 3. Deteksi Anomali Lintas Tabel
Tampilkan semua pencatatan suhu > 38°C, beserta nama lokasi, nama pengguna yang terakhir melakukan perawatan pada sensor tersebut, dan tanggal perawatan terakhir.

```sql
SELECT h.*, l.nama_lokasi, p2.nama AS teknisi_terakhir, p1.tanggal_perawatan
FROM historis_suhu_sensor h
JOIN sensor s ON h.id_sensor = s.id_sensor
JOIN lokasi l ON s.id_lokasi = l.id_lokasi
LEFT JOIN (
    SELECT ps.id_sensor, MAX(ps.tanggal_perawatan) AS tanggal_perawatan
    FROM perawatan_sensor ps
    GROUP BY ps.id_sensor
) p1 ON h.id_sensor = p1.id_sensor
LEFT JOIN perawatan_sensor ps2 ON p1.id_sensor = ps2.id_sensor AND p1.tanggal_perawatan = ps2.tanggal_perawatan
LEFT JOIN pengguna p2 ON ps2.id_perawatan IS NOT NULL AND p2.role = 'teknisi'
WHERE h.suhu_celsius > 38;
```

---

## 4. Statistik Sensor
Tampilkan 5 sensor dengan jumlah perawatan terbanyak, beserta tipe sensor, lokasi, dan total aktivitas log terkait sensor tersebut.

```sql
SELECT s.id_sensor, s.tipe, l.nama_lokasi,
       COUNT(DISTINCT p.id_perawatan) AS total_perawatan,
       (
         SELECT COUNT(*) FROM log_aktivitas la
         WHERE la.aktivitas LIKE CONCAT('%', s.id_sensor, '%')
       ) AS total_log
FROM sensor s
JOIN lokasi l ON s.id_lokasi = l.id_lokasi
LEFT JOIN perawatan_sensor p ON s.id_sensor = p.id_sensor
GROUP BY s.id_sensor, s.tipe, l.nama_lokasi
ORDER BY total_perawatan DESC
LIMIT 5;
```

---

## 5. Tren Mingguan
Tampilkan tren rata-rata suhu mingguan per lokasi selama 6 bulan terakhir, urutkan dari lokasi dengan rata-rata suhu tertinggi.

```sql
SELECT l.nama_lokasi, YEAR(h.waktu_tercatat) AS tahun, WEEK(h.waktu_tercatat) AS minggu,
       ROUND(AVG(h.suhu_celsius),2) AS rata_suhu
FROM historis_suhu_sensor h
JOIN sensor s ON h.id_sensor = s.id_sensor
JOIN lokasi l ON s.id_lokasi = l.id_lokasi
WHERE h.waktu_tercatat >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY l.nama_lokasi, tahun, minggu
ORDER BY rata_suhu DESC;
```

---

> **Catatan:**
> - Pastikan semua tabel sudah terisi data dummy yang cukup.
> - Query dapat disesuaikan dengan kebutuhan analisis lebih lanjut.
