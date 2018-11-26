import math
from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    image_path = db.Column(db.String(1000))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    full_name = db.Column(db.String(240))

    def edit_profile_image(self, image_path):
        self.image_path = image_path

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size, first_name, last_name):
        return 'https://ui-avatars.com/api/?size={}&name={}+{}'.format(
            size, first_name, last_name)


class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    # in format mm/dd/yyyy
    DOB = db.Column(db.String(11))
    enrollment_date = db.Column(db.String(11))
    scholarship_amount = db.Column(db.Integer)
    country_of_origin = db.Column(db.String(120))
    university_name = db.Column(db.String(120))
    image_path = db.Column(db.String(1000))

    def get_age(self):
        dob = datetime.strptime(self.DOB, '%m/%d/%Y')
        now = datetime.now()
        return math.floor((now - dob).days / 365)

    def get_years_played(self):
        enrollment = datetime.strptime(self.enrollment_date, '%m/%d/%Y')
        now = datetime.now()
        return '{} years'.format(math.floor((now - enrollment).days / 365))

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '<Athlete {}>'.format(self.get_full_name())


class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university_name = db.Column(db.String(120))
    university_mascot = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    field_name = db.Column(db.String(120))
    athletes = db.relationship('Athlete', backref='university', lazy='dynamic')
    staff = db.relationship('Staff', backref='university', lazy='dynamic')
    conference_name = db.relationship(
        'Conference', backref='university', lazy='dynamic')

    def __repr__(self):
        return '<University {}>'.format(self.university_name)

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    # in format mm/dd/yyyy
    DOB = db.Column(db.String(11))
    start_date = db.Column(db.String(11))
    job_title = db.Column(db.String(120))
    university_name = db.relationship(
        'University', backref='staff', lazy='dynamic')

    def get_age(self):
        dob = datetime.strptime(self.DOB, '%m/%d/%Y')
        now = datetime.now()
        return math.floor((now - dob).days / 365)

    def get_years_at_university(self):
        enrollment = datetime.strptime(self.enrollment_date, '%m/%d/%Y')
        now = datetime.now()
        return '{} years'.format(math.floor((now - enrollment).days / 365))

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '<Staff {}>'.format(self.get_full_name())

class conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conference_name = db.Column(db.String(120))
    universities = db.relationship('University', backref='conference', lazy='dynamic')

    def __repr__(self):
        return '<Conference {}>'.format(self.conference_name())


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
