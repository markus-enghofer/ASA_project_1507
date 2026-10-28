from flask import Flask, request, jsonify
import database

app = Flask(__name__)

class valueAssignment:
    def __init__(self, label: str, value):
        self.label = label
        self.value = value

class filterState:
    #def __init__(self, category: str, args: list[valueAssignment]):
    def __init__(self, category: str, args: list[valueAssignment], active: bool = False):
        self.category = category
        self.args = args
        self.active = active

filterSettings = [
    filterState("location", [valueAssignment("latitude", 51), valueAssignment("longitude", 7.5), valueAssignment("radius", 999)]),
    filterState("severity", [valueAssignment("very high", False), valueAssignment("high", False), valueAssignment("medium", False), valueAssignment("low", False)]),
    filterState("confidence", [valueAssignment("probability", 0)]),
    filterState("time", [valueAssignment("max. number of days elapsed since detection", 0)])
]

"""
def update_filter_states(category, label, value):
    for state in filter_states:
        if state.category == category:
            for arg in state.args:
                if arg.label == label:
                    arg.label
"""

"""
@app.route("/checkbox", methods=["POST"])
def update_filter_checkbox():
    data = request.get_json()
    print("reached endpoint!!!")
    print(data["category"])
    for filter in filter_states:
        if(filter.category == data["category"]):
            for arg in filter.args:
                if(arg == data["arg"]):
                    arg = data["checked"]
    return jsonify(database.filter(filter_states))
"""
@app.route("/checkbox", methods=["POST"])
def update_filter_checkbox():
    """
    data = request.get_json()
    print("reached endpoint!!!")
    print(data["layer"])
    for filter in filter_states:
        if(filter.category == "severity"):
           for arg in filter.args:
                if(arg == data["layer"]):
                    arg = data["checked"]
    return jsonify(database.filter(filter_states)"""
    print("reached endpoint")
    return jsonify([])

@app.route("/textfield", methods=["POST"])
def update_filter_textfield():
    data = request.get_json()
    for filter in filterSettings:
        if(filter.category == data["category"]):
            for arg in filter.args:
                if(arg == data["arg"]):
                    arg = data["checked"]
    return jsonify(database.filter(filterSettings))

if __name__ == "__main__":
    app.run(debug=True)
