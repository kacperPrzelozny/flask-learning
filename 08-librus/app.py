from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_bs4 import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

app: Flask = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'sdfsfsafafahehwf52341eqf21ACAB'


class LoginForm(FlaskForm):
    """formularz logowania"""
    userLogin = StringField('Login:', validators=[DataRequired()])
    userPassword = PasswordField('Hasło:', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')


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
        userLogin=session.get('userLogin')
    )

@app.route('/logout')
def logout():
    session.pop('userLogin')
    return redirect('login')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', userLogin=session.get('userLogin'))


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', title='500'), 500


if __name__ == '__main__':
    app.run(debug=True)
