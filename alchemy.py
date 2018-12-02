from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import enum
import math
from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from sqlalchemy import Enum, Integer
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@35.231.60.133/baseball-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'User'
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
