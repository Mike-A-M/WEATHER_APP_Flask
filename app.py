from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET', 'POST'])
def index():
    
    url ="https://api.openweathermap.org/data/2.5/weather?q={}&appid=c13bbff35651894e806992a7129ab87a"
    city = request.form.get('city')
    r = requests.get(url.format(city)).json()
    
    weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }
    print(weather)
    return render_template('weather.html', weather=weather)

