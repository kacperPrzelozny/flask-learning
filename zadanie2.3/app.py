import json

from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_bs4 import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

app: Flask = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
date = datetime.now()
app.config['SECRET_KEY'] = 'sdfsfsafafahehwf52341eqf21ACAB'


class StationForm(FlaskForm):
    """formularz szukania pogody"""
    station = StringField('Station:', validators=[DataRequired()])
    submit = SubmitField('Search')


@app.route('/')
def index():
    return render_template(
        'weather.html',
        title='Strona główna',
        form=StationForm()
    )


@app.route('/showWeather', methods=['POST', 'GET'])
def showWeather():
    stationName = request.form['station']
    with open("data/data.json", encoding="utf-8") as stationsFile:
        stations = json.load(stationsFile)
        print(stations)
        stationsFile.close()
    for station in stations:
        if station['stacja'] == stationName:
            return render_template(
                'weather.html',
                title='Pogoda',
                form=StationForm(),
                date=station['data_pomiaru'],
                time=station['godzina_pomiaru'],
                temperature=station['temperatura'],
                wind_speed=station['predkosc_wiatru'],
                wind_direction=station['kierunek_wiatru'],
                humidity=station['wilgotnosc_wzgledna'],
                rain_sum=station['suma_opadu'],
                pressure=station['cisnienie'],
                hasData=True
            )
    return render_template('weather.html', form=StationForm(), title='Strona główna', message="Enter proper city name", hasData=False)

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', title='500'), 500


if __name__ == '__main__':
    app.run(debug=True)
