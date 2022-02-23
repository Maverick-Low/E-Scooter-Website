from audioop import reverse
from time import strftime
from unicodedata import name
from venv import CORE_VENV_DEPS
from wsgiref.validate import validator
# from app.test import luhns
from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import PasswordField, StringField, DateField, IntegerField, SubmitField, DateTimeField
from wtforms.validators import EqualTo, DataRequired, ValidationError, Length, Email, NumberRange
from app import models
from datetime import date, datetime
import re
from flask import flash


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
    def validate_email(self, email):     
        user_object = models.User.query.filter_by(email=email.data).first()
        if user_object: #if user is already registered don't allow them to register again
            raise ValidationError('This email address is already registered!')
            
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
   
    # def validate_expiry_date(self, expiry_date_year):
    #     today = datetime.now()  
    #     today.strftime('%m/%Y')
    #     if self.expiry_date < today:
    #         raise ValidationError('Your card has expired')

        
    
    
    #function inspired by (Allwin Raju, 2020) available at:
    # https://allwin-raju-12.medium.com/credit-card-number-validation-using-luhns-algorithm-in-python-c0ed2fac6234 
    

  
