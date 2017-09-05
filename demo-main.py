from flask import Flask
from flask import make_response
from flask import render_template

from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

'''
@app.route('/')
def index():
    response = make_response('<h1>Document</h1>')
    response.set_cookie('answer', '42')
    return response


@app.route('/user/<name>')
def user(name):
    str = 'Hello, %s!' % name
    response = make_response(str)
    response.set_cookie('answer', '42')
    return response
'''
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    manager.run()