import sqlite3

import geopandas as gpd
from shapely.geometry import Point

from typing import List
import os

from endpoint import filterState, valueAssignment

from pyproj import Transformer
import math

print("the start works")
conn = sqlite3.connect("potholes.db")
cursor = conn.cursor()

#cursor.execute(""" DELETE FROM potholes""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS potholes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL,
    longitude REAL,
    confidence REAL,
    severity TEXT,
    timestamp TEXT
)
""")

class polygon_point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class polygon_area:
    def __init__(self, vertices: List[polygon_point]):
        self.vertices = vertices

    def surface_area(self):
        if len(self.vertices) < 3:
            raise ValueError("A polygon must have at least 3 vertices.")

        # Ensure all vertices are numeric
        for v in self.vertices:
            if not (isinstance(v, tuple) and len(v) == 2 and all(isinstance(coord, (int, float)) for coord in v)):
               raise TypeError("Each vertex must be a tuple of two numbers (x, y).")

        # Shoelace formula
        area = 0.0
        n = len(self.vertices)
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]  # Wrap around to first vertex
        area += x1 * y2 - x2 * y1

        return abs(area) / 2.0
"""
class pothole:

    def __init__(self, vertices: List[polygon_point], confidence, severity, max_depth, avg_depth, timestamp):
        self.polygon_area = polygon_area(vertices) #list of polygon points
        self.surface_area = self.polygon_area.surface_area()
        self.confidence = confidence
        self.severity = severity
        self.max_depth = max_depth
        self.avg_depth = avg_depth
        self.volume = self.surface_area * self.avg_depth
        self.timestamp = timestamp
"""

class pothole:

    def __init__(self, latitude, longitude, confidence, severity):
        self.latitude = latitude
        self.longitude = longitude
        self.confidence = confidence
        self.severity = severity

testPh1 = pothole(51.53, 7.5, 0.9, "low")
testPh2 = pothole(51.33, 7.5, 0.9, "very high")
testPh3 = pothole(51.5, 7.3, 0.7, "medium")
testPh4 = pothole(51.3, 7.35, 0.8, "high")
testPh5 = pothole(51.52, 7.45, 0.7, "very high")

otherGeometry = pothole(51.51, 7.468, 0.8, "high")

def insertPothole(pothole):
    
    print("function entered")

    cursor.execute("SELECT latitude, longitude FROM potholes")

    for ph in cursor.fetchall():

        print(pothole.latitude)
        print(ph[0])

        if (abs(pothole.latitude - ph[0]) < 0.01) and (abs(pothole.longitude - ph[1]) < 0.01):
            print("pothole already stored")
            return

    cursor.execute("""
    INSERT INTO potholes
    (latitude, longitude, confidence, severity, timestamp)
    VALUES (?, ?, ?, ?, datetime('now'))
    """, (pothole.latitude, pothole.longitude, pothole.confidence, pothole.severity))
    conn.commit()

    data = {
    "confidence": pothole.confidence,
    "severity": pothole.severity
    }

    gdf = gpd.GeoDataFrame(
    [data],
    geometry=[Point(pothole.latitude, pothole.longitude)],
    crs="EPSG:4326"
    )

    gdf.to_file(
    "potholes.geojson",
    driver="GeoJSON"
    )
    """
    gdf.to_file(
    "potholes.gpkg",
    driver="GPKG"
    )
    """

def insertPotholes(potholes):
    
    for pothole in potholes:
        insertPothole(pothole)

def deletePotholeById(idd):
    cursor.execute("""
        DELETE FROM potholes WHERE id = ?
        """, (idd,))
    conn.commit()

def deletePotholeByPosition(x, y):
    cursor.execute("""
        DELETE FROM potholes WHERE ABS(latitude - ?) < 0.01 AND ABS(longitude - ?) < 0.01
        """, (x, y))
    conn.commit()

def filterByLocation(latitude, longitude, radius):
    #cursor.execute("""
    #    SELECT * FROM potholes WHERE (latitude - ?) * (latitude - ?) + (longitude - ?) * (longitude - ?) <= ? * ?
    #    """, (latitude, latitude, longitude, longitude, radius, radius))
    #conn.commit()
    xUnit_squared = 0.1
    yUnit_squared = 0.1
    try:
        xUnit_squared = (111.32 * math.cos(math.radians(float(latitude))))**2
        yUnit_squared = 111.32 * 111.32
        #xUnit = 40000 * math.cos(lat1/90) / 360 yUnit = 40000 /360 return math.sqrt(((lat1 - lat2) * yUnit)^2 + ((lon1 - lon2) * xUnit)^2)
        condition = ["(latitude - ?) * (latitude - ?) * ? + (longitude - ?) * (longitude - ?) * ? <= ? * ?", 
                    [latitude, latitude, yUnit_squared, longitude, longitude, xUnit_squared, radius, radius]]
        #condition = ["(latitude - ?) * (latitude - ?) + (longitude - ?) * (longitude - ?) <= ? * ?", 
        #             [latitude, latitude, longitude, longitude, radius, radius]]
        #print((latitude - 7.5) * (latitude - 7.5) * ? + (longitude - ?) * (longitude - ?) * ?)
        return condition
    except ValueError as e:
        print("ValueError")

def filterBySeverity(severity):
    #cursor.execute("""
    #    SELECT * FROM potholes WHERE severity = ?
    #    """, (severity))
    #conn.commit()
    if(len(severity) > 0):
        query = f"(severity = ?"
        for i in range(len(severity) - 1):
            query += " OR severity = ?"
        query += ")"
        condition = [query, severity]
        return condition
    else:
        return ["",[]]

def filterByConfidence(confidence):
    #cursor.execute("""
     #   SELECT * FROM potholes WHERE confidence >= ?
      #  """, (confidence))
    #conn.commit()
    try:
        condition = ["confidence >= ?", [float(confidence)]]
        return condition
    except ValueError as e:
        print("ValueError")
    

def filterByTime(time):
    #cursor.execute("""
    #    SELECT * FROM potholes WHERE timestamp >= datetime('now', '-? days')
    #    """, (time))
    #conn.commit()
    print("reached filterByTime")
    try: 
        condition = ["timestamp >= datetime('now', ?)", [f'-{int(time)} days']]
        print(condition)
        return condition
    except ValueError as e: 
        print("ValueError")
        condition = "error"
        print(condition)
    
    

query_by_category = {
    "severity": "severity = ?",
    "confidence": "confidence >=",
    "location": "(latitude - ?) * (latitude - ?) + (longitude - ?) * (longitude - ?) <= ? * ?",
    "time": "timestamp >= datetime('now', '-? days');"
}


def filterBy(category, args):
    print(args[0])
    if category == "location":
        #try {
        return filterByLocation(args[0].value, args[1].value, args[2].value)
        #}
        #catch Exception as e {
        #    print("inappropriate list of arguments")
        #}  
    elif category == "severity":
        allowedLevels = []
        for arg in args:
            if arg.value == True:
                allowedLevels.append(arg.label)
        return filterBySeverity(allowedLevels)
    elif category == "confidence":
        return filterByConfidence(args[0].value)
    elif category == "time":
        print("reached filterBy")
        print(args[0].value)
        return filterByTime(args[0].value)

def filter(filterings: list[filterState]):
    query = "SELECT * FROM potholes WHERE 1=1"
    params = []

    for filtering in filterings:
        print(filtering.category)
        print(filtering.active)
        if filtering.args[0].label == "non-active":
            continue
        elif filtering.active:
            query += " AND "
            #query += query_by_category.get(filtering.name)
            appendix = filterBy(filtering.category, filtering.args) #return value is an array consisting of a string and an array of strings (very ugly)
            if appendix == None:
                print("invalid input")
                query += "1=1"
            else:
                print(appendix)
                query += appendix[0]
                for param in appendix[1]:
                    params.append(param)

    conn = sqlite3.connect("potholes.db")
    cursor = conn.cursor()
    print(query)
    print(params)
    cursor.execute(query,params)
    return cursor.fetchall()

insertPotholes([testPh1, testPh2, testPh3, testPh4, testPh5])
insertPothole(otherGeometry)
#print(os.path.abspath("potholes.db"))
test = filterState("confidence",[valueAssignment("probability", 0.8)])
test2 = filterState("severity", [valueAssignment("very high", True)])
test3 = filterState("location",[valueAssignment("latitude", 7.5), valueAssignment("longitude", 51.32), valueAssignment("radius", 0.011)])
#test = filterState("confidence",0.8)
conn = sqlite3.connect("potholes.db")
cursor = conn.cursor()
print(filter([test]))
#print("test2")
#print(filter([test2]))
#print(filter([test, test2]))
deletePotholeById(28)
deletePotholeById(29)
deletePotholeById(30)
deletePotholeById(31)
deletePotholeById(32)
deletePotholeById(38)
print("test3")
print(filter([test3]))
cursor.execute("SELECT * FROM potholes")
print(cursor.fetchall())
conn.close()