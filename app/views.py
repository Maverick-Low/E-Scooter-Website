from app import app
from flask import render_template, request, url_for, redirect, flash, session
from datetime import datetime

@app.route("/")
def test():
    return redirect("/home")
    #return render_template("base.html")

# TODO: replace return statements with actual templates

@app.route("/home/register/")
def register():
    return render_template("register.html")

@app.route("/home/login/")
def signin():
    return render_template("login.html")

@app.route("/home/")
def home():
    return render_template("base.html")
