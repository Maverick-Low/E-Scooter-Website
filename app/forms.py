from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateField, IntegerField, SubmitField
from wtforms.validators import EqualTo, DataRequired, ValidationError, Length, Email
from app import models
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


        #todo: finish function
        """
        #function that validates the password when registering a new user
        def validatePassword(self, password_1):
            
            #list of rules that a candidate password must meet
            rules = [lambda password : any(c.isupper() for c in password),
                     lambda password : any(c.islower() for c in password),
                     lambda password : any(c.isdigit() for c in password),
                     lambda password : len(password) >= 8,
                     lambda passowrd : 
            ]

            if len(password_1) < 8:
                raise ValidationError('The password is too short!')
            
            """
                