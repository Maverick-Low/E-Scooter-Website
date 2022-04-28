from email.message import Message
from encodings import utf_8
from enum import auto                     
from pickle import FALSE
from sqlalchemy import false
from app import app, models, bcrypt, db
from flask import render_template, request, url_for, redirect, flash, session,json
from datetime import datetime, timedelta, date, time
from .forms import Registration, Login, Payment, Report, Booking, Prices
import smtplib, ssl
from email.mime.text import MIMEText
from werkzeug.datastructures import MultiDict
from cryptography.fernet import Fernet                                             




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
    admin_obj = models.User.query.filter_by(email="admin@admin.com").first()
    admin_obj.admin = True
    staff_obj = models.User.query.filter_by(email="staff@staff.com").first()
    staff_obj.staff = True
    # issue = models.Report(issue = "Refund", description = "Havent recieved refund yet", priority = 1)
    # db.session.add(issue)
    models.Card.query.filter_by(id=1).delete()                                                                                                   
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
@app.route("/login", methods = ["GET", "POST"])
def login():
    if "email" in session:
        flash("You are already logged in!")
        return redirect(url_for("dashboard"))

    form = Login()
    if request.method == "GET":
        return render_template("Login/Website_Login.html", form=form)
    elif request.method == "POST" and form.validate_on_submit:
        user_obj = models.User.query.filter_by(email=form.email.data).first()
        if not user_obj:
            flash('This email is not registered!')
            return render_template('Login/Website_Login.html', form=form)
        elif user_obj and bcrypt.check_password_hash(user_obj.password, form.password.data):
            session["email"] = user_obj.email
            session["admin"] = user_obj.admin
            session["staff"] = user_obj.staff
            flash("Welcome " + user_obj.username + "!")
            # if user_obj.admin == True:
            #     return redirect("/admin")
            return redirect(url_for("dashboard"))
        else:
            flash("Incorrect password!")
            return render_template('Login/Website_Login.html', form=form)
    else:
        return render_template("Login/Website_Login.html", form=form)

@app.route("/", methods = ["GET", "POST"])
def mainmenu():
        if session.get('admin') != 0:
            return redirect("/admin")
        if session.get('staff') != 0:
            return redirect('/staff')
        prices = models.Price.query.all()
        form = Booking()
        Scooters = models.Scooter.query.filter_by(in_use = False).all()
        # Counting the number of available scooters in each loaction
        # For ease of displaying in hire_scooter.html
        count = [0,0,0,0,0]
        for elem in Scooters:
            if elem.LocationID == 1:
                count[0] += 1
            elif elem.LocationID == 2:
                count[1] += 1
            elif elem.LocationID == 3:
                count[2] += 1
            elif elem.LocationID == 4:
                count[3] += 1
            elif elem.LocationID == 5:
                count[4] += 1
        if request.method == "GET":
            return render_template("Main/Website_Main.html",form = form, scooters = Scooters, count = count, prices = prices)
        elif request.method == "POST":
            if form.validate_on_submit():
                location = int(form.location.data)
                hours = int(form.hours.data)
                return redirect(url_for("payment", location=location, hours=hours))
            else:
                return render_template("Main/Website_Main.html",form = form, scooters = Scooters, count = count, prices = prices)
        else:
            return render_template("Main/Website_Main.html",form = form, scooters = Scooters, count = count, prices = prices)
        
@app.route("/error404")
def error404():
    if session.get('admin') != 0:
        return redirect("/admin")
    if session.get('staff') != 0:
        return redirect('/staff')
    return render_template("Error/Website_Error___1.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    # Prevent user who is already registered and logged in from registering  again
    if "email" in session:
        return redirect(url_for("dashboard"))

    form = Registration()
    if request.method == "GET":
        return render_template('Signup/Website_Sign_up___1.html', form=form)

    elif request.method == "POST":
        if form.validate_on_submit():
            print("validated")
            hashed_password = bcrypt.generate_password_hash(form.password_1.data).decode('utf-8')
            user_obj = models.User(username=form.username.data, email=form.email.data, password=hashed_password, admin=False)
            #check wether account is a student account
            #if it is then apply a discount
            email = str(form.email.data)
            print(email)
            emailLength = int(len(email))
            print(emailLength)
            #check if user is a senior
            user_age = int(form.age.data)
            print(user_age)
            if form.email.data[int(emailLength - 6): int(emailLength)] == ".ac.uk" or user_age >= 65:
                user_obj.discount = True
            print("success")
            session["email"] = form.email.data
            session["admin"] = False
            session["staff"] = False
            db.session.add(user_obj)
            db.session.commit()
            return render_template('Dashboard/Website_Dashboard.html')
        else:
            print("not validated")
            flash('Failed to submit registration form!')
            return render_template('Signup/Website_Sign_up___1.html', form=form)

@app.route("/report", methods = ["GET", "POST"])
def report():
    form = Report()
    if request.method == "GET":
        return render_template('Reports/Website_Report.html', form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            report_obj = models.Report(issue=form.issue.data, description=form.report.data)
            db.session.add(report_obj)
            db.session.commit()
            flash('Report has been successfully sent!')
            return render_template('Dashboard/Website_Dashboard.html')
        else:
            flash('Failed to submit report form!')
            return render_template('Reports/Website_Report.html', form=form)
    


@app.route("/logout")
def logout():
    logout = False
    if "email" in session:
        logout = True
        session.pop("email", None)
    if "admin" in session:
        session.pop("admin", None)
    if "staff" in session:
        session.pop("staff", None)
    if logout:
        flash("You have successfully logged out!")
    
    return redirect(url_for("login"))
    
@app.route("/dashboard")
def dashboard():
    if not session.get('email'):
        return redirect("/login")
    elif session.get('admin') != 0:
        return redirect("/admin")
    elif session.get('staff') != 0:
        return redirect('staff')
    else:
        
        user = models.User.query.filter_by(email = session['email']).first()
        orders = models.Booking.query.filter_by(UserID = user.id).all()
        active_id = []
        current_date = datetime.now()
        for o in orders:
            if (current_date < (o.expiry)):
                active_id.append(o.id)
        return render_template("Dashboard/Website_Dashboard.html", title='Dashboard', orders=orders, active= active_id)


@app.route("/testBookings")
def create_test_bookings():
    # db.session.query(models.Booking).delete()
    db.session.commit()
    b1 = models.Booking(numHours=0, date=datetime.now() - timedelta(days=1), expiry=datetime.now(), price=5,
                        cancelled=False)
    b2 = models.Booking(numHours=0, date=datetime.now() - timedelta(weeks=4), expiry=datetime.now(), price=8,
                        cancelled=False)
    b3 = models.Booking(numHours=0, date=datetime.now() - timedelta(weeks=3), expiry=datetime.now(), price=11,
                        cancelled=False)
    b4 = models.Booking(numHours=0, date=datetime.now() - timedelta(weeks=2), expiry=datetime.now(), price=23,
                        cancelled=False)
    db.session.add(b1)
    db.session.add(b2)
    db.session.add(b3)
    db.session.add(b4)
    db.session.commit()
    return redirect("/")


@app.route("/admin/statistics")
def weekly_income():
    # Redirects user if admin is not in session
    if session.get('admin') == 0:
        return redirect("/")
    # create_test_bookings()
    week_start_date = []  # Stores week start dates starting from the date a week ago today
    week = (datetime.combine(datetime.now(), time.min)) - timedelta(weeks=1)
    week_start_date.append(week)
    sums = [0] * 6  # Stores the sum of the price for each booking within the corresponding week

    for i in range(5):  # Let the graph show information going 10 weeks back from today
        week = week - timedelta(weeks=1)
        week_start_date.append(week)
        # Find all bookings within a given week
        orders = models.Booking.query.all()
        order_list = []
        for obj in orders:
            if obj.date <= week_start_date[i] and obj.date > week_start_date[i + 1]:
                order_list.append(obj)
        # Sum the price of all the bookings in this week

        for order in order_list:
            sums[i] += order.price

    # Format the week start dates to a string day/month/year which will then be displayed in the graph
    count = 0
    for d in week_start_date:
        week_start_date[count] = str(d.strftime("%d/%m/%Y"))
        count += 1
    # week_start_date = ["1", "2", "3"]
    # sums = ["5", "5", "5"]
    # return render_template("graphs.html", weeks=week_start_date, income=sums)
    week_start_date.reverse();
    sums.reverse();
    return render_template("graphs.html", weeks=json.dumps(week_start_date), income=json.dumps(sums))


#solved bug where chrome automatically adds an extra '/' at the end of the url
@app.route("/register/")
def reRoute():
    return redirect("/register")

# Admin-specific app routes
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
        bookings = models.Booking.query.all()
        
        return render_template("bookings.html", orders = bookings)

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

@app.route("/admin/issues")
def admin_issues():
    if session.get('admin') == 0:
        return redirect("/dashboard")
    else:
        issues = models.Report.query.all()
        return render_template("issues.html", issues = issues)
# End of admin specific app routes

@app.route("/admin/issues/resolve_issue/<string:issue_id>")
def resolve_issue(issue_id):
    if session.get('admin') == 0:
        return redirect("/dashboard")
    else:
        issue_obj = models.Report.query.filter_by(id = issue_id).first()
        issue_obj.resolved = True
        db.session.commit()
        return redirect(url_for('admin_issues'))

@app.route("/admin/issues/high_priority")
def high_priority():
    if session.get('admin') == 0:
        return redirect("/dashboard")
    else:
        issues = models.Report.query.order_by(models.Report.priority.asc())
        return render_template("issues.html", issues = issues)

@app.route("/admin/issues/low_priority")
def low_priority():
    if session.get('admin') == 0:
        return redirect("/dashboard")
    else:
        issues = models.Report.query.order_by(models.Report.priority.desc())
        return render_template("issues.html", issues = issues)
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
    param[1] = Hours
    """
    param = location.split('$')
    scooter_to_remove = models.Scooter.query.filter_by(LocationID = param[0], in_use=False).first()
    if scooter_to_remove is None:
        flash("Transaction failed: Someone ordered the last scooter before you.")
        return redirect(url_for('dashboard'))                             
    scooter_to_remove.in_use = True
    user = models.User.query.filter_by(email = session['email']).first()
    username = user.username
    # hours_added = datetime.timedelta(hours = int(param[2]))
    hours1 = int(param[1])
    price = models.Price.query.filter_by(id=hours1).first().price
    
    #check if user is a frequent user
    orders = []
    #calculate week start date
    week = datetime.now() - timedelta(weeks=1)
    #select all bookings for the current user
    orders = models.Booking.query.all()
    hours =  0
    for order in orders:
        if order.date >= week and order.UserID == user.id:
            hours += order.numHours
    
    if user.discount == True or hours >= 8:
        price = price * 4/5

    h = 1
    if param[1] == 2:
        h = 4
    elif param[1] == 3:
        h = 24
    elif param[1] == 4:
        h = 24 *7


    expiry = datetime.now() + timedelta(hours=int(param[1]))
    booking = models.Booking(ScooterID = scooter_to_remove.id, UserID = user.id, numHours = h, date= datetime.today(), price = price, expiry = expiry)
    db.session.add(booking)
    db.session.commit()
    #Sending confirmation email
    #code for sending an email

    """
    Email sending functionality will not work when details are not filled in
    Need a way of storing them securly as they should not be pushed with a commit.
    """

    # email = 'team38escooter@gmail.com'
    # passw = '' # details in discord - need to add to be able to send emails
    # reciever = session['emal']
    # port = 465
    # message = ('Hi ' + str(username) +', thanks for booking with us. Here are the details of your order:\nPrice: '+ str(param[1]) + '\nDuration: ' + str(param[2]) + '\nDate: ' + str(datetime.today().strftime("%d/%m/%Y, %H:%M")) + ' \nExpiry: ' + str(expiry.strftime("%d/%m/%Y, %H:%M")))

    # msg = MIMEText(message)
    # msg['Subject'] = 'Thanks for ordering with EScooter'
    # msg['From'] = email
    # msg['To'] = reciever



    # with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
    #     server.login(email, passw)
    #     server.send_message(msg)
    #     server.quit()
    
    flash(f'Scooter has been successfuly hired')
    return redirect(url_for('dashboard'))

@app.route("/admin/bookings")
def bookings():
    orders = models.Booking.query.all()
    

@app.route("/payment", methods = ["GET", "POST"])
def payment():
    if not session.get('email'):
        return redirect("/login")
    location = request.args['location']
    arr = request.args['hours']
    #admin redirected to admin dashboard
    locations = ['Trinity Centre','Train Station','Merrion Centre','LRI Hospital','UoL Edge Sports Centre']
    if session.get('admin') != 0:
        return redirect("/admin")
    #write_key()
    key = load_key()
    f = Fernet(key)                           
    if request.method == "GET":
        # In order to display the location that user is reserving scooter from on payment screen
        currentUser = models.User.query.filter_by(email = session.get('email')).first()
        exists = db.session.query(models.Card.UserID).filter_by(UserID = currentUser.id).first() is not None
        if (exists == True):
            currentUserCard = models.Card.query.filter_by(UserID = currentUser.id).first()
            autoFilledName = currentUserCard.name # Retrieves name of user
            autoFilledCardNumber = f.decrypt(currentUserCard.cardnum).decode("utf-8") # Retrieves user's card number
            autoFilledExpiry = currentUserCard.expiry.strftime("%m/%Y") # Retrieves user's card expiry date
            autoFilledAddressLine1 = currentUserCard.address1
            autoFilledAddressLine2 = currentUserCard.address2
            autoFilledCity = currentUserCard.city
            autoFilledPostCode = currentUserCard.postcode
            form = Payment(formdata = MultiDict([('name', autoFilledName), ('card_number', autoFilledCardNumber), ('expiry_date', autoFilledExpiry),
                                                 ('address_line_1', autoFilledAddressLine1), ('address_line_2', autoFilledAddressLine2), ('city', autoFilledCity),
                                                 ('postcode', autoFilledPostCode), ]))
        else: 
            form = Payment()                                                                                                                     
        return render_template("Payment/Website_Payment___1.html", form=form, location = location, arr=arr)
    elif request.method == "POST":
        form = Payment()                
        if form.validate_on_submit():
            location = int(location)
            value = request.form.getlist('saveDetails')
            if(len(value) != 0):                                                                       
                arr2 = [form.name.data,form.card_number.data,form.expiry_date.data,form.address_line_1.data,form.address_line_2.data,form.city.data,form.postcode.data]
                x = form.card_number.data.encode()
                encryptedCard = f.encrypt(x)                            
                user = models.User.query.filter_by(email = session.get('email')).first()
                card_obj = models.Card(UserID = user.id, name = arr2[0], cardnum = encryptedCard, expiry = arr2[2]
                                   , address1 = arr2[3], address2 = arr2[4], city = arr2[5], postcode = arr2[6])
                db.session.add(card_obj)
                db.session.commit()
            #flash("Transaction confirmed!")
            return redirect("/remove_available/"+str(location)+'$' + str(arr))
        else:
            flash('Card payment not accepted')
            return render_template('Payment/Website_Payment___1.html', form=form, location = location, arr=arr)
# Encryption code taken from https://dev.to/anishde12020/cryptography-with-python-using-fernet-40o3
def write_key():
    key = Fernet.generate_key() # Generates the key
    with open("key.key", "wb") as key_file: # Opens the file the key is to be written to
        key_file.write(key) # Writes the key

def load_key():
    return open("key.key", "rb").read() #Opens the file, reads and returns the key stored in the file
               



@app.route("/cancel_booking/<int:bookingID>")
def cancel_booking(bookingID):
    booking_to_cancel = models.Booking.query.filter_by(id=bookingID).first()
    scooter_to_free = models.Scooter.query.filter_by(id = booking_to_cancel.ScooterID).first()
    scooter_to_free.in_use = False                            
    booking_to_cancel.cancelled = True
    db.session.commit()
    return redirect(url_for("dashboard"))



@app.route("/extend_booking/<int:bookingID>/<int:duration>")
def extend_booking(bookingID, duration):
    booking_to_extend = models.Booking.query.filter_by(id=bookingID).first()
    prices = models.Price.query.all()
    
    #check if user 
    user_obj = models.User.query.filter_by(id =booking_to_extend.UserID).first()
    orders = []
    #calculate week start date
    week = datetime.now() - timedelta(weeks=1)
    #select all bookings for the current user
    orders = models.Booking.query.all()
    hours =  0
    for order in orders:
        if order.date >= week and order.UserID == user_obj.id:
            hours += order.numHours

    #check if discount should be applied
    if hours >= 8 or user_obj.discount == True:
        if duration == 1:
            booking_to_extend.numHours += 1
            booking_to_extend.price += prices[0].price*0.8
            booking_to_extend.expiry +=  timedelta(hours=1)
        elif duration == 2:
            booking_to_extend.numHours += 4
            booking_to_extend.price += prices[1].price*0.8
            booking_to_extend.expiry +=  timedelta(hours=4)
        elif duration == 3:
            booking_to_extend.numHours += 24
            booking_to_extend.price += prices[2].price*0.8
            booking_to_extend.expiry +=  timedelta(days=1)
        elif duration == 4:
            booking_to_extend.numHours += 168
            booking_to_extend.price += prices[3].price*0.8
            booking_to_extend.expiry +=  timedelta(days=7)
    else:
        if duration == 1:
            booking_to_extend.numHours += 1
            booking_to_extend.price += prices[0].price
            booking_to_extend.expiry +=  timedelta(hours=1)
        elif duration == 2:
            booking_to_extend.numHours += 4
            booking_to_extend.price += prices[1].price
            booking_to_extend.expiry +=  timedelta(hours=4)
        elif duration == 3:
            booking_to_extend.numHours += 24
            booking_to_extend.price += prices[2].price
            booking_to_extend.expiry +=  timedelta(days=1)
        elif duration == 4:
            booking_to_extend.numHours += 168
            booking_to_extend.price += prices[3].price
            booking_to_extend.expiry +=  timedelta(days=7)
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/add_pricing")
def add_pricing():
    price1 = models.Price(time = "1 hour", price = 10)
    price2 = models.Price(time = "4 hour's", price = 10)
    price3 = models.Price(time = "1 day", price = 10)
    price4 = models.Price(time = "1 week", price = 10)
    db.session.add(price1)
    db.session.add(price2)
    db.session.add(price3)
    db.session.add(price4)
    db.session.commit()
    return redirect("/dashboard")
    
    
    
@app.route("/admin/pricing", methods = ["GET", "POST"])
def pricing():
    if session.get('admin') == 0:
        return redirect("/dashboard")
    else:
        form = Prices()
        if request.method == "GET":
            prices = models.Price.query.all()
            autoFillPrice1 = prices[0].price
            autoFillPrice2 = prices[1].price
            autoFillPrice3 = prices[2].price
            autoFillPrice4 = prices[3].price
            form = Prices(formdata = MultiDict([('hour_price', autoFillPrice1), ('four_hour_price', autoFillPrice2), ('day_price', autoFillPrice3),
                                                ('week_price', autoFillPrice4),]))
            return render_template("pricing.html", form = form, prices = prices)

        elif request.method == "POST":
            prices = models.Price.query.all()
            prices[0].price = form.hour_price.data
            prices[1].price = form.four_hour_price.data
            prices[2].price = form.day_price.data
            prices[3].price = form.week_price.data
            db.session.commit()
            return redirect("/admin")
     

#main route for staff dashboard
@app.route('/staff')
def staff_dashboard():
    if session.get('staff') == 0:
        return redirect('/')
    return render_template('staff_dashboard.html')


@app.route('/staff/booking')
def staff_booking():
    if session.get('staff') == 0:
        return redirect('/')
    return render_template('staff_booking.html')


@app.route('/staff/issues')
def staff_issues():
    if session.get('staff') == 0:
        return redirect('/')
    return render_template('staff_issues.html')


@app.route('/staff/manage')
def staff_manage():
    if session.get('staff') == 0:
        return redirect('/')
    return render_template('staff_manage.html')


#for merging
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

