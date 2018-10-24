from flask import render_template,redirect,url_for,abort,request
from . import main
from flask_login import login_required,current_user
from ..models import User,Ticket
from .forms import TicketForm
from .. import db
from ..email import mail_message

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    if current_user.role_id == 1:
        return redirect(url_for('.admin'))
    elif current_user.role_id == 2:
        return redirect(url_for('.technician'))
    else:
        return redirect(url_for('.requester'))

    return render_template('index.html')

@main.route('/requester')
def requester():
    return render_template('requester.html')


@main.route('/technician', methods=['GET','POST'])
def technician():
    open_tickets = Ticket.query.filter_by(status = 'open',assigned_to = current_user.username).order_by(Ticket.id.desc()).limit(5)
    progress_tickets = Ticket.query.filter_by(status = 'progress',assigned_to = current_user.username).order_by(Ticket.id.desc()).limit(5)
    closed_tickets = Ticket.query.filter_by(status = 'closed',assigned_to = current_user.username).order_by(Ticket.id.desc()).limit(5)
    form = TicketForm()
    if form.validate_on_submit():
        new_ticket = Ticket(ticket_title = form.subject.data,ticket_description = form.description.data, severity = form.severity.data, user_id = current_user, assigned_to = form.technician.data)
        db.session.add(new_ticket)
        db.session.commit()
        # user = User
        # mail_message('New Ticket Issued','email/new_ticket','')
        return redirect(url_for('.technician'))
    return render_template('technician.html', form = form, open_tickets = open_tickets,progress_tickets = progress_tickets,closed_tickets = closed_tickets)

@main.route('/technician/tickets')
def tickets():
    tickets = Ticket.query.filter_by(assigned_to = current_user.username).all()
    my_tickets = Ticket.query.filter_by(user_id = current_user.id).all()

    return render_template('tickets.html',tickets = tickets, my_tickets = my_tickets)

@main.route('/technician/tickets/ticket/<int:id>')
def ticket(id):
    ticket = Ticket.query.filter_by(id = id).first()

    return render_template('ticket.html', ticket = ticket)

@main.route('/technician/tickets/ticket/<int:id>/status_progress', methods=['GET','POST'])
def update_progress(id):
    ticket = Ticket.query.filter_by(id = id).first()
    ticket.status = 'progress'
    db.session.commit()

    return redirect(url_for('main.ticket', id=id))

@main.route('/technician/tickets/ticket/<int:id>/status_closed', methods=['GET','POST'])
def update_closed(id):
    ticket = Ticket.query.filter_by(id = id).first()
    ticket.status = 'closed'
    db.session.commit()

    return redirect(url_for('main.ticket', id=id))
