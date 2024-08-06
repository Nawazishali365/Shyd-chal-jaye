from flask import Flask, jsonify, render_template
import requests
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    # Fetch location data
    locURL = 'https://ipinfo.io/json'
    location = urlopen(locURL)
    YourLoc = json.load(location)
    cityName = YourLoc.get('city')

    # Fetch weather data
    apiKey = '98943b1b4b2021db6e7a9f14cb07059b'
    baseURL = 'https://api.openweathermap.org/data/2.5/weather?q='
    completeURL = baseURL + cityName + '&appid=' + apiKey
    response = requests.get(completeURL)
    data = response.json()

    # Extract weather data
    temp = float(data['main']['temp']) - 273.15
    feels_like = float(data['main']['feels_like']) - 273.15
    max_temp = float(data['main']['temp_max']) - 273.15
    min_temp = float(data['main']['temp_min']) - 273.15

    # Prepare data to be sent
    weather_data = {
        'temp': round(temp, 2),
        'feels_like': round(feels_like, 2),
        'max_temp': round(max_temp, 2),
        'min_temp': round(min_temp, 2),
        'location_data': YourLoc
    }

    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)
