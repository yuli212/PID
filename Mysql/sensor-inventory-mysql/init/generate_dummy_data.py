# Script Python untuk generate data dummy SQL
import random
from datetime import datetime, timedelta

# Pengguna
with open('pengguna_dummy.sql', 'w') as f:
    f.write("INSERT INTO pengguna (nama, email, role) VALUES\n")
    for i in range(1, 998):
        nama = f'User {i}'
        email = f'user{i}@example.com'
        role = random.choice(['user', 'teknisi', 'admin'])
        koma = ',' if i < 997 else ';'
        f.write(f"('{nama}', '{email}', '{role}')" + koma + "\n")

# Perawatan Sensor
with open('perawatan_sensor_dummy.sql', 'w') as f:
    f.write("INSERT INTO perawatan_sensor (id_sensor, tanggal_perawatan, deskripsi) VALUES\n")
    base_date = datetime(2024, 1, 16)
    for i in range(1, 334):
        id_sensor = random.randint(1, 3)
        tanggal = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
        deskripsi = f'Perawatan rutin ke-{i}'
        koma = ',' if i < 333 else ';'
        f.write(f"({id_sensor}, '{tanggal}', '{deskripsi}')" + koma + "\n")

# Log Aktivitas
with open('log_aktivitas_dummy.sql', 'w') as f:
    f.write("INSERT INTO log_aktivitas (id_pengguna, aktivitas, waktu) VALUES\n")
    base_time = datetime(2024, 5, 1, 8, 0, 0)
    aktivitas_list = ['Login aplikasi', 'Logout aplikasi', 'Mengubah data sensor', 'Melihat laporan', 'Menambah data sensor', 'Melakukan perawatan sensor', 'Melihat laporan suhu']
    for i in range(1, 334):
        id_pengguna = random.randint(1, 997)
        aktivitas = random.choice(aktivitas_list)
        waktu = (base_time + timedelta(minutes=i*10)).strftime('%Y-%m-%d %H:%M:%S')
        koma = ',' if i < 333 else ';'
        f.write(f"({id_pengguna}, '{aktivitas}', '{waktu}')" + koma + "\n")
