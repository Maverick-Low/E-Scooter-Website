from encodings import utf_8

from sqlalchemy import false
from app import app, models, bcrypt, db
from flask import render_template, request, url_for, redirect, flash, session
from datetime import datetime
from .forms import Registration, Login



@app.route("/add_test")
def add_test():
    location2 = models.Location()
    location3 = models.Location()
    location4 = models.Location()
    location5 = models.Location()
    user_obj = models.Scooter(in_use = False, LocationID = 2)
    user_obj1 = models.Scooter(in_use = False, LocationID = 3)
    user_obj2 = models.Scooter(in_use = False, LocationID = 4)
    user_obj3 = models.Scooter(in_use = False, LocationID = 5)
    user_obj4 = models.Scooter(in_use = False, LocationID = 1)
    db.session.add(user_obj)
    db.session.add(user_obj1)
    db.session.add(user_obj2)
    db.session.add(user_obj3)
    db.session.add(user_obj4)
    db.session.add(location2)
    db.session.add(location3)
    db.session.add(location4)
    db.session.add(location5)
    db.session.commit()
    return redirect(url_for("dashboard"))


# use this function to protect routes from unauthorised access
# e.g. guard_array = ["admin"] ensures only admin users can access route
# e.g. redirect_route = "/home". If user is not authorized, redirect them to this route
def routeGuard(guard_array, redirect_route):
    redirect = False
    if "email" in guard_array:
        if "email" not in session:
            flash("Error: No user logged in!")
            redirect = True
    if "admin" in guard_array:
        if not session["admin"]:
            flash("Error: You do not have admin privileges!")
            redirect = True
    if redirect:
        return redirect(redirect_route)

# if user is registered: adds user's email and admin flag to session and takes them to dashboard]
# gives option for user to be redirected to register or continue as a guest
@app.route("/", methods = ["GET", "POST"])
def login():
    if "email" in session:
        flash("You are already logged in!")
        return redirect(url_for("dashboard"))

    form = Login()
    if request.method == "GET":
        return render_template("login.html", form=form)
    elif request.method == "POST" and form.validate_on_submit:
        user_obj = models.User.query.filter_by(email=form.email.data).first()
        if not user_obj:
            flash('This email is not registered!')
            return render_template('login.html', form=form)
        elif user_obj and bcrypt.check_password_hash(user_obj.password, form.password.data):
            session["email"] = user_obj.email
            session["admin"] = user_obj.admin
            flash("Welcome " + user_obj.username + "!")
            return redirect(url_for("dashboard"))
        else:
            flash("Incorrect password!")
            return render_template('login.html', form=form)
    else:
        return render_template("login.html", form=form)

@app.route("/register", methods = ["GET", "POST"])
def register():
    # Prevent user who is already registered and logged in from registering  again
    if "email" in session:
        return redirect(url_for("dashboard"))

    form = Registration()
    if request.method == "GET":
        return render_template('register.html', form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password_1.data).decode('utf-8')
            user_obj = models.User(username=form.username.data, email=form.email.data, password=hashed_password, admin=False)
            session["email"] = form.email.data
            db.session.add(user_obj)
            db.session.commit()
            return render_template('Dashboard.html')
        else:
            flash('Failed to submit registration form!')
            return render_template('register.html', form=form)
        

@app.route("/logout")
def logout():
    logout = False
    if "email" in session:
        logout = True
        session.pop("email", None)
    if "admin" in session:
        session.pop("admin", None)
    if logout:
        flash("You have successfully logged out!")
    
    return redirect(url_for("login"))
    
@app.route("/dashboard")
def dashboard():
    
    return render_template("dashboard.html", title='Dashboard')

@app.route("/hire_scooter")
def hire_scooter():
    # guest accounts unable to hire right now.
    if session.get('email') == None:
        flash('You must sign in to hire a scooter!')
        return redirect(url_for('login'))
    else:
        Scooters = models.Scooter.query.filter_by(in_use = False).all()
        # Counting the number of available scooters in each loaction
        # For ease of displaying in hire_scooter.html
        counts = [0,0,0,0,0]
        for elem in Scooters:
            if elem.LocationID == 1:
                counts[0] += 1
            elif elem.LocationID == 2:
                counts[1] += 1
            elif elem.LocationID == 3:
                counts[2] += 1
            elif elem.LocationID == 4:
                counts[3] += 1
            elif elem.LocationID == 5:
                counts[4] += 1
        return render_template('hire_scooter.html', scooters = Scooters, counts = counts)

@app.route('/remove_available/<int:location>')
def remove_available(location):
    """
    Remember to save scooter id in order table somewhere
    in order to free correct scooter.
    May cause isssues later
    """
    scooter_to_remove = models.Scooter.query.filter_by(LocationID = location, in_use=False).first()
    scooter_to_remove.in_use = True
    db.session.commit()
    flash(f'Scooter has been successfuly hired')
    return redirect(url_for('dashboard'))


"""
logout code:

if not session.get("email"):
    flash('ERROR')
    return redirect (url_for("login"))
flash("Successful logout")
session.pop("email", None)
session.pop("admin", None)
return redirect (url_for("login"))

"""

# # TODO: replace return statements with actual templates

# @app.route("/home/register/")
# def register():
#     return render_template("register.html")

# @app.route("/home/login/")
# def signin():
#     return render_template("login.html")

# @app.route("/home/")
# def home():
#     return render_template("base.html")
