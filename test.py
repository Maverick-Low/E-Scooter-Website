import os
import unittest
from flask import request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Should allow valid user to register i.e. redirects to correct page and user gets added to db
    def test_register_user_correct_1(self):
        tester = app.test_client(self)
        response = tester.post('/register', data = dict(username="Tester", email="test1@gmail.com", password_1="Testtest1", password_2="Testtest1"), follow_redirects=True)
        user_obj = models.User.query.filter_by(email="test1@gmail.com").first()
        self.assertTrue(user_obj) # checks user is in database
        self.assertIn(b"Dashboard!", response.data) # checks user has been redirected to dashboard

    def test_login_user_correct_1(self):
        tester = app.test_client(self)
        tester.post('/register', data = dict(username="Tester", email="test1@gmail.com", password_1="Testtest1", password_2="Testtest1"), follow_redirects=True)
        response = tester.post('/', data = dict(email="test1@gmail.com", password="Testtest1"), follow_redirects=True)
        self.assertIn(b"Dashboard!", response.data)

    # Should allow valid user to register i.e. redirects to correct page and user gets added to db
    def test_register_user_correct_2(self):
        tester = app.test_client(self)
        response = tester.post('/register', data = dict(username="Hap", email="happy@gmail.com", password_1="Testtest1", password_2="Testtest1"), follow_redirects=True)
        user_obj = models.User.query.filter_by(email="happy@gmail.com").first()
        self.assertTrue(user_obj) # checks user is in database
        self.assertIn(b"Dashboard!", response.data) # checks user has been redirected to dashboard

    # Should not allow two users with the same email address
    def test_register_user_incorrect_1(self):
        tester = app.test_client(self)
        tester.post('/register', data = dict(username="Tester", email="test1@gmail.com", password_1="Testtest1", password_2="Testtest1"), follow_redirects=True)
        response = tester.post('/register', data = dict(username="Tester", email="test1@gmail.com", password_1="Testtest1", password_2="Testtest1"), follow_redirects=True)
        user_count = models.User.query.filter_by(email="test1@gmail.com").count()
        self.assertEqual(user_count, 1)
        # self.assertIn(b"Register!", response.data)
        # self.assertIn(b"Confirm password", response.data)

    # Should not allow invalid email address 1
    def test_register_user_incorrect_2(self):
        tester = app.test_client(self)
        response = tester.post('/register', data = dict(username="Tester", email="blahemail@com", password_1="Testtest1*", password_2="Testtest1*"), follow_redirects=True)
        self.assertIn(b"Register!", response.data)
        self.assertIn(b"Confirm password", response.data)

    # Should not allow invalid email address 2
    def test_register_user_incorrect_3(self):
        tester = app.test_client(self)
        response = tester.post('/register', data = dict(username="Tester", email="blahemail.com", password_1="Testtest1*", password_2="Testtest1*"), follow_redirects=True)
        self.assertIn(b"Register!", response.data)
        self.assertIn(b"Confirm password", response.data)

    # Should not allow password with less than 8 characters
    def test_register_user_incorrect_4(self):
        tester = app.test_client(self)
        response = tester.post('/register', data = dict(username="Tester", email="test2@gmail.com", password_1="Tab1", password_2="Tab1"), follow_redirects=True)
        self.assertIn(b"Register!", response.data)
        self.assertIn(b"Confirm password", response.data)

    # Should not allow password with no numerical digit
    def test_register_user_incorrect_5(self):
        tester = app.test_client(self)
        response = tester.post('/register', data = dict(username="Tester", email="test3@gmail.com", password_1="Testttttt", password_2="Testttttt"), follow_redirects=True)
        self.assertIn(b"Register!", response.data)
        self.assertIn(b"Confirm password", response.data)

    # Should not allow password with no capital letter
    def test_register_user_incorrect_6(self):
        tester = app.test_client(self)
        response = tester.post('/register', data = dict(username="Tester", email="test4@gmail.com", password_1="testword99", password_2="testword99"), follow_redirects=True)
        self.assertIn(b"Register!", response.data)
        self.assertIn(b"Confirm password", response.data)
    
    # Should not allow user with null username to register
    def test_register_user_incorrect_7(self):
        tester = app.test_client(self)
        response = tester.post('/register', data = dict(username="", email="test5@gmail.com", password_1="Testtest1", password_2="Testtest1"), follow_redirects=True)
        self.assertIn(b"Register!", response.data)
        self.assertIn(b"Confirm password", response.data)

    # Should not allow user to register if passwords don't match
    def test_register_user_incorrect_8(self):
        tester = app.test_client(self)
        response = tester.post('/register', data = dict(username="Testo", email="test6@gmail.com", password_1="Testtest1", password_2="Testtest2"), follow_redirects=True)
        self.assertIn(b"Register!", response.data)
        self.assertIn(b"Confirm password", response.data)
    

        
if __name__ == '__main__':
    unittest.main()

