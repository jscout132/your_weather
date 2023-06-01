from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired, Email

class UserLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')

class CreateUser(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    user_city = StringField('User City')
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')

class AddFavCity(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    submit_button = SubmitField('Save this city')

class DelFavCity(FlaskForm):
    submit_button = SubmitField('Delete this city')
