from flask import Flask, render_template, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')

users = {
    'admin': 'password'
}


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/get/login/content')
def login_form_page():
    form = LoginForm()
    return render_template('login_form.html', form=form)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users and users[username] == password:
            return redirect(url_for('get_data'))
        else:
            return "Invalid credentials", 401
    return render_template('login_form.html', form=form)


@app.route('/get/data', methods=['GET'])
def get_data():
    data = {
        "user_info": {
            "username": "admin",
            "role": "administrator"
        }
    }
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)
