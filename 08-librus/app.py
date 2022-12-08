import hashlib
import json

from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_bs4 import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, RadioField
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


class SubjectForm(FlaskForm):
    subject = StringField('Nazwa przedmiotu:', validators=[DataRequired()])
    submit = SubmitField('Dodaj')


class GradeForm(FlaskForm):
    subject = SelectField('Wybierz przedmiot:', choices=str)
    term = RadioField('Wybierz semestr:', choices=[('term1', 'Semestr 1'), ('term2', 'Semestr 2')])
    category = SelectField('Wybierz kategorię:', choices=[('quiz', 'Kartkówka'), ('answear', 'Odpowiedź'), ('test', 'Sprawdzian')])
    grade = SelectField('Ocena', choices=[
        (6, 'Celujący'),
        (5, 'Bardzo dobry'),
        (4, 'Dobry'),
        (3, 'Dostateczny'),
        (2, 'Dopuszczający'),
        (1, 'Niedostateczny'),
    ])
    submit = SubmitField('Dodaj')

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
    if len != 0:
        return round(sum / len, 2)
    else:
        return 0

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
        if avg < 2 and avg != 0:
            subjectsName = subjectsName + subject + ","
    if subjectsName == '':
        return 'Brak'
    return subjectsName.rstrip(subjectsName[-1])


users = {
    1: {
        'login': 'kprzelozny',
        'password': '77aae185203edc6357676db95caa25d0f398d402c1723e6a7b42cfe8d2967f2e',
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
        userPassword = userPassword.encode()
        userPassword = hashlib.sha256(userPassword).hexdigest()
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
                           countAverage=average, highestAverage=highestAverage, highestName=highestName,
                           secondHighestAverage=secondHighestAverage, secondHighestName=secondHighestName,
                           under2=under2)


@app.route('/addSubject', methods=['GET', 'POST'])
def addSubject():
    subjectForm = SubjectForm()
    if subjectForm.validate_on_submit():
        with open('data/grades.json', encoding='utf-8') as gradesFile:
            grades = json.load(gradesFile)
            subject = subjectForm.subject.data
            grades[subject] = {
                'term1': {'answear': [], 'quiz': [], 'test': [], 'interim': 0},
                'term2': {'answear': [], 'quiz': [], 'test': [], 'interim': 0}
            }
        with open('data/grades.json', 'w', encoding='utf-8') as gradesFile:
            json.dump(grades, gradesFile)
            gradesFile.close()
            flash('Dane zostały zapisane poprawnie')
    return render_template('add-subject.html', title='Dodaj przedmiot', userLogin=session.get('userLogin'),
                           form=subjectForm, date=date)

@app.route('/addGrade', methods=['GET', 'POST'])
def addGrade():
    gradeForm = GradeForm()
    with open('data/grades.json', encoding='utf-8') as gradesFile:
        grades = json.load(gradesFile)
        gradeForm.subject.choices = [subject for subject in grades]
    return render_template('add-grade.html', form=gradeForm, date=date, title='Dodaj ocenę', userLogin=session.get('userLogin'))

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', title='500'), 500


if __name__ == '__main__':
    app.run(debug=True)
