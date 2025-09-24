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
