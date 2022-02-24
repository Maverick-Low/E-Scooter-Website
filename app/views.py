from app import app
from flask import render_template, request, url_for, redirect, flash, session
from datetime import datetime

@app.route("/")
def test():
    return render_template("base.html")
