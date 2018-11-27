import enum
import math
from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from sqlalchemy import Enum, Integer
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

class bats_throws(enum.Enum):
    R = 'R'
    L = 'L'
    S = 'S'
class position(enum.Enum):
    P = 1
    ChildProcessError = 2
    INF = 3, 4, 5, 6
    OF = 7, 8, 9
class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    # in format mm/dd/yyyy
    DOB = db.Column(db.String(11))
    enrollment_date = db.Column(db.String(11))
    scholarship_amount = db.Column(db.Integer)
    country_of_origin = db.Column(db.String(120))
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    image_path = db.Column(db.String(1000))
    weight = db.Column(db.Integer)
    height = db.Column(db.String(20))
    bats = db.Column(Enum(bats_throws))
    throws = db.Column(Enum(bats_throws))
    position = db.Column(Enum(position))
    number = db.Column(db.Integer)
    high_school = db.Column(db.String(120))

    def get_age(self):
        dob = datetime.strptime(self.DOB, '%m/%d/%Y')
        now = datetime.now()
        return math.floor((now - dob).days / 365)

    def get_years_played(self):
        enrollment = datetime.strptime(self.enrollment_date, '%m/%d/%Y')
        now = datetime.now()
        years = math.floor((now - enrollment).days / 365)
        if years == 0:
            years = 1
            return '{} year'.format(years)
        return '{} years'.format(years)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '<Athlete {}>'.format(self.get_full_name())


class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    mascot = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    field_name = db.Column(db.String(120))
    athletes = db.relationship('Athlete', backref='university', lazy='dynamic')
    staff = db.relationship('Staff', backref='university', lazy='dynamic')
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'))
    image_path = db.Column(db.String(1000))

    def __repr__(self):
        return '<University {}>'.format(self.name)


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    # in format mm/dd/yyyy
    DOB = db.Column(db.String(11))
    start_date = db.Column(db.String(11))
    job_title = db.Column(db.String(120))
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    image_path = db.Column(db.String(1000))

    def get_age(self):
        dob = datetime.strptime(self.DOB, '%m/%d/%Y')
        now = datetime.now()
        return math.floor((now - dob).days / 365)

    def get_years_at_university(self):
        start_date = datetime.strptime(self.start_date, '%m/%d/%Y')
        now = datetime.now()
        years = math.floor((now - start_date).days / 365)
        if years == 0:
            years = 1
            return '{} year'.format(years)
        return '{} years'.format(years)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '<Staff {}>'.format(self.get_full_name())


class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    universities = db.relationship(
        'University', backref='conference', lazy='dynamic')
    image_path = db.Column(db.String(1000))

    def __repr__(self):
        return '<Conference {}>'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
