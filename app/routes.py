import hashlib
import os
from datetime import datetime
import copy
import json
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from sqlalchemy.sql import text
from app import app, db
from app.forms import EditProfileForm, FantasyForm, LoginForm, RegistrationForm
from app.models import Athlete, Conference, Fantasy, Staff, University, User, PitcherCareerStats, PositionPlayerCareerStats
from config import Config
athletes, universities, countries = [], [], []
conference_choice, university_choice, country_choice, bats_choice, throws_choice, years_choice, athlete_weight = '', '', '', '', '', '', '' 

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # SELECT * FROM fantasy WHERE fantasy.user_id = ?
    fantasy_team= db.session.query(Fantasy).filter(Fantasy.user_id==current_user.id).first()
    return render_template("index.html", fantasy_team=fantasy_team)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username==form.username.data).first()
        
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
    user = db.session.query(User).filter(User.username==username).first_or_404()
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
    athlete = db.session.query(Athlete).filter(Athlete.id==id).first_or_404()
    stats = db.session.query(PositionPlayerCareerStats).filter(PositionPlayerCareerStats.athlete_id==athlete.id).first()
    if not stats:
        stats = db.session.query(PitcherCareerStats).filter(PitcherCareerStats.athlete_id==athlete.id).first()
    return render_template(
        'athlete.html', athlete=athlete, stats=stats, title=athlete.get_full_name())


@app.route('/university/<id>')
@login_required
def university(id):
    university = db.session.query(University).filter(University.id==id).first_or_404()
    return render_template(
        'university.html', university=university, title=university.name)


@app.route('/staff/<id>')
@login_required
def staff(id):
    staff = db.session.query(Staff).filter(Staff.id==id).first_or_404()
    return render_template(
        'staff.html', staff=staff, title=staff.get_full_name())


@app.route('/conference/<id>')
@login_required
def conference(id):
    conference = db.session.query(Conference).filter(Conference.id==id).first_or_404()
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
    # SELECT * FROM fantasy WHERE fantasy.user_id = ? 
    fantasyTeam = db.session.query(Fantasy).filter(Fantasy.user_id==current_user.id).first()
    fantasyForm = FantasyForm()
    query  = []
    global athletes, countries, universities, university_choice, country_choice
    conferences = Conference.query.all()
    countries = db.session.query(Athlete.country_of_origin).group_by(Athlete.country_of_origin).all()
    universities = db.session.query(University.id,University.name).all()
    for conference in conferences:
        fantasyForm.conference.choices.append((conference.id, conference.name))
        fantasyForm.conference_attr.choices.append((conference.id, conference.name))
    for country in countries:
        fantasyForm.country_attr.choices.append((country[0],country[0]))
    for id, name in universities:
        fantasyForm.university_attr.choices.append((id,name))

    if fantasyForm.submit_attr.data:
        # check if conference has been selected
        if fantasyForm.conference_attr.data:
            # SELECT * FROM athlete JOIN university ON university.id = athlete.university_id WHERE athlete.university_id = university.id AND university.conference_id = ? ***Complex
            athletes = db.session.query(Athlete).join(University).filter(Athlete.university_id==University.id).filter(University.conference_id==fantasyForm.conference_attr.data).all()
        else:    
            athletes = Athlete.query.all()
        if fantasyForm.university_attr.data:
            # SELECT * FROM athlete WHERE athlete.university_id = ?
            athletes = db.session.query(Athlete).filter(Athlete.university_id==(University.query.get(fantasyForm.university_attr.data)).id).all()
            athlete_ids=[]
            
            
        athlete_ids = []
        for athlete in athletes:
            athlete_ids.append(athlete.id)

# build query Strings
        if str(fantasyForm.university_attr.data) != 'None' and str(fantasyForm.university_attr.data) != '0':
            query.append('Athlete.university_id == "{}"'.format(fantasyForm.university_attr.data))
        if str(fantasyForm.throws_attr.data) != 'None' and str(fantasyForm.throws_attr.data) != '0':
            # SELECT * FROM athlete WHERE athlete.university_id = ? AND athlete.country_of_origin = ?, AND athlete.weight >= ?, AND athlete.weight <= ?, AND athlete.position = ?,  AND athlete.bats = ?, AND athlete.throws= ?
            # athletes = db.session.query(Athlete).filter(Athlete.university_id==(University.query.get(fantasyForm.university_attr.data)).id, Athlete.country_of_origin==fantasyForm.country_attr.data, Athlete.weight >= athlete_weight['min'], Athlete.weight <= athlete_weight['max'], Athlete.position == fantasyForm.position_attr.data, Athlete.bats == fantasyForm.bats_attr.data,  Athlete.throws == fantasyForm.throws_attr.data).all()
            query.append('Athlete.throws == "{}"'.format(fantasyForm.throws_attr.data))
        if str(fantasyForm.bats_attr.data) != 'None' and str(fantasyForm.bats_attr.data) != '0':
            # SELECT * FROM athlete WHERE athlete.university_id = ? AND athlete.country_of_origin = ?, AND athlete.weight >= ?, AND athlete.weight <= ?, AND athlete.position = ?, AND athlete.bats = ?
            # athletes = db.session.query(Athlete).filter(Athlete.university_id==(University.query.get(fantasyForm.university_attr.data)).id, Athlete.country_of_origin==fantasyForm.country_attr.data, Athlete.weight >= athlete_weight['min'], Athlete.weight <= athlete_weight['max'], Athlete.position == fantasyForm.position_attr.data, Athlete.bats == fantasyForm.bats_attr.data).all()
            query.append('Athlete.bats == "{}"'.format(fantasyForm.bats_attr.data))
        if str(fantasyForm.position_attr.data) != 'None' and str(fantasyForm.position_attr.data) != '0':
            # SELECT * FROM athlete WHERE athlete.university_id = ? AND athlete.country_of_origin = ?, AND athlete.weight >= ?, AND athlete.weight <= ?, AND athlete.position = ?
            # athletes = db.session.query(Athlete).filter(Athlete.university_id==(University.query.get(fantasyForm.university_attr.data)).id, Athlete.country_of_origin==fantasyForm.country_attr.data, Athlete.weight >= athlete_weight['min'], Athlete.weight <= athlete_weight['max'], Athlete.position == fantasyForm.position_attr.data).all()
            query.append('Athlete.position == "{}"'.format(fantasyForm.position_attr.data))
        if str(fantasyForm.weight_attr.data) != 'None' and str(fantasyForm.weight_attr.data) != '0':
            athlete_weight = json.loads(fantasyForm.weight_attr.data.replace('\'','"'))
            # SELECT * FROM athlete WHERE athlete.university_id = ? AND athlete.country_of_origin = ? AND athlete.weight >= ? AND athlete.weight <= ?
            # athletes = db.session.query(Athlete).filter(Athlete.university_id==(University.query.get(fantasyForm.university_attr.data)).id, Athlete.country_of_origin==fantasyForm.country_attr.data, Athlete.weight >= athlete_weight['min'], Athlete.weight <= athlete_weight['max']).all()
            query.append(' Athlete.weight >= "{}"'.format(athlete_weight['min']))
            query.append('Athlete.weight <= "{}"'.format(athlete_weight['max']))
        if str(fantasyForm.country_attr.data) != 'None' and str(fantasyForm.country_attr.data) != '0':
            # SELECT * FROM athlete WHERE athlete.university_id = ? AND athlete.country_of_origin = ?
            query.append('Athlete.country_of_origin=="{}"'.format(fantasyForm.country_attr.data)) 
            query.append('Athlete.university_id=="{}"'.format(fantasyForm.university_attr.data))
        if str(fantasyForm.appearances.data) != 'None' and str(fantasyForm.appearances.data) != '0':
            appearances = json.loads(fantasyForm.appearances.data.replace('\'','"'))
            athlete_ids = db.session.query(PitcherCareerStats.athlete_id,PitcherCareerStats.appearances).filter(PitcherCareerStats.appearances >= appearances['min'], PitcherCareerStats.appearances <= appearances['max']).all() 
            if athlete_ids:
                q='('
                for index in range(0,len(athlete_ids)):
                    if index == len(athlete_ids) -1:
                        q = q + ' Athlete.id==' + str(athlete_ids[index][0]) + ')'
                    else:
                        q = q + ' Athlete.id==' + str(athlete_ids[index][0]) + ' OR'
                query.append(q)
            else:
                query.append('Athlete.id==199999999999933333333333')
        if str(fantasyForm.innings_thrown.data) != 'None' and str(fantasyForm.innings_thrown.data) != '0':
            innings_thrown = json.loads(fantasyForm.innings_thrown.data.replace('\'','"'))
            athlete_ids = db.session.query(PitcherCareerStats.athlete_id,PitcherCareerStats.innings_thrown).filter(PitcherCareerStats.innings_thrown >= innings_thrown['min'], PitcherCareerStats.innings_thrown <= innings_thrown['max']).all() 
            if athlete_ids:
                q='('
                for index in range(0,len(athlete_ids)):
                    if index == len(athlete_ids) -1:
                        q = q + ' Athlete.id==' + str(athlete_ids[index][0]) + ')'
                    else:
                        q = q + ' Athlete.id==' + str(athlete_ids[index][0]) + ' OR'
                query.append(q)
            else:
                query.append('Athlete.id==199999999999933333333333')
        # Submit query
        
        athletes = db.session.query(Athlete).filter(*query).all()
        

    
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
        conference = db.session.query(Conference).filter(Conference.id==id).first()
        fantasyTeam.conference=conference
        db.session.commit() 
        flash('Your fantasy team profile has been created!')
    
    if fantasyForm.add_player.data: 
        athlete=db.session.query(Athlete).filter(Athlete.id==fantasyForm.athlete_add.data).first()
        athlete.fantasy_id=fantasyTeam.id
        db.session.commit()
        flash('You adde {} to your fantasy team!'.format(athlete.get_full_name()))
    if fantasyForm.remove_player.data: 
        athlete=db.session.query(Athlete).filter(Athlete.id==fantasyForm.athlete_remove.data).first()
        athlete.fantasy_id=''
        db.session.commit()
        flash('You removed {} from your fantasy team!'.format(athlete.get_full_name()))
    return render_template(
        'fantasy.html',
        title='Fantasy Team',
        fantasyTeam=fantasyTeam,
        fantasyForm=fantasyForm, athletes=athletes)
