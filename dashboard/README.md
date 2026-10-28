# ASA_IN_DE
Pothole detection with Robot

python-code for creation of an interactive dashboard to visualize the location and shape of potholes on existing maps such as OpenStreetMap and provide additional information.

### Features
- pop-ups for each pothole displaying its "severity", "confidence" (probability, that it really exists, up to 1 digit) and "found at" (date of detection)
- geometric shape of each pothole as polygon as long as sufficent data is available; coloring based on severity in accordance with a legend
- filter options for location, severity, confidence and date of detection

### Architecture
- database.py: setup for database potholes.db with function filter(filterings: list[filterState]) for constructing query-strings in sqlite3
- endpoint.py: initialization of filterSettings and defining of object types used to change them
- visualization.py: creating a folium map visible on localhost with some pseudo-potholes for testing purposes

### Start
1. paste python visualization.py in terminal in VSCode
2. browse URL: "http://127.0.0.1:5000" to open map
3. use mouse and keyboard to customize filter and pop-ups 
