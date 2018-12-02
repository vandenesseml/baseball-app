import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@35.231.60.133/baseball-app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    POST_IMAGE_UPLOAD_FOLDER = './app/static/uploads/post/'
    POST_IMAGE_ACCESS_PATH = '/static/uploads/post/'
    PROFILE_IMAGE_UPLOAD_FOLDER = './app/static/uploads/profile/'
    PROFILE_IMAGE_ACCESS_PATH = '/static/uploads/profile/'
    FANTASY_TEAM_IMAGE_UPLOAD_FOLDER = './app/static/uploads/fantasy'
    FANTASY_TEAM_IMAGE_ACCESS_PATH = '/static/uploads/fantasy/'
    POSTS_PER_PAGE = 10
    COMMENTS_PER_POST = 5