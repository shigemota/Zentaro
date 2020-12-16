from flask import Flask, redirect, jsonify
from flask import render_template, request
from forms import *
from compiler import *
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.key


@app.route('/')
@app.route('/index')
def index():
    return '<a href="/editor">Start Coding!</a>'


@app.route('/background_process')
def background_process():
    try:
        text = request.args.get('proglang', 0, type=str)
        lang = request.args.get('lang', 0, type=str)
        text = text.split('\n')
        result = main(text, lang)
        result = result.splitlines()
        return jsonify(result=result)
    except Exception as e:
        return str(e)


@app.route('/editor')
def code_editor():
    data = [{'name': 'Java'}, {'name': 'C++'}, {'name': 'Python'}]
    return render_template('code_editor.html', data=data)


@app.route('/sign_in', methods=['GET', 'POST'])  # Вход в систему
def sign_in():
    form = SignIn()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('sign_in.html', title='Sign in' + ' | ', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])  # Регистрация в систему
def sign_up():
    form = SignUp()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('sign_up.html', title='Sign up' + ' | ', form=form)


@app.route('/success')
def success():
    return 'success'


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
