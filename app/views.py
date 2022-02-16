from app import app
from flask import render_template, request, url_for, redirect, flash, session
from datetime import datetime

@app.route("/")
def test():
    return render_template("base.html")

# TODO: replace return statements with actual templates

@app.route("/register/")
def register():
    return 'registration page'

@app.route("/login/")
def signin():
    return 'login page'

@app.route("/home/")
def home():
    return 'home page'
