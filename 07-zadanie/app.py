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


class QuadraticFunctionForm(FlaskForm):
    a = IntegerField('Podaj a:', validators=[
        DataRequired()
    ], )
    b = IntegerField('Podaj b:', validators=[
        DataRequired()
    ], )
    c = IntegerField('Podaj c:', validators=[
        DataRequired()
    ], )
    submit = SubmitField('Oblicz miejsca zerowe')


@app.route('/')
def index():
    form = QuadraticFunctionForm()
    return render_template(
        'index.html',
        title='Oblicz miejsca zerowe funkcji kwadratowej',
        form=form
    )


@app.route('/oblicz', methods=['POST'])
def oblicz():
    a = int(request.form['a'])
    b = int(request.form['b'])
    c = int(request.form['c'])
    if a == 0:
        message = 'To nie jest funkcja kwadratowa'
    else:
        delta = math.pow(b, 2) - 4 * a * c
        if delta > 0:
            x1 = round((-b - math.sqrt(delta)) / 2 * a)
            x2 = round((-b + math.sqrt(delta)) / 2 * a)
            message = 'x1 = ' + str(x1) + ', x2 = ' + str(x2)
        elif delta == 0:
            x0 = round(-b/2 * a)
            message = 'x0 = ' + str(x0)
        else:
            message = 'Ta funkcja nie ma miejsc zerowych'

    return render_template('index.html', message=message, a=a, b=b, c=c, form=QuadraticFunctionForm())


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', title='500'), 500


if __name__ == '__main__':
    app.run(debug=True)
