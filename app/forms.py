from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateTimeField, IntegerField, SubmitField, EmailField
from wtforms.validators import EqualTo, DataRequired, ValidationError, Length, Email
from app import models
import re
from datetime import date, datetime


class Login(FlaskForm):
        email = StringField('Enter email', validators=[DataRequired(), Length(max=60)])
        password = PasswordField('Enter password', validators=[DataRequired(), Length(max=60)])
        submit = SubmitField('Submit')


class Registration(FlaskForm):
        username = StringField('Enter username', validators=[DataRequired(), Length(max=60)])
        email = StringField('Enter email', validators=[DataRequired(), Length(max=60), Email()])
        password_1 = PasswordField('Enter password', validators=[DataRequired(), Length(min=8,max=60)])
        password_2 = PasswordField('Confirm password', validators=[DataRequired(), Length(min=8,max=60), EqualTo('password_1', message='Passwords must match!')])
        submit = SubmitField('Submit')

        # function that validates email adress upon registration
        # todo: write unit tests for functions
        def validateEmail(self, email):     
            user_object = models.User.query.filter_by(email=email.data).first()
            if user_object: #if user is already registered don't allow them to register again
                raise ValidationError('This email address is already registered!')

            #regular expression for an email address with a single '.' after the '@':    
            # email_regex_1 = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            #regular expression for an email address with two '.'s after the '@': 
            # email_regex_2 = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}+\.[A-Z|a-z]{2,}\b'
            
            # if not( (re.search(email_regex_2,str(email)))):# or (re.search(email_regex_1,str(email))) ):
            #      raise ValidationError('This email is not of a valid format!')
        
        #function that validates the password when registering a new user
        def validate_password_1(self, password_1):
            password_1 = str(password_1)

            special_symbol =["$", "@", "#", "%", "£", "^", "*", "(", ")"]
            
            if not any(char.isdigit() for char in password_1):
                raise ValidationError('Password should have at least one numeric digit!')
                
            if not any(char.isupper() for char in password_1):
                raise ValidationError('Password should have at least one uppercase letter!')
                
            if not any(char.islower() for char in password_1):
                raise ValidationError('Password should have at least one lowercase letter!')

            password_regex = re.compile('[^0-9a-zA-Z]+')
            if not password_regex.search(password_1): 
                raise ValidationError('Password should have at least one special symbol!')
    
    
    
class Payment(FlaskForm):
    #function that checks if the expiry date is in the future
    # def validateCVV():
    #     if not (len(self.cvv) == 3 or self.cvv == 4):
    #         raise ValidationError('CVV is invalid')    

    def luhns(card_number):
        
        #check if card number is numeric
        if not card_number.isnumeric():
            return -1
        else: 
            card_number = int(card_number)

        digits = [int(x) for x in str(card_number)]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(int(x) for x in str(d*2))
        return checksum % 10


      #todo: add code that determines type of credit card
    def validateCardNumber():
        if luhns(self.card_number) != 0:
            raise ValidationError('Card number is invalid')


    
    name = StringField('Enter name', validators=[DataRequired(message = "Enter your name please"), Length(max=60)])
    card_number = StringField('Enter card number', validators=[DataRequired(), Length(min=14, max=20)])
    cvv = StringField('Enter cvv', validators=[DataRequired() , Length(min=3, max=4)])
    expiry_date = DateTimeField('Enter expiry date (mm/YYYY)', validators=[DataRequired()], format='%m/%Y')
    submit = SubmitField('Submit')

    def validate_name(self, name):
        excluded_chars = "*?!'^+%&/()=}][{$#£"
        for char in self.name.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")
                    