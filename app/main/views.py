from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Ticket,Role
from .. import db,photos
from .forms import TicketForm, UpdateUserForm, CreateUserForm
from flask_login import login_required,current_user
import datetime

# Views
@main.route('/')
@login_required
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home - Phoenix issue tracker'
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
    progress_tickets_list = Ticket.query.filter_by(status = 'inprogress').order_by(Ticket.id.desc()).limit(10)
    closed_tickets_list = Ticket.query.filter_by(status = 'closed').order_by(Ticket.id.desc()).limit(10)

    labels = ["Open","In progress","Closed"]

    values = []

    tickets = Ticket.query.all()

    open_count = 0
    progress_count = 0
    closed_count = 0

    for ticket in tickets:
        if ticket.status == 'open':
            open_count += 1
    values.append(open_count)

    for ticket in tickets:
        if ticket.status == 'inprogress':
            progress_count += 1
    values.append(progress_count)

    for ticket in tickets:
        if ticket.status == 'closed':
            closed_count += 1
    values.append(closed_count)

    return render_template('admin.html', open_tickets_list = open_tickets_list,progress_tickets_list = progress_tickets_list, closed_tickets_list = closed_tickets_list,labels = labels, values = values)

@main.route('/technician', methods=['GET','POST'])
@login_required
def technician():
    form = TicketForm()
    if form.validate_on_submit():
        new_ticket = Ticket(ticket_title = form.subject.data,ticket_description = form.description.data, severity = form.severity.data, user_id = current_user, assigned_to = form.technician.data)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('.technician'))
    return render_template('technician.html', form = form)

@main.route('/requester', methods=['GET','POST'])
@login_required
def requester():

    open_tickets_list = Ticket.query.filter_by(status = 'open', user_id = current_user.id).order_by(Ticket.id.desc()).limit(10)
    progress_tickets_list = Ticket.query.filter_by(status = 'inprogress', user_id = current_user.id).order_by(Ticket.id.desc()).limit(10)
    closed_tickets_list = Ticket.query.filter_by(status = 'closed', user_id = current_user.id).order_by(Ticket.id.desc()).limit(10)

    form = TicketForm()
    if form.validate_on_submit():
        print(form.technician.data, form.subject.data, form.severity.data)
        new_ticket = Ticket(ticket_title = form.subject.data,ticket_description = form.description.data, severity = form.severity.data, ticket = current_user, assigned_to = str(form.technician.data))
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('.requester'))
    return render_template('requester.html', form= form, open_tickets_list = open_tickets_list, progress_tickets_list = progress_tickets_list, closed_tickets_list = closed_tickets_list)

@main.route('/users', methods = ['GET','POST'])
def users():
    form = CreateUserForm()

    if form.validate_on_submit():
        role = 0
        if str(form.role.data) == 'admin':
            role = 1
        elif str(form.role.data) == 'technician':
            role = 2
        elif str(form.role.data) == 'requester':
            role = 3
        user = User(email = form.email.data, username = form.username.data,firstname= form.firstname.data,lastname= form.lastname.data,password = form.password.data,role_id = role)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.users'))

    users = User.query.order_by(User.id.asc()).all()
    return render_template('users.html',users = users, form = form)

@main.route('/tickets')
def tickets():
    tickets = Ticket.query.all()
    return render_template('tickets.html', tickets = tickets)

@main.route('/user/<int:id>/update', methods = ['GET','POST'])
@login_required
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
