from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DateField, IntegerField, SubmitField, EmailField
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
                    