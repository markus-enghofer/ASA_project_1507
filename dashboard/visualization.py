import sqlite3

import geopandas as gpd
from shapely.geometry import Point, Polygon

import folium
import webbrowser
from branca.element import Element, MacroElement, Template

from flask import Flask, request, jsonify

import database
from endpoint import update_filter_checkbox, update_filter_textfield, filterSettings

app = Flask(__name__)
conn = sqlite3.connect("potholes.db")
cursor = conn.cursor()

cursor.execute("SELECT longitude, latitude, confidence, severity, timestamp FROM potholes")
potholes = cursor.fetchall()
m = folium.Map(location=[0, 0], zoom_start=16, tiles="OpenStreetMap")

class filtering:

    def __init__(self, category: str, args, type):
        self.category = category
        self.args = args
        self.type = type

severity_colors = {
        "very high": "red",
        "high": "orange",
        "medium": "yellow",
        "low": "green"
    }

def visualize(center_X = "none", center_Y = "none", fromDb = True, list = []):
    conn = sqlite3.connect("potholes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT latitude, longitude FROM potholes")
    print("function entered successfully")
    #update_filter_checkbox()

    centerX = 0
    centerY = 0
    
    if center_X == "none":
        tmp = cursor.fetchone()
        centerX = tmp[1]
        centerY = tmp[0]

    else:
        centerX = center_X
        centerY = center_Y

    if centerX is None:
        #raise ValueError("No potholes found")
        print("no potholes found")

    else:
        #m = folium.Map(location=[centerX, centerY], zoom_start=16, tiles="OpenStreetMap")
        #m = folium.Map(location=[1, 2], zoom_start=16)

        #folium.TileLayer("Esri WorldImagery").add_to(m)
        #folium.TileLayer("CartoDB Positron").add_to(m)
        #folium.TileLayer("CartoDB Voyager").add_to(m)

        #folium.LayerControl().add_to(m)

        if fromDb:
            #cursor.execute("SELECT longitude, latitude, confidence, severity, timestamp FROM potholes")
            #potholes = cursor.fetchall()
            potholes = database.filter(filterSettings)
            potholes = []
            print(potholes)
        else:
            potholes = list

        #for-loop currently disabled until...        
        for pothole in potholes:
            
            folium.Marker(
                #[pothole[0], pothole[1]],
                #popup=f"Confidence:{pothole[2]}\n Severity:{pothole[3]} \n Found:{pothole[4]}" only if cursor.fetchall() is used
                [pothole[1], pothole[0]],
                popup=f"Confidence:{pothole[2]}\n Severity:{pothole[3]} \n Found:{pothole[4]}"
            ).add_to(m)
            
            data = {
                "confidence": pothole[3],
                "severity": pothole[4]
            }
            
            geometry = Polygon([
                (pothole[1], pothole[2]),
                (pothole[1] + 0.001, pothole[2] - 0.0005),
                (pothole[1] + 0.0015, pothole[2] - 0.0018),
                (pothole[1] - 0.0005, pothole[2] - 0.002),
                (pothole[1] - 0.0025, pothole[2] - 0.001),
                (pothole[1], pothole[2])
            ])

            gdf2 = gpd.GeoDataFrame(
            [data],
            #geometry=[Point(pothole[0], pothole[1])],
            geometry=[geometry],
            crs="EPSG:4326"
            )

            gdf2.to_file(
            "tmp.geojson",
            driver="GeoJSON"
            )
            print("survived geojsonPart")

            folium.GeoJson(
                gdf2,              
                style_function=lambda feature: {
                    "fillColor": severity_colors.get(
                        feature["properties"]["severity"],
                        "gray"   # fallback if unknown
                    ),       
                    "color": "black", #outline
                    "weight": 1,
                    "fillOpacity": 0.7
                },
                
                popup=folium.GeoJsonPopup(
                    fields=["confidence","severity"],
                    aliases=["Confidence:", "Severity:"]
                )
            ).add_to(m)
#...here
        legend_html = f"""
        <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        z-index: 9999;
        background-color: white;
        border: 2px solid grey;
        border-radius: 6px;
        padding: 10px;
        font-size: 14px;
        ">
        <b>Pothole Severity</b><br>
        """

        for label, color in severity_colors.items():
            legend_html += f"""
            <i style="background:{color}; width:12px; height:12px; display:inline-block;"></i>
            {label.title()}<br>
            """

        legend_html += "</div>"

        filter = filter_set_up()
        filter += "</div>"

        filter += script_set_up()
        m.get_root().html.add_child(folium.Element(legend_html))
        m.get_root().html.add_child(folium.Element(filter))
        m.save("map.html")

        #print(pothole)
        print(m.location)
        conn.close()
        #webbrowser.open("map.html")

filterPanel = [
    filtering("location", ["latitude", "longitude", "radius"], "textfield"),
    filtering("severity", ["very high", "high", "medium", "low"], "checkbox"),
    filtering("confidence", ["probability"], "textfield"),
    filtering("time", ["max. number of days elapsed since detection"], "textfield")
]
"""
def filteringsToJavaScript():
    code = ""
    for filtering in filterings:
        code += "\n".join(t type="checkbox"> <label>{filtering.category}</label><br>'"
checkboxes_html = f"""

def filter_set_up():
    javaScriptCode = f"""<div style="
                position: fixed;
                top: 10px;
                left: 10px;
                z-index:9999;
                background-color:white;
                padding:5px;
                border: 2px solid grey;
                border-radius: 6px;
                max-width: 250px;
                max-height: 300px;
                overflow-y: auto;
                padding: 10px;
                font-size: 14px;">
                <b>filter panel</b><br><br>
                """
    for filtering in filterPanel:
        if filtering.type == "checkbox":
            javaScriptCode += f"""
            <div>
                <b>{filtering.category}</b><br>
                <div>
                    {options_set_up(filtering)}  
                </div><br>     
            </div>
            """
        elif filtering.type == "textfield":
            #args_count = len(filtering.args)
            javaScriptCode += f"""
            <div>
                <b>{filtering.category}</b><br>
                <div>
                    {textfields_set_up(filtering)}
                </div><br>
                <button
                    class="layer-textfield"
                    data-layer="{filtering.category}"              
                    id="{filtering.category}"
                >
                    Submit
                </button><br><br><br>      
            </div>
            """
            #onclick="getText({filtering.category, filtering.args}
        else:
            continue
            #TODO: exception handling
    return javaScriptCode

def options_set_up(filtering):
    result = ""
    category = filtering.category
    for arg in filtering.args:
        result += f"""
            <label for="{arg}">{arg}</label>
                    <input type="checkbox"
                        class="layer-checkbox"
                        data-layer="{category}"
                        id="{arg}"
                        name="{arg}"
                        {arg}>

    """
        # onclick="toggleCheckboxTest({category, arg}
    return result

def textfields_set_up(filtering):
    result = ""
    for arg in filtering.args:
        result += f"""
            <label for="{arg}">{arg}:</label>
                <input type="text"
                    class="{filtering.category}"
                    id="{arg}"
                    name="{arg}"
                    {arg}>
    """
    return result

def script_set_up():
    result = f"""
    <script>
        // wait until map is ready
        document.addEventListener("DOMContentLoaded", function() {{

                // Folium map variable (auto-generated)
                var mapObj = Object.values(window).find(v => v instanceof L.Map);

                if (!mapObj) {{
                    console.error("Map not found");
                    return;
                }}

                // create layer group
                window.dynamicLayer = L.layerGroup().addTo(mapObj);

                // update function
                window.updateLayer = function(data) {{
                    window.dynamicLayer.clearLayers();

                    for (let i = 0; i < data.length; i++) {{
                        L.marker([data[i][0], data[i][1]])
                            .addTo(window.dynamicLayer);
                    }}
                }};
                updateLayer([
                    [51.5,0.1],
                    [51.51,0.12]
                ]);

                L.marker([5, 5])
                .bindPopup("hallo")
                .addTo(window.dynamicLayer);

            function getColor(s) {{
                if (s == "very high") return "red";
                if (s == "high") return "orange";
                if (s == "medium") return "yellow";
                if (s == "low") return "green";
                return "#FD8D3C";
            }}

            document.querySelectorAll(".layer-checkbox")
                .forEach(cb => {{
                    cb.addEventListener("change", async function() {{
                        const response = await fetch("/checkbox", {{
                            method: "POST",
                            headers: {{
                            "Content-Type": "application/json"
                            }},
                            body: JSON.stringify({{ 
                                category: this.dataset.layer,
                                arg: this.id,
                                checked: this.checked }})
                        }});
                        const potholesNew = await response.json();
                        //alert(potholesNew);
                        if (potholesNew == "test") {{
                            alert("yes");
                        }}

                        window.dynamicLayer.clearLayers();
                        potholesNew.forEach(function(m) {{
                            L.marker([m[1], m[2]])
                            .bindPopup(`<div>
                                <strong>Severity: </strong> ${{m[4]}}<br>
                                <strong>Confidence: </strong> ${{m[3]}}<br>
                                <strong>Found at: </strong> ${{m[5]}}
                            </div>`)
                            .addTo(window.dynamicLayer);

                            const feature = {{
                                "type": "Feature",
                                "properties": {{ "confidence": m[3], "severity": m[4],}},
                                "geometry": {{
                                    "type": "Polygon",
                                    "coordinates": 
                                    [[
                                        [m[2], m[1]],
                                        [m[2] + 0.00001, m[1] - 0.000005],
                                        [m[2] + 0.000015, m[1] - 0.000018],
                                        [m[2] - 0.000005, m[1] - 0.00002],
                                        [m[2] - 0.00002, m[1] - 0.00001],
                                        [m[2], m[1]],
                                    ]]
                                }}
                            }};

                            L.geoJSON(feature, {{
                                style: function(feature) {{
                                    return {{
                                        color: "black",
                                        weight: 1,
                                        fillColor: getColor(feature.properties.severity),
                                        fillOpacity: m[3]   
                                    }};
                                }}
                            }}).addTo(window.dynamicLayer);
                        }});    
                    }});
                }});

            document.querySelectorAll(".layer-textfield")
                .forEach(cb => {{
                    cb.addEventListener("click", async function() {{
                        const category = this.dataset.layer
                        const values = [...document.querySelectorAll(`.${{category}}`)]
                            .map(textfield => ({{
                                id: textfield.id,
                                content: textfield.value}}));
                        //alert(category)
                        //alert(JSON.stringify(values, null, 2));
                        const response = await fetch("/textfield", {{
                            method: "POST",
                            headers: {{
                            "Content-Type": "application/json"
                            }},
                            body: JSON.stringify({{ 
                                category: category,
                                args: values 
                            }})
                        }});
                        const potholesNewText = await response.json();
                        
                        if (potholesNewText == "test") {{
                            alert("yes");
                        }}
                        //alert(potholesNewText)
                        window.dynamicLayer.clearLayers();
                        potholesNewText.forEach(function(m) {{
                        L.marker([m[1], m[2]])
                        .bindPopup(`<div>
                            <strong>Severity: </strong> ${{m[4]}}<br>
                            <strong>Confidence: </strong> ${{m[3]}}<br>
                            <strong>Found at: </strong> ${{m[5]}}
                        </div>`)
                        .addTo(window.dynamicLayer);

                        const feature = {{
                                "type": "Feature",
                                "properties": {{ "confidence": m[3], "severity": m[4],}},
                                "geometry": {{
                                    "type": "Polygon",
                                    "coordinates": [[
                                        [m[2], m[1]],
                                        [m[2] + 0.1, m[1]],
                                        [m[2], m[1] + 0.02],
                                        [m[2], m[1]],
                                    ]]
                                }}
                            }};

                            L.geoJSON(feature, {{
                                style: function(feature) {{
                                    return {{
                                        color: "black",
                                        weight: 1,
                                        fillColor: getColor(feature.properties.severity),
                                        fillOpacity: m[3]   
                                    }};
                                }}
                            }}).addTo(window.dynamicLayer);
                        }});    
                    }});
                }});                 

            async function getText(category, args) {{
                for(let i=0; i<args.length; i++) {{
                    console.log(i);
                    sendText(category, args[i]);
                }}
            }}
            async function sendText(category, arg) {{
                const text = document.getElementById(category + "_" + arg).value;
  
                console.log("text detected");

                await fetch("/textfield", {{
                    method: "POST",
                    headers: {{
                    "Content-Type": "application/json"
                    }},
                    body: JSON.stringify({{ 
                        category,
                        arg,
                        text }})
                }});
            }}
        }});
        </script>"""
    return result

#category, arg, in body of await...
#[[
#    [m[2], m[1]],
#    [m[2] + 0.1, m[1]],
#    [m[2], m[1] + 0.02],
#   [m[2], m[1]],
#]]

"""
alert("response = " + response.status)
async function toggleCheckboxTest() {{
                updateLayer([
                    [51.6,0.1],
                    [51.55,0.12]
                ]);
            }}

            async function toggleCheckbox(category, arg) {{
                updateLayer([
                    [51.6,0.1],
                    [51.55,0.12]
                ]);
                const checked = document.getElementById(category + "_" + arg).checked;
                
                if (checkbox.checked) {{
                    console.log("Checkbox is checked");
                }} else {{
                    console.log("Checkbox is not checked");
                }}
"""



"""
const potholesNew = await response.json
                potholesNew.forEach(function(m) {{
                L.marker([m[1], m[2]])
                .bindPopup(m[3])
                .addTo(dynamicLayer);
                }});              
"""


"""
    <div style="position: fixed;
                top: 10px;
                left: 10px;
                z-index:9999;
                background:white;
                padding:5px;">
        <input type="checkbox" id="myCheckbox"> Option
    </div>

    <script>
    document.getElementById("myCheckbox").addEventListener("change", function() {
        fetch("/checkbox", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({checked: this.checked})
        });
    });
    </script>

    m.get_root().html.add_child(Element(html))
    """
@app.route("/")
def index():
    visualize()
    return m.get_root().render()

@app.route("/checkbox", methods=["POST"])
def update_filter_checkbox():
    data = request.get_json()
    #result = "failed"
    print("reached endpoint!!!")
    print("responseee")
    nothingChecked = True
    for filter in filterSettings:
        if(filter.category == data["category"]):  
            filter.active = True 
            for arg in filter.args:
            #    if checks_count == 0:
            #        arg.value = False
            #    if checks_count == 1 and data["arg"]:
            #        arg.value == True
                if(arg.label == data["arg"]):
                    arg.value = data["checked"]
                
                if arg.value:
                    nothingChecked = False

    #if data["checked"]:
    #checks_count = checks_count + 1
    #else:
    #    checks_count =  - 1
            if nothingChecked:
                filter.active = False
    print("nothingChecked = ")
    print(nothingChecked)
    return jsonify(database.filter(filterSettings))

@app.route("/textfield", methods=["POST"])
def update_filter_textfield():
    data = request.get_json()
    print("reached textfield endpoint")
    for filter in filterSettings:
        if(filter.category == data["category"]):
            #filter.active = True
            for arg1 in data["args"]:
                if(arg1 != ""):
                    filter.active = True
                print(arg1["id"])
                for arg2 in filter.args:
                    if(arg1["id"] == arg2.label):
                        print(arg2.label)
                        arg2.value = arg1["content"]
                        print(arg2.value)
    return jsonify(database.filter(filterSettings))
    

if __name__ == "__main__":
    app.run(debug=True)
print("worked")
#visualize()
