from flask import Flask, render_template, jsonify
import json
import os
from pymongo import MongoClient

# Flask initialization
app = Flask(__name__, static_folder='static')

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['toledoSouza']
collection = db['devices']

# Path to the JSON file
jsonFilePath = os.path.join(os.path.dirname(__file__), 'teste.json')

# Load data from JSON to MongoDB
def loadDataToMongodb():
    with open(jsonFilePath, 'r') as file:
        data = json.load(file)
        collection.delete_many({})
        collection.insert_many(data)

# Main route that renders the HTML template
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/dados', methods=['GET'])
def get_dados():
    print(collection)
    devices = list(collection.find({}, {'_id': 0}))
    return jsonify(devices)

if __name__ == "__main__":
    # Load data when starting the application
    loadDataToMongodb()
    app.run(host='localhost', port=7654, debug=True)
