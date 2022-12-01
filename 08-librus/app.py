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


class LoginForm(FlaskForm):
    """formularz logowania"""
    userLogin = StringField('Login:', validators=[DataRequired()])
    userPassword = PasswordField('Hasło:', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')


def average(subjectValue, termValue):
    """funkcja licząca średnią ocen"""
    with open("data/grades.json") as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    sum = 0
    len = 0
    if subjectValue == "" and termValue == "":
        for subject, terms in grades.items():
            for term, categories in terms.items():
                for category, grades in categories.items():
                    if category in ['answear', 'quiz', 'test']:
                        for grade in grades:
                            sum += grade
                            len += 1
    elif subjectValue != "" and termValue == "":
        for subject, terms in grades.items():
            if subject == subjectValue:
                for term, categories in terms.items():
                        for category, grades in categories.items():
                            if category in ['answear', 'quiz', 'test']:
                                for grade in grades:
                                    sum += grade
                                    len += 1
    else:
        for subject, terms in grades.items():
            if subject == subjectValue:
                for term, categories in terms.items():
                    if term == termValue:
                        for category, grades in categories.items():
                            if category in ['answear', 'quiz', 'test']:
                                for grade in grades:
                                    sum += grade
                                    len += 1
    return round(sum / len, 2)


def highestAverage():
    """funkcja wyznaczająca najwyższą średnią ocen"""
    with open("data/grades.json") as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    subjectAverage = 0
    for subject, terms in grades.items():
        avg = average(subject, "")
        if avg > subjectAverage:
            subjectAverage = avg
    return subjectAverage
def highestName():
    """funkcja wyznaczająca najwyższą średnią ocen"""
    with open("data/grades.json") as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    subjectName = ''
    subjectAverage = 0
    for subject, terms in grades.items():
        avg = average(subject, "")
        if avg > subjectAverage:
            subjectAverage = avg
            subjectName = subject
    return subjectName

def secondHighestAverage():
    highestAvg = highestAverage()
    """funkcja wyznaczająca drugą najwyższą średnią ocen"""
    with open("data/grades.json") as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    subjectAverage = 0
    for subject, terms in grades.items():
        avg = average(subject, "")
        if subjectAverage < avg < highestAvg:
            subjectAverage = avg
    return subjectAverage
def secondHighestName():
    """funkcja wyznaczająca drugą najwyższą średnią ocen"""
    highestAvg = highestAverage()
    with open("data/grades.json") as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    subjectName = ''
    subjectAverage = 0
    for subject, terms in grades.items():
        avg = average(subject, "")
        if subjectAverage < avg < highestAvg:
            subjectAverage = avg
            subjectName = subject
    return subjectName

def under2():
    """funkcja wyznaczająca zagrozenia"""
    with open("data/grades.json") as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    subjectsName = ''
    for subject, terms in grades.items():
        avg = average(subject, "")
        if avg < 2:
            subjectsName = subjectsName + subject + ","
    if subjectsName == '':
        return 'Brak'
    return subjectsName.rstrip(subjectsName[-1])


users = {
    1: {
        'login': 'kprzelozny',
        'password': 'Qwerty123',
        'firstName': 'Kacper',
        'lastName': 'Przełożny'
    }
}


@app.route('/')
def index():
    return render_template(
        'index.html',
        title='Strona główna',
        date=date
    )


@app.route('/login', methods=['POST', 'GET'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        userLogin = loginForm.userLogin.data
        userPassword = loginForm.userPassword.data
        if userLogin == users[1]['login'] and userPassword == users[1]['password']:
            session['userLogin'] = userLogin
            return redirect('dashboard')
    return render_template(
        'login.html',
        title='Logowanie',
        form=loginForm,
        userLogin=session.get('userLogin'),
        date=date
    )


@app.route('/logout')
def logout():
    session.pop('userLogin')
    return redirect('login')


@app.route('/dashboard')
def dashboard():
    with open('data/grades.json') as gradesFiles:
        grades = json.load(gradesFiles)
        gradesFiles.close()
    return render_template('dashboard.html', userLogin=session.get('userLogin'), date=date, grades=grades,
                           countAverage=average, highestAverage=highestAverage, highestName=highestName, secondHighestAverage=secondHighestAverage, secondHighestName=secondHighestName, under2=under2)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', title='500'), 500


if __name__ == '__main__':
    app.run(debug=True)
