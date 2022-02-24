from encodings import utf_8
from pickle import FALSE

from sqlalchemy import false
from app import app, models, bcrypt, db
from flask import render_template, request, url_for, redirect, flash, session
from datetime import datetime, timedelta
from .forms import Registration, Login, Payment



@app.route("/add_test")
def add_test():
    # location2 = models.Location()
    # location3 = models.Location()
    # location4 = models.Location()
    # location5 = models.Location()
    # user_obj = models.Scooter(in_use = False, LocationID = 2)
    # user_obj1 = models.Scooter(in_use = False, LocationID = 3)
    # user_obj2 = models.Scooter(in_use = False, LocationID = 4)
    # user_obj3 = models.Scooter(in_use = False, LocationID = 5)
    # user_obj4 = models.Scooter(in_use = False, LocationID = 1)
    # db.session.add(user_obj)
    # db.session.add(user_obj1)
    # db.session.add(user_obj2)
    # db.session.add(user_obj3)
    # db.session.add(user_obj4)
    # db.session.add(location2)
    # db.session.add(location3)
    # db.session.add(location4)
    # db.session.add(location5)
    admin_obj = models.User.query.filter_by(email="admin@admin.com").first()
    admin_obj.admin = True
    db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/reset_scooter")
def reset_scooter():
    Scooters = models.Scooter.query.filter_by(in_use = True).all()
    for scooter in Scooters:
        scooter.in_use  = False      
    db.session.commit()
    return redirect(url_for("hire_scooter"))



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
            # if user_obj.admin == True:
            #     return redirect("/admin")
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
            session["admin"] = False
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
    if not session.get('email'):
        return redirect("/")
    elif session.get('admin') != 0:
        return redirect("/admin")
    else:
        
        user = models.User.query.filter_by(email = session['email']).first()
        orders = models.Booking.query.filter_by(UserID = user.id).all()
        active_id = []
        current_date = datetime.now()
        for o in orders:
            if (current_date < (o.expiry)):
                active_id.append(o.id)
        return render_template("dashboard.html", title='Dashboard', orders=orders, active= active_id)
     
        
    

#solved bug where chrome automatically adds an extra '/' at the end of the url
@app.route("/register/")
def reRoute():
    return redirect("/register")


@app.route("/admin")
def admin_dash():
    if session.get('admin') != 0:
        return render_template("admin_dashboard.html")
    else:
        return redirect(url_for("dashboard"))

@app.route("/admin/bookings")
def admin_bookings():
    if session.get('admin') == 0:
        return redirect("/dashboard")
    else:
        return render_template("bookings.html")

@app.route("/admin/statistics")
def admin_stats():
    if session.get('admin') == 0:
        return redirect("/dashboard")
    else:
        return render_template("statistics.html")

@app.route("/admin/configure")
def admin_config():
    if session.get('admin') == 0:
        return redirect("/dashboard")
    else:
        return render_template("configure.html")


@app.route("/hire_scooter")
def hire_scooter():
    #admin redirected to admin dashboard
    if session.get('admin') != 0:
        return redirect("/admin")

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



@app.route('/remove_available/<string:location>')
def remove_available(location):
    #admin redirected to admin dashboard
    if session.get('admin') != 0:
        return redirect("/admin")
    """
    param[0] = locationID
    param[1] = Price
    param[2] = Hours
    """
    param = location.split('$')
    
    scooter_to_remove = models.Scooter.query.filter_by(LocationID = param[0], in_use=False).first()
    scooter_to_remove.in_use = True
    user = models.User.query.filter_by(email = session['email']).first()
    # hours_added = datetime.timedelta(hours = int(param[2]))
    expiry = datetime.now() + timedelta(hours=int(param[2]))
    booking = models.Booking(ScooterID = scooter_to_remove.id, UserID = user.id, numHours = param[2], date= datetime.today(), price=param[1], expiry = expiry)
    db.session.add(booking)
    db.session.commit()
    flash(f'Scooter has been successfuly hired')
    return redirect(url_for('dashboard'))


@app.route("/payment/<int:location>", methods = ["GET", "POST"])
def payment(location):
    #admin redirected to admin dashboard
    locations = ['Trinity Centre','Train Station','Merrion Centre','LRI Hospital','UoL Edge Sports Centre']
    if session.get('admin') != 0:
        return redirect("/admin")
    form = Payment()
    if request.method == "GET":
        # In order to display the location that user is reserving scooter from on payment screen
        
        return render_template("payment.html", form=form, location = locations[location - 1])
    elif request.method == "POST":
        if form.validate_on_submit():
            arr = [form.price.data,form.hours.data]
            flash("Transaction confirmed!")
            return redirect("/remove_available/"+str(location)+'$' + str(arr[0]) + '$' + str(arr[1]))
        else:
            flash('Card payment not accepted')
            return render_template('payment.html', form=form, location = locations[location - 1])

@app.route("/cancel_booking/<int:bookingID>")
def cancel_booking(bookingID):
    booking_to_cancel = models.Booking.query.filter_by(id=bookingID).first()
    booking_to_cancel.cancelled = True
    db.session.commit()
    return redirect(url_for("dashboard"))




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

