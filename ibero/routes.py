from flask import render_template
from ibero import app

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')