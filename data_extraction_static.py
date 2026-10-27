import pandas as pd
import sqlite3
from pathlib import Path

imu_data = pd.read_csv("imu.csv")
odom_data = pd.read_csv("odom.csv")
print(imu_data.head())
print(odom_data.head())

print(imu_data["az"].mean())
print(imu_data["ax"].var())
print(imu_data["ay"].var())
print(imu_data["az"].var())

db_path = Path(r"C:\Users\stratklar\Downloads\sensordata\my_sensor_data_0.db3")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT * FROM topics")
#cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#tables = cursor.fetchall()

#print("Tables:", tables)

for row in cursor.fetchall():
    print(row)

conn.close()

angle_increment = 0.015591030940413475

def calculate_volume(timestamp, x1, x2, y1, y2):
    lidar_rows = [[]]#depending on y1, y2
    a = 42 #determined by computer vision
    b = 42
    directions_count = (b - a) / angle_increment
    volume = 0
    depth_reference = 42
    for i in range(directions_count):
        for lidar_row in lidar_rows:
            if lidar_row[a + i] > depth_reference:
                volume = volume + (lidar_row[a + i] - depth_reference) * angle_increment #*lidar_row_distance
