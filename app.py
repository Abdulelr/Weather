from flask import Flask, render_template, request
import configparser
import requests
from datetime import datetime

app = Flask(__name__)
app.debug = True


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    api_key = get_api_key()
    temp_units = request.form['temp_units']
    if temp_units == 'F':
        data = get_weather_results_imperial(zip_code, api_key)
        temp = data["main"]["temp"]
    else:
        data = get_weather_results_metric(zip_code, api_key)
        temp = data["main"]["temp"]
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    sa_now = datetime.now()
    print(sa_now)
    offset = data['timezone']
    utc = datetime.utcnow()
    utc = datetime.timestamp(utc)
    local_now = utc + offset
    print(local_now)

    return render_template('results.html', temp=temp, feels_like=feels_like,weather=weather, location=location, local_now=local_now,sa_now=sa_now)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.run()