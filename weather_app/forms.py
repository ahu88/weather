#not using any modules from the package itself (pip install) so imports remain same
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#import user model for validation of unique users
from weather_app.models import City, User, cities

#simple form with a 2 fields for creating posts
class AddForm(FlaskForm):
    name = StringField('Add a City', validators=[DataRequired()]) 
    
    #submit button
    submit1 = SubmitField('Add')
    
    ######### pointless, in models there is no unique=true for this so no error will be encountered
    def validate_name(self, name): 
        print("VALIDATE", name.data)
        city = City.query.filter_by(name=name.data).first()
        if city:
            raise ValidationError('Duplicate City')

    """
    name_tmp = response['name']
    #print("yeet", name_tmp)

    temp = City.query.filter_by(name=name_tmp).first()
    
    if temp:
        flash('Duplicate city', 'danger')
    """

class DeleteForm(FlaskForm):
    name = StringField('Delete a City', validators=[DataRequired()]) #every post needs content
    
    #submit button
    submit2 = SubmitField('Delete')

    def validate_name(self, name): 
        city = City.query.filter_by(name=name.data).first()
        if city:
            raise ValidationError('Duplicate City')

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('That username is taken, please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That email is taken, please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


#custom validation to ensure each user is unique (if username/email is already taken) - FORMAT
    #def validate_field(self, field):  #"field" is the field name (e.g. username, email, password...)
        #if True: #a conditional
            #raise ValidationError('Validation Message')