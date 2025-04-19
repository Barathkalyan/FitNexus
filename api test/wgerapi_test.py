from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Your API key
API_KEY = '8436656bfdea517cf584c4019532200f806ffb08'
API_URL = "https://wger.de/api/v2/exercise/?limit=30"  # Modify as needed for more data

def get_workouts():
    headers = {
        "Authorization": f"Token {API_KEY}"
    }
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()  # Returns the workout data in JSON format
    else:
        return {"error": "Failed to fetch workouts"}

@app.route("/get-workouts")
def get_workouts_route():
    workouts = get_workouts()
    return jsonify(workouts)  # Displays the workouts in JSON format

if __name__ == "__main__":
    app.run(debug=True)
