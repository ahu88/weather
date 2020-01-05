#not using any modules from the package itself (pip install) so imports remain same
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#import user model for validation of unique users
from weather_app.models import City

#simple form with a 2 fields for creating posts
class AddForm(FlaskForm):
    name = StringField('Add a City', validators=[DataRequired()]) 
    
    #submit button
    submit1 = SubmitField('Add')
    
    ######### DOESN'T WORK WHY ######################################################## 
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


#custom validation to ensure each user is unique (if username/email is already taken) - FORMAT
    #def validate_field(self, field):  #"field" is the field name (e.g. username, email, password...)
        #if True: #a conditional
            #raise ValidationError('Validation Message')