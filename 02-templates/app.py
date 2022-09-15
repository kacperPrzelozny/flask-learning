from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title='Strona główna')


@app.route('/user/<name>')
def user(name):
    return render_template('index.html', title='Użytkownik', name=name)


if __name__ == '__main__':
    app.run()
