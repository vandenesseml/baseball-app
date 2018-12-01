import hashlib
import os
from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app, db
from app.forms import EditProfileForm, FantasyForm, LoginForm, RegistrationForm
from app.models import Athlete, Conference, Fantasy, Staff, University, User
from config import Config


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            full_name=form.first_name.data + ' ' + form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, title=user.full_name)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        if form.photo.data:
            photo = request.files['photo']
            filename = secure_filename(photo.filename)
            print(filename)
            extension = filename.split('.')[1]
            filename = str(
                hashlib.md5(filename.split('.')[0].encode()).hexdigest())
            filename = filename + '.' + extension
            photo.save(
                os.path.join(Config.PROFILE_IMAGE_UPLOAD_FOLDER, filename))
            current_user.image_path = os.path.join(
                Config.PROFILE_IMAGE_ACCESS_PATH, filename)
        db.session.commit()
        flash('Your profile changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template(
        'edit_profile.html', form=form, title=current_user.full_name)


@app.route('/athlete/<id>')
@login_required
def athlete(id):
    athlete = Athlete.query.filter_by(id=id).first_or_404()
    return render_template(
        'athlete.html', athlete=athlete, title=athlete.get_full_name())


@app.route('/university/<id>')
@login_required
def university(id):
    university = University.query.filter_by(id=id).first_or_404()
    return render_template(
        'university.html', university=university, title=university.name)


@app.route('/staff/<id>')
@login_required
def staff(id):
    staff = Staff.query.filter_by(id=id).first_or_404()
    return render_template(
        'staff.html', staff=staff, title=staff.get_full_name())


@app.route('/conference/<id>')
@login_required
def conference(id):
    conference = Conference.query.filter_by(id=id).first_or_404()
    return render_template(
        'conference.html', conference=conference, title=conference.name)


@app.route('/conferences')
@login_required
def conferences():
    conferences = Conference.query.all()
    return render_template(
        'conferences.html', conferences=conferences, title='Conferences')


@app.route('/fantasy', methods=['GET', 'POST'])
@login_required
def FantasyTeam():
    fantasyTeam = Fantasy.query.filter_by(user_id=current_user.id).first()
    fantasyForm = FantasyForm()
    athletes = []
    athlete_add = Athlete()
    conferences = Conference.query.all()
    fantasyForm.conference.choices.append((0, ''))
    for conference in conferences:
        fantasyForm.conference.choices.append((conference.id, conference.name))
        fantasyForm.conference_attr.choices.append((conference.id, conference.name))
        fantasyForm.conference_attr.choices.append((0, ''))
   
    if fantasyForm.submit_profile.data:
        photo = request.files['teamImage']
        filename = secure_filename(photo.filename)
        extension = filename.split('.')[1]
        filename = str(
            hashlib.md5(filename.split('.')[0].encode()).hexdigest())
        filename = filename + '.' + extension
        photo.save(
            os.path.join(Config.FANTASY_TEAM_IMAGE_UPLOAD_FOLDER, filename))
        fantasyTeam.image_path = os.path.join(
            Config.FANTASY_TEAM_IMAGE_ACCESS_PATH, filename)
        fantasyTeam.team_name=fantasyForm.team_name.data
        fantasyTeam.mascot=fantasyForm.mascot.data
        fantasyTeam.field_name=fantasyForm.field_name.data
        fantasyTeam.city=fantasyForm.city.data
        fantasyTeam.state=fantasyForm.state.data
        id = fantasyForm.conference.data
        conference = Conference.query.filter_by(id=id).first()
        fantasyTeam.conference=conference
        db.session.commit() 
        flash('Your fantasy team profile has been created!')
    if fantasyForm.submit_attr.data:
        if fantasyForm.conference_attr.data:
            # join athlete and university on athlete.university_id == university.id where university.conference_id == the selected conference id
            athletes = db.session.query(Athlete).join(University).filter(Athlete.university_id==University.id).filter(University.conference_id==fantasyForm.conference_attr.data).all()
    if fantasyForm.add_player.data: 
        athlete=Athlete.query.filter_by(id=fantasyForm.athlete.data).first()
        athlete.fantasy_id=fantasyTeam.id
        db.session.commit()
        flash('You adde {} to your fantasy team!'.format(athlete.get_full_name()))
    if fantasyForm.remove_player.data: 
        athlete=Athlete.query.filter_by(id=fantasyForm.athlete.data).first()
        athlete.fantasy_id=''
        db.session.commit()
        flash('You removed {} from your fantasy team!'.format(athlete.get_full_name()))
    return render_template(
        'fantasy.html',
        title='Fantasy Team',
        fantasyTeam=fantasyTeam,
        fantasyForm=fantasyForm, athletes=athletes, athlete_add=athlete_add)
