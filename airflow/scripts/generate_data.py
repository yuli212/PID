#!/usr/bin/env python3
"""
Data Generator untuk Praktikum Airflow ETL vs ELT
Menggenerate data sensor IoT yang lebih besar untuk testing scalability
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import argparse
import os

def generate_sensors(num_sensors):
    """Generate sensor metadata"""
    locations = [
        "Room101", "Room102", "Room201", "Room202", "Room301", "Room302",
        "Lobby", "Kitchen", "Conference_Room", "Server_Room", "Storage",
        "Meeting_Room_A", "Meeting_Room_B", "Executive_Suite", "Break_Room",
        "IT_Department", "HR_Department", "Finance_Department", "Reception",
        "Archive_Room", "Training_Room", "Cafeteria", "Library", "Lab_A", "Lab_B"
    ]
    
    sensors = []
    for i in range(1, num_sensors + 1):
        location = np.random.choice(locations)
        sensors.append({
            'sensor_id': i,
            'location': location
        })
    
    return pd.DataFrame(sensors)

def generate_readings(sensors_df, num_days, readings_per_hour):
    """Generate sensor readings time series data"""
    readings = []
    reading_id = 1
    
    # Base temperature by location (realistic ranges)
    location_base_temps = {
        'Server_Room': 18.0,  # Server rooms are cooler
        'Kitchen': 26.0,      # Kitchens are warmer
        'Conference_Room': 22.0,
        'Lobby': 21.0,
        'Storage': 20.0,
    }
    
    start_date = datetime(2025, 9, 1)
    
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        
        for hour in range(24):
            for reading_num in range(readings_per_hour):
                # Random time within the hour
                minute = np.random.randint(0, 60)
                second = np.random.randint(0, 60)
                timestamp = current_date.replace(hour=hour, minute=minute, second=second)
                
                # Select random sensor
                sensor_row = sensors_df.sample(1).iloc[0]
                sensor_id = sensor_row['sensor_id']
                location = sensor_row['location']
                
                # Generate temperature based on location and time
                base_temp = location_base_temps.get(location, 22.0)
                
                # Add daily and hourly patterns
                daily_variation = 2 * np.sin((hour - 6) * np.pi / 12)  # Peak at 2 PM
                random_noise = np.random.normal(0, 0.5)
                
                # Weekend vs weekday differences
                if timestamp.weekday() >= 5:  # Weekend
                    base_temp += np.random.normal(-1, 0.3)
                
                temperature = base_temp + daily_variation + random_noise
                temperature = round(temperature, 1)
                
                readings.append({
                    'reading_id': reading_id,
                    'sensor_id': sensor_id,
                    'temperature': temperature,
                    'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })
                
                reading_id += 1
    
    return pd.DataFrame(readings)

def generate_weather_data(num_days):
    """Generate weather data for advanced experiments"""
    weather_data = []
    start_date = datetime(2025, 9, 1)
    
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        
        # Generate realistic weather patterns
        base_temp = 25 + 5 * np.sin((day - 80) * 2 * np.pi / 365)  # Seasonal variation
        daily_high = base_temp + np.random.normal(3, 1)
        daily_low = base_temp + np.random.normal(-3, 1)
        humidity = max(30, min(95, 60 + np.random.normal(0, 15)))
        
        # Simple weather conditions
        temp_diff = daily_high - daily_low
        if temp_diff > 8 and humidity > 70:
            condition = 'Rainy'
        elif daily_high > 30:
            condition = 'Hot'
        elif daily_low < 15:
            condition = 'Cold'
        else:
            condition = 'Normal'
        
        weather_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'high_temp': round(daily_high, 1),
            'low_temp': round(daily_low, 1),
            'humidity': round(humidity, 1),
            'condition': condition
        })
    
    return pd.DataFrame(weather_data)

def main():
    parser = argparse.ArgumentParser(description='Generate IoT sensor data')
    parser.add_argument('--sensors', type=int, default=50, help='Number of sensors')
    parser.add_argument('--days', type=int, default=7, help='Number of days')
    parser.add_argument('--readings-per-hour', type=int, default=2, help='Readings per hour per sensor')
    parser.add_argument('--output-dir', default='../data', help='Output directory')
    parser.add_argument('--generate-weather', action='store_true', help='Generate weather data')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    print(f"🏭 Generating data for {args.sensors} sensors over {args.days} days...")
    print(f"📊 Expected readings: {args.sensors * args.days * 24 * args.readings_per_hour:,}")
    
    # Generate sensors
    print("📡 Generating sensors...")
    sensors_df = generate_sensors(args.sensors)
    sensors_df.to_csv(f"{args.output_dir}/sensors.csv", index=False)
    print(f"✅ Generated {len(sensors_df)} sensors")
    
    # Generate readings
    print("📈 Generating readings...")
    readings_df = generate_readings(sensors_df, args.days, args.readings_per_hour)
    readings_df.to_csv(f"{args.output_dir}/readings.csv", index=False)
    print(f"✅ Generated {len(readings_df):,} readings")
    
    # Generate weather data if requested
    if args.generate_weather:
        print("🌤️  Generating weather data...")
        weather_df = generate_weather_data(args.days)
        weather_df.to_csv(f"{args.output_dir}/weather.csv", index=False)
        print(f"✅ Generated {len(weather_df)} weather records")
    
    # Summary
    print("\n📋 Data Summary:")
    print(f"   Sensors: {len(sensors_df)}")
    print(f"   Readings: {len(readings_df):,}")
    print(f"   Date range: {readings_df['timestamp'].min()} to {readings_df['timestamp'].max()}")
    print(f"   Locations: {sensors_df['location'].nunique()}")
    print(f"   Avg readings per sensor: {len(readings_df) / len(sensors_df):.1f}")
    
    # Temperature stats
    print(f"\n🌡️  Temperature Statistics:")
    print(f"   Min: {readings_df['temperature'].min()}°C")
    print(f"   Max: {readings_df['temperature'].max()}°C")  
    print(f"   Mean: {readings_df['temperature'].mean():.1f}°C")
    print(f"   Std: {readings_df['temperature'].std():.1f}°C")
    
    print("\n🎉 Data generation completed!")

if __name__ == "__main__":
    main()