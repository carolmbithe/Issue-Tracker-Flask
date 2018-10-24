from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,RadioField,SelectField,SubmitField
from wtforms.validators import Required, Email
from ..models import User,Ticket,Role
from wtforms import ValidationError
import wtforms_sqlalchemy.fields as f
from wtforms_sqlalchemy.fields import QuerySelectField


def get_pk_from_identity(obj):
<<<<<<< HEAD
    cls, key = f.identity_key(instance=obj)[:2]
    return ':'.join(f.text_type(x) for x in key)
f.get_pk_from_identity = get_pk_from_identity

def user_query():
    users = User.query.filter_by(role_id = 2).all()
    return users
=======
   cls, key = f.identity_key(instance=obj)[:2]
   return ':'.join(f.text_type(x) for x in key)
f.get_pk_from_identity = get_pk_from_identity

def user_query():
   users = User.query.filter_by(role_id = 2).all()
   return users
>>>>>>> d34dda4e3ef821b68006bb749ef0e0ca2ae64eb2

def role_query():
   return Role.query

class TicketForm(FlaskForm):
<<<<<<< HEAD
    subject = StringField('Ticket Subject',validators=[Required()])
    description = StringField('Ticket Description', validators=[Required()])
    severity = RadioField('Severity',validators=[Required()],choices=[('low','Low'),('medium','Medium'),('high','High')])
    technician = QuerySelectField('Choose Technician',query_factory=user_query,allow_blank=True,validators=[Required()])
    submit = SubmitField('Submit Ticket')
=======
   subject = StringField('Ticket Subject',validators=[Required()])
   description = StringField('Ticket Description', validators=[Required()])
   severity = RadioField('Severity',validators=[Required()],choices=[('low','Low'),('medium','Medium'),('high','High')])
   technician = QuerySelectField('Choose Technician',query_factory=user_query,allow_blank=True,validators=[Required()])
   submit = SubmitField('Submit Ticket')
>>>>>>> d34dda4e3ef821b68006bb749ef0e0ca2ae64eb2

class UpdateUserForm(FlaskForm):
    username = StringField('Username',validators=[Required()])
    firstname = StringField('First Name',validators=[Required()])
    lastname = StringField('Last Name', validators=[Required()])
    email = StringField('Email', validators=[Email(), Required()])
    role = QuerySelectField('Role', validators=[Required()],query_factory=role_query,allow_blank=True)
    submit = SubmitField('Update User')
