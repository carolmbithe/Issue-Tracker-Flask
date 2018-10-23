from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Ticket,Role
from .. import db,photos
from .forms import TicketForm, UpdateUserForm
from flask_login import login_required,current_user
import datetime

# Views
@main.route('/')
@login_required
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home - Welcome to Perfect Pitch'
    if current_user.role_id == 1:
        return redirect(url_for('.admin'))
    elif current_user.role_id == 2:
        return redirect(url_for('.technician'))
    else:
        return redirect(url_for('.requester'))

    return render_template('index.html',title = title)

@main.route('/admin')
@login_required
def admin():
    open_tickets_list = Ticket.query.filter_by(status = 'open').order_by(Ticket.id.desc()).limit(10)
    progress_tickets_list = Ticket.query.filter_by(status = 'progress').order_by(Ticket.id.desc()).limit(10)
    closed_tickets_list = Ticket.query.filter_by(status = 'closed').order_by(Ticket.id.desc()).limit(10)

    return render_template('admin.html', open_tickets_list = open_tickets_list,progress_tickets_list = progress_tickets_list, closed_tickets_list = closed_tickets_list)

@main.route('/technician', methods=['GET','POST'])
def technician():
    form = TicketForm()
    if form.validate_on_submit():
        new_ticket = Ticket(ticket_title = form.subject.data,ticket_description = form.description.data, severity = form.severity.data, user_id = current_user, assigned_to = form.technician.data)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('.technician'))
    return render_template('technician.html', form = form)

@main.route('/requester', methods=['GET','POST'])
def requester():
    form = TicketForm()
    if form.validate_on_submit():
        print(form.technician.data, form.subject.data, form.severity.data)
        new_ticket = Ticket(ticket_title = form.subject.data,ticket_description = form.description.data, severity = form.severity.data, user_id = current_user, assigned_to = form.technician.data)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('.requester'))
    return render_template('requester.html', form= form)

@main.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html',users = users)

@main.route('/user/<int:id>/update', methods = ['GET','POST'])
def update_user(id):
    form = UpdateUserForm()
    user = User.query.filter_by(id=id).first()
    if form.validate_on_submit():
        user.username = form.username.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        return redirect(url_for('main.users'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.email.data = user.email
        form.role.data = user.role

    return render_template('user.html',form = form)
