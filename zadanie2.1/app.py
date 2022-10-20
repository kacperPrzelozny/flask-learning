from array import array

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


class ArrayForm(FlaskForm):
    a = StringField('Podaj ciąg liczb po przecinku:', validators=[
        DataRequired()
    ])
    submit = SubmitField('Oblicz')


@app.route('/')
def index():
    form = ArrayForm()
    return render_template(
        'index.html',
        title='Ciąg liczb',
        form=form
    )


@app.route('/ciag', methods=['POST'])
def oblicz():
    desired_array = [int(numeric_string) for numeric_string in request.form['a'].split(',')]
    avg = sum(desired_array) / len(desired_array)
    desired_array.sort(reverse=True)
    minimum = min(desired_array)
    maximum = max(desired_array)
    return render_template('index.html', avg=avg, reversed_array=desired_array, min=minimum, max=maximum, a=request.form['a'], form=ArrayForm())


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', title='500'), 500


if __name__ == '__main__':
    app.run(debug=True)
