from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Players, Characters, Campaigns, Instances
from flask_login import current_user
#--------------------------------------------------------------------------------------------
#Character creation form
class CharacterForm(FlaskForm):
    character_first_name = StringField('Character First Name',
        validators= [
            DataRequired(),
            Length(min=2,max=15)
        ])
    character_last_name = StringField('Character Last Name',
        validators= [
            Length(max=15)
        ])
    character_background = StringField('Character Background',
        validators= [
            Length(max=250)
        ])
    submit = SubmitField('Create')
#--------------------------------------------------------------------------------------------
#Campaign creation form
class CampaignForm(FlaskForm):
    campaign_name = StringField('Campaign title',
        validators= [
            DataRequired(),
            Length(min=4, max=30)
        ])
    setting = StringField('Campaign setting',
        validators= [
            DataRequired()
        ])
    submit = SubmitField('Create')
#--------------------------------------------------------------------------------------------
#Instance creation form
class InstanceForm(FlaskForm):
    charchoices = Characters.query.all
    campchoices = Campaigns.query.all

    instance_name = StringField('Instance name',
        validators= [
            DataRequired(),
            Length(min=3, max=30)
        ])
    instance_location = StringField('Game location',
        validators= [
            DataRequired(),
            Length(min=25)
        ])
    campaign_id = SelectField(campchoices)
    character_id = SelectField(charchoices)
    submit = SubmitField('Create')
#--------------------------------------------------------------------------------------------
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
        validators = [
            DataRequired(),
            Length(min=2, max=30)
        ]
    )
    last_name = StringField('Last Name',
        validators = [
            DataRequired(),
            Length(min=2, max=30)
        ]
    )
    email = StringField('Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField('Password',
        validators = [
            DataRequired(),
        ]
    )
    confirm_password = PasswordField('Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        player = Players.query.filter_by(email=email.data).first()

        if player:
            raise ValidationError('Email already in use.')
#--------------------------------------------------------------------------------------------
class LoginForm(FlaskForm):
    email = StringField('Email',
    validators=[
        DataRequired(),
        Email()
        ]
    )

    password = PasswordField('Password',
    validators=[
        DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
#--------------------------------------------------------------------------------------------
class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    last_name = StringField('Last Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ])
    submit = SubmitField('Update')

    def validate_email(self,email):
        if email.data != current_user.email:
            player = Players.query.filter_by(email=email.data).first()
            if player:
                raise ValidationError('Email already in use')
#--------------------------------------------------------------------------------------------