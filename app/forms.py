from flask_wtf import FlaskForm
from wtforms import (BooleanField, FileField, HiddenField, PasswordField,
                     StringField, SubmitField, TextAreaField, SelectField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=1500)])
    submit = SubmitField('Update')
    photo = FileField(label='Update Profile Image')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
class FantasyForm(FlaskForm):
    createTeam = SubmitField('Yes')
    teamImage = FileField('Team Image', [DataRequired])
    submit_profile = SubmitField('Update', [DataRequired])
    team_name = StringField('Team Name' ,[DataRequired])
    mascot = StringField('Mascot', [DataRequired])
    field_name = StringField('Field Name', [DataRequired])
    city = StringField('City', [DataRequired])
    state = StringField('State', [DataRequired])
    conference = SelectField('Conference', [DataRequired], coerce=int, choices=[(0,'---') ])
    
    submit_attr = SubmitField('Update', [DataRequired])
    add_player = SubmitField('Add')
    remove_player = SubmitField('Remove')
    athlete_add = HiddenField()
    athlete_remove = HiddenField()

    conference_attr = SelectField('Conference', [DataRequired()], coerce=int, choices=[(0,'---') ])
    university_attr = SelectField('University', coerce=int, choices=[(0,'---') ])
    country_attr  = SelectField('Country of Origin', choices=[(0,'---') ])
    weight_attr = SelectField('Weight', choices=[(0,'---'), ({"min":140,"max":150},'140-150'), ({"min":151,"max":160},'151-160'), ({"min":161,"max":170},'161-170'), ({"min":171,"max":180},'171-180'), ({"min":181,"max":190},'181-190'), ({"min":191,"max":200},'191-200'), ({"min":201,"max":210},'201-210'), ({"min":211,"max":220},'211-220'), ({"min":221,"max":230},'221-230'), ({"min":231,"max":240},'231-240'), ({"min":241,"max":250},'241-250'), ({"min":251,"max":260},'251-260'), ({"min":261,"max":270},'261-270'), ({"min":271,"max":280},'271-280'), ({"min":281,"max":290},'281-290'), ({"min":291,"max":300},'291-300')])
    bats_attr  = SelectField('Bats',  choices=[(0,'---'), ('R', 'R'), ('L', 'L'), ('S', 'S')])
    throws_attr  = SelectField('Throws',  choices=[(0,'---'), ('R', 'R'), ('L', 'L'), ('S', 'S')])
    throws_attr  = SelectField('Throws',  choices=[(0,'---'), ('R', 'R'), ('L', 'L'), ('S', 'S')])
    position_attr = SelectField('Position',  choices=[(0,'---'), ('P','P'), ('C','C'), ('INF','INF'), ('OF','OF')])
    highschool_attr = SelectField('High School',  coerce=int, choices=[(0,'---')])
    years_attr  = SelectField('Years Played',  coerce=int, choices=[(0,'---'), (1, '1'), (2, '2'), (3, '3'), (4, '4')])

    # position stats
    games_played = SelectField('Games Played', choices=[(0,'---'), ({"min":1,"max":20},'1-20'), ({"min":21,"max":40},'21-40'), ({"min":41,"max":60},'41-60'), ({"min":61,"max":80},'61-80'), ({"min":81,"max":100},'81-100'), ({"min":101,"max":120},'101-120'), ({"min":121,"max":140},'121-140'), ({"min":141,"max":160},'141-160'), ({"min":161,"max":180},'161-180'), ({"min":181,"max":200},'181-200'), ({"min":201,"max":220},'201-220'), ({"min":221,"max":240},'221-240'), ({"min":241,"max":260},'241-260'), ({"min":261,"max":280},'261-280'), ({"min":281,"max":300},'281-300'), ({"min":301,"max":320},'301-320')])
    innings_played = SelectField('Innings Played', choices=[(0,'---'), ({"min":1,"max":20},'1-20'), ({"min":21,"max":40},'21-40'), ({"min":41,"max":60},'41-60'), ({"min":61,"max":80},'61-80'), ({"min":81,"max":100},'81-100'), ({"min":101,"max":120},'101-120'), ({"min":121,"max":140},'121-140'), ({"min":141,"max":160},'141-160'), ({"min":161,"max":180},'161-180'), ({"min":181,"max":200},'181-200'), ({"min":201,"max":220},'201-220'), ({"min":221,"max":240},'221-240'), ({"min":241,"max":260},'241-260'), ({"min":261,"max":280},'261-280'), ({"min":281,"max":300},'281-300'), ({"min":301,"max":320},'301-320')])
    at_bats = SelectField('At Bats', choices=[(0,'---'), ({"min":1,"max":20},'1-20'), ({"min":21,"max":40},'21-40'), ({"min":41,"max":60},'41-60'), ({"min":61,"max":80},'61-80'), ({"min":81,"max":100},'81-100'), ({"min":101,"max":120},'101-120'), ({"min":121,"max":140},'121-140'), ({"min":141,"max":160},'141-160'), ({"min":161,"max":180},'161-180'), ({"min":181,"max":200},'181-200'), ({"min":201,"max":220},'201-220'), ({"min":221,"max":240},'221-240'), ({"min":241,"max":260},'241-260'), ({"min":261,"max":280},'261-280'), ({"min":281,"max":300},'281-300'), ({"min":301,"max":320},'301-320')])
    hits = SelectField('Hits', choices=[(0,'---'), ({"min":1,"max":20},'1-20'), ({"min":21,"max":40},'21-40'), ({"min":41,"max":60},'41-60'), ({"min":61,"max":80},'61-80'), ({"min":81,"max":100},'81-100'), ({"min":101,"max":120},'101-120'), ({"min":121,"max":140},'121-140'), ({"min":141,"max":160},'141-160'), ({"min":161,"max":180},'161-180'), ({"min":181,"max":200},'181-200'), ({"min":201,"max":220},'201-220'), ({"min":221,"max":240},'221-240'), ({"min":241,"max":260},'241-260'), ({"min":261,"max":280},'261-280'), ({"min":281,"max":300},'281-300'), ({"min":301,"max":320},'301-320')])
    walks = SelectField('Walks', choices=[(0,'---'), ({"min":1,"max":20},'1-20'), ({"min":21,"max":40},'21-40'), ({"min":41,"max":60},'41-60'), ({"min":61,"max":80},'61-80'), ({"min":81,"max":100},'81-100'), ({"min":101,"max":120},'101-120'), ({"min":121,"max":140},'121-140'), ({"min":141,"max":160},'141-160'), ({"min":161,"max":180},'161-180'), ({"min":181,"max":200},'181-200'), ({"min":201,"max":220},'201-220'), ({"min":221,"max":240},'221-240'), ({"min":241,"max":260},'241-260'), ({"min":261,"max":280},'261-280'), ({"min":281,"max":300},'281-300'), ({"min":301,"max":320},'301-320')])
    runs_scored = SelectField('Runs Scored', choices=[(0,'---'), ({"min":1,"max":20},'1-20'), ({"min":21,"max":40},'21-40'), ({"min":41,"max":60},'41-60'), ({"min":61,"max":80},'61-80'), ({"min":81,"max":100},'81-100'), ({"min":101,"max":120},'101-120'), ({"min":121,"max":140},'121-140'), ({"min":141,"max":160},'141-160'), ({"min":161,"max":180},'161-180'), ({"min":181,"max":200},'181-200'), ({"min":201,"max":220},'201-220'), ({"min":221,"max":240},'221-240'), ({"min":241,"max":260},'241-260'), ({"min":261,"max":280},'261-280'), ({"min":281,"max":300},'281-300'), ({"min":301,"max":320},'301-320')])
    runs_batted_in = SelectField('Runs Batted In', choices=[(0,'---'), ({"min":1,"max":20},'1-20'), ({"min":21,"max":40},'21-40'), ({"min":41,"max":60},'41-60'), ({"min":61,"max":80},'61-80'), ({"min":81,"max":100},'81-100'), ({"min":101,"max":120},'101-120'), ({"min":121,"max":140},'121-140'), ({"min":141,"max":160},'141-160'), ({"min":161,"max":180},'161-180'), ({"min":181,"max":200},'181-200'), ({"min":201,"max":220},'201-220'), ({"min":221,"max":240},'221-240'), ({"min":241,"max":260},'241-260'), ({"min":261,"max":280},'261-280'), ({"min":281,"max":300},'281-300'), ({"min":301,"max":320},'301-320')])
    home_runs = SelectField('Home Runs', choices=[(0,'---'), ({"min":1,"max":20},'1-20'), ({"min":21,"max":40},'21-40'), ({"min":41,"max":60},'41-60'), ({"min":61,"max":80},'61-80'), ({"min":81,"max":100},'81-100'), ({"min":101,"max":120},'101-120'), ({"min":121,"max":140},'121-140'), ({"min":141,"max":160},'141-160'), ({"min":161,"max":180},'161-180'), ({"min":181,"max":200},'181-200'), ({"min":201,"max":220},'201-220'), ({"min":221,"max":240},'221-240'), ({"min":241,"max":260},'241-260'), ({"min":261,"max":280},'261-280'), ({"min":281,"max":300},'281-300'), ({"min":301,"max":320},'301-320')])
    batting_average = SelectField('Batting Average', choices=[(0,'---'), ({"min":.1,"max":.20},'.1-.20'), ({"min":.21,"max":.40},'.21-.40'), ({"min":.41,"max":.60},'.41-.60'), ({"min":.61,"max":.80},'.61-.80'), ({"min":.81,"max":1.00},'.81-1.00'), ({"min":1.01,"max":1.20},'1.01-1.20'), ({"min":1.21,"max":1.40},'1.21-1.40'), ({"min":1.41,"max":1.60},'1.41-1.60'), ({"min":1.61,"max":1.80},'1.61-1.80'), ({"min":1.81,"max":2.00},'1.81-2.00'), ({"min":2.01,"max":2.20},'2.01-2.20'), ({"min":2.21,"max":2.40},'2.21-2.40'), ({"min":2.41,"max":2.60},'2.41-2.60'), ({"min":2.61,"max":2.80},'2.61-2.80'), ({"min":2.81,"max":3.00},'2.81-3.00'), ({"min":3.01,"max":3.20},'301-320'), ({"min":3.21,"max":3.40},'3.21-3.40'), ({"min":3.41,"max":3.60},'3.41-3.60'), ({"min":3.61,"max":3.80},'3.61-3.80'), ({"min":3.81,"max":4.00},'3.81-4.00')])

    # pitcher stats
    appearances = SelectField('Appearances', choices=[(0,'---'), ({"min":1,"max":20},'1-20'), ({"min":21,"max":40},'21-40'), ({"min":41,"max":60},'41-60'), ({"min":61,"max":80},'61-80'), ({"min":81,"max":100},'81-100'), ({"min":101,"max":120},'101-120'), ({"min":121,"max":140},'121-140'), ({"min":141,"max":160},'141-160'), ({"min":161,"max":180},'161-180'), ({"min":181,"max":200},'181-200'), ({"min":201,"max":220},'201-220'), ({"min":221,"max":240},'221-240'), ({"min":241,"max":260},'241-260'), ({"min":261,"max":280},'261-280'), ({"min":281,"max":300},'281-300'), ({"min":301,"max":320},'301-320')])
    innings_thrown  = SelectField('Innings Thrown', choices=[(0,'---'), ({"min":1,"max":20},'1-20'), ({"min":21,"max":40},'21-40'), ({"min":41,"max":60},'41-60'), ({"min":61,"max":80},'61-80'), ({"min":81,"max":100},'81-100'), ({"min":101,"max":120},'101-120'), ({"min":121,"max":140},'121-140'), ({"min":141,"max":160},'141-160'), ({"min":161,"max":180},'161-180'), ({"min":181,"max":200},'181-200'), ({"min":201,"max":220},'201-220'), ({"min":221,"max":240},'221-240'), ({"min":241,"max":260},'241-260'), ({"min":261,"max":280},'261-280'), ({"min":281,"max":300},'281-300'), ({"min":301,"max":320},'301-320')])
    runs_allowed  = SelectField('Runs Allowed', choices=[(0,'---'), ({"min":1,"max":20},'1-20'), ({"min":21,"max":40},'21-40'), ({"min":41,"max":60},'41-60'), ({"min":61,"max":80},'61-80'), ({"min":81,"max":100},'81-100'), ({"min":101,"max":120},'101-120'), ({"min":121,"max":140},'121-140'), ({"min":141,"max":160},'141-160'), ({"min":161,"max":180},'161-180'), ({"min":181,"max":200},'181-200'), ({"min":201,"max":220},'201-220'), ({"min":221,"max":240},'221-240'), ({"min":241,"max":260},'241-260'), ({"min":261,"max":280},'261-280'), ({"min":281,"max":300},'281-300'), ({"min":301,"max":320},'301-320')])
    earned_run_average  = SelectField('Earned Run Average', choices=[(0,'---'), ({"min":.1,"max":.20},'.1-.20'), ({"min":.21,"max":.40},'.21-.40'), ({"min":.41,"max":.60},'.41-.60'), ({"min":.61,"max":.80},'.61-.80'), ({"min":.81,"max":1.00},'.81-1.00'), ({"min":1.01,"max":1.20},'1.01-1.20'), ({"min":1.21,"max":1.40},'1.21-1.40'), ({"min":1.41,"max":1.60},'1.41-1.60'), ({"min":1.61,"max":1.80},'1.61-1.80'), ({"min":1.81,"max":2.00},'1.81-2.00'), ({"min":2.01,"max":2.20},'2.01-2.20'), ({"min":2.21,"max":2.40},'2.21-2.40'), ({"min":2.41,"max":2.60},'2.41-2.60'), ({"min":2.61,"max":2.80},'2.61-2.80'), ({"min":2.81,"max":3.00},'2.81-3.00'), ({"min":3.01,"max":3.20},'301-320'), ({"min":3.21,"max":3.40},'3.21-3.40'), ({"min":3.41,"max":3.60},'3.41-3.60'), ({"min":3.61,"max":3.80},'3.61-3.80'), ({"min":3.81,"max":4.00},'3.81-4.00')])
    strikeouts =SelectField('Strikeouts', choices=[(0,'---'), ({"min":1,"max":20},'1-20'), ({"min":21,"max":40},'21-40'), ({"min":41,"max":60},'41-60'), ({"min":61,"max":80},'61-80'), ({"min":81,"max":100},'81-100'), ({"min":101,"max":120},'101-120'), ({"min":121,"max":140},'121-140'), ({"min":141,"max":160},'141-160'), ({"min":161,"max":180},'161-180'), ({"min":181,"max":200},'181-200'), ({"min":201,"max":220},'201-220'), ({"min":221,"max":240},'221-240'), ({"min":241,"max":260},'241-260'), ({"min":261,"max":280},'261-280'), ({"min":281,"max":300},'281-300'), ({"min":301,"max":320},'301-320')])
    
    


