from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,ValidationError,RadioField
from wtforms.validators import Required,Email
from ..models import User,Ticket,Role
from wtforms import ValidationError
import wtforms_sqlalchemy.fields as f
from wtforms_sqlalchemy.fields import QuerySelectField


def get_pk_from_identity(obj):
   cls, key = f.identity_key(instance=obj)[:2]
   return ':'.join(f.text_type(x) for x in key)
f.get_pk_from_identity = get_pk_from_identity

def user_query():
   users = User.query.filter_by(role_id = 2).all()
   return users

def role_query():
   return Role.query

class TicketForm(FlaskForm):
   subject = StringField('Ticket Subject',validators=[Required()])
   description = StringField('Ticket Description', validators=[Required()])
   severity = RadioField('Severity',validators=[Required()],choices=[('low','Low'),('medium','Medium'),('high','High')])
   technician = QuerySelectField('Choose Technician',query_factory=user_query,allow_blank=True,validators=[Required()])
   submit = SubmitField('Submit Ticket')
