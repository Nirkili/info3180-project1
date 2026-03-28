from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField, IntegerField, SelectField
from wtforms.validators import InputRequired
from flask_wtf.file import FileRequired, FileAllowed

class PropertyForm(FlaskForm):
    
    title = StringField('Title', validators=[InputRequired()])
    desc = TextAreaField('Description', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    choices = [('House', 'House'), ('Apartment', 'Apartment'),]
    price = IntegerField('Price', validators=[InputRequired()])
    ptype = SelectField('Select Type', choices=choices , validators= [InputRequired()])
    numBaths = IntegerField('No. of Bathrooms', validators= [InputRequired()])
    numRooms = IntegerField('No. of Rooms', validators= [InputRequired()])
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpeg','jpg','png'])])