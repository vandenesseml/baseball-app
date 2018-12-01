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
    athlete = HiddenField()

    conference_attr = SelectField('Conference', [DataRequired], coerce=int, choices=[(0,'---') ])
    university_attr = SelectField('University', [DataRequired], coerce=int, choices=[(0,'---') ])
    country_attr  = SelectField('Country of Origin', [DataRequired], coerce=int, choices=[(0,'---') ])
    weight_attr = SelectField('Weight', [DataRequired], coerce=int, choices=[(0,'---'), (1,'140-150'), (2,'151-160'), (3,'161-170'), (4,'171-180'), (5,'181-190'), (6,'191-200'), (7,'201-210'), (8,'211-220'), (8,'221-230'), (9,'231-240'), (10,'241-250'), (11,'251-260'), (12,'261-270'), (13,'271-280'), (14,'281-290'), (15,'291-300')])
    bats_attr  = SelectField('Bats', [DataRequired], coerce=int, choices=[(0,'---'), (1, 'R'), (2, 'L'), (3, 'S')])
    throws_attr  = SelectField('Throws', [DataRequired], coerce=int, choices=[(0,'---'), (1, 'R'), (2, 'L'), (3, 'S')])
    highschool_attr = SelectField('High School', [DataRequired], coerce=int, choices=[(0,'---')])
    years_attr  = SelectField('Years Played', [DataRequired], coerce=int, choices=[(0,'---'), (1, '1'), (2, '2'), (3, '3'), (4, '4')])

    
    


