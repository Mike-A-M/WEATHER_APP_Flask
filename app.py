import os

import requests
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
app.config["DEBUG"] = True
db = SQLAlchemy(app)


class city(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city_name = request.form.get("city", "").strip()
        if city_name:
            db.session.add(city(name=city_name))
            db.session.commit()
        return redirect(url_for("index"))

    cities = city.query.all()
    weather_data = []
    api_key = "c13bbff35651894e806992a7129ab87a"

    for saved_city in cities:
        if not api_key:
            weather_data.append(
                {
                    "city": saved_city.name,
                    "error": "Set OPENWEATHER_API_KEY to retrieve weather.",
                }
            )
            continue

        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": saved_city.name,
                    "units": "imperial",
                    "appid": api_key,
                },
                timeout=10,
            )
            response.raise_for_status()
            result = response.json()
            weather_data.append(
                {
                    "city": saved_city.name,
                    "temperature": result["main"]["temp"],
                    "description": result["weather"][0]["description"],
                    "icon": result["weather"][0]["icon"],
                }
            )
        except (requests.RequestException, KeyError, IndexError, TypeError):
            app.logger.exception("Weather lookup failed for %s", saved_city.name)
            weather_data.append(
                {"city": saved_city.name, "error": "Weather data unavailable."}
            )
    
    return render_template("weather.html", weather_data=weather_data)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
