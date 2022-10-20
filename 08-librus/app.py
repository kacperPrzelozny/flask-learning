from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_bs4 import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import math

app: Flask = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'sdfsfsafafahehwf52341eqf21ACAB'


@app.route('/')
def index():
    return render_template(
        'index.html',
        title='Strona główna',
    )

@app.route('/login')
def login():
    return render_template('login.html', title='Logowanie')

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', title='500'), 500


if __name__ == '__main__':
    app.run(debug=True)
