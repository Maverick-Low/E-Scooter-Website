from audioop import reverse
from unicodedata import name
from venv import CORE_VENV_DEPS
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateField, IntegerField, SubmitField
from wtforms.validators import EqualTo, DataRequired, ValidationError, Length, Email
from app import models
from datetime import date
import re


class Login(FlaskForm):
    email = StringField('Enter email', validators=[DataRequired(), Length(max=60)])
    password = PasswordField('Enter password', validators=[DataRequired(), Length(max=60)])
    submit = SubmitField('Submit')


class Registration(FlaskForm):
    username = StringField('Enter username', validators=[DataRequired(), Length(max=60)])
    email = StringField('Enter email', validators=[DataRequired(), Length(max=60), Email()])
    password_1 = PasswordField('Enter password', validators=[DataRequired(), Length(max=60)])
    password_2 = PasswordField('Confirm password', validators=[DataRequired(), Length(max=60), EqualTo('password_1', message='Passwords must match!')])
    submit = SubmitField('Submit')

    # function that validates email adress upon registration
    # todo: write unit tests for functions
    def validateEmail(self, email):     
        user_object = models.User.query.filter_by(email=email.data).first()
        if user_object: #if user is already registered don't allow them to register again
            raise ValidationError('This email address is already registered!')

        #regular expression for an email address with a single '.' after the '@':    
        email_regex_1 = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        #regular expression for an email address with two '.'s after the '@': 
        email_regex_2 = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}+\.[A-Z|a-z]{2,}\b'
        
        if not( (re.fullmatch(email_regex_1,email)) or (re.fullmatch(email_regex_2)) ):
                raise ValidationError('This email is not of a valid format!')

class Payment(FlaskForm):
    card_number = IntegerField('Enter card number', validators=[DataRequired(), Length(max=20)])
    cvv = IntegerField('Enter cvv', validators=[DataRequired(), Length(max=5)])
    expiry_date = DateField('Enter expiry date', validators=[DataRequired()])
    submit = SubmitField('Submit')
   
    #function that checks if the expiry date is in the future
    def validateExpiryDate(self, expiry_date):
        today = date.today()
        if expiry_date < today:
            raise ValidationError('Your card has expired')


    def validateCVV(self, cvv):
        if len(cvv) > 4:
            raise ValidationError('CVV is invalid')        
    
    
    #function inspired by (Allwin Raju, 2020) available at:
    # https://allwin-raju-12.medium.com/credit-card-number-validation-using-luhns-algorithm-in-python-c0ed2fac6234 
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
    def validateCardNumber(self, card_number):
        if luhns(card_number) != 0:
            raise ValidationError('Card number is invalid')

