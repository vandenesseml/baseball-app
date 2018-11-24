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
        enrollment = datetime.datetime.strptime(self.enrollment_date,
                                                '%m/%d/%Y')
        now = datetime.now()
        return math.floor((now - dob).days / 365)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
