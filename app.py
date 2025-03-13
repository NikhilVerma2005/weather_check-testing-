from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "1cb70ffab3515ad8f9a368222f15ce1b"  # ✅ Your OpenWeatherMap API key

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_weather", methods=["POST"])
def get_weather():
    city = request.json.get("city")
    if not city:
        return jsonify({"error": "City name is required"}), 400

    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(URL)
    weather_data = response.json()

    if response.status_code == 200:
        return jsonify({
            "city": weather_data["name"],
            "description": weather_data["weather"][0]["description"],
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "wind_speed": weather_data["wind"]["speed"]
        })
    else:
        return jsonify({"error": weather_data.get("message", "Failed to fetch weather data.")}), 404


if __name__ == "__main__":
    app.run(debug=True)
