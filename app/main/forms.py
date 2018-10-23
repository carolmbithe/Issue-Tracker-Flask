from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,RadioField,SelectField,SubmitField
from wtforms.validators import Required, Email
from ..models import User,Ticket,Role
from wtforms import ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField


def user_query():
    user =  User.query.filter_by(role_id=2)
    return user

def get_pk(obj):
    return str(obj)

def role_query():
    return Role.query

class TicketForm(FlaskForm):
    subject = StringField('Ticket Subject',validators=[Required()])
    description = StringField('Ticket Description', validators=[Required()])
    severity = RadioField('Severity',validators=[Required()],choices=[('low','Low'),('medium','Medium'),('high','High')])
    technician = QuerySelectField('Choose Technician',query_factory=user_query,allow_blank=True,get_pk=get_pk, validators=[Required()])
    submit = SubmitField('Submit Ticket')

class UpdateUserForm(FlaskForm):
    username = StringField('Username',validators=[Required()])
    firstname = StringField('First Name',validators=[Required()])
    lastname = StringField('Last Name', validators=[Required()])
    email = StringField('Email', validators=[Email(), Required()])
    role = QuerySelectField('Role', validators=[Required()],query_factory=role_query,allow_blank=True,get_pk=get_pk)
    submit = SubmitField('Update User')
