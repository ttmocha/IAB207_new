from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os

from . import db
from .models import Event, Comment, Order
from .forms import EventForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Order by start_at (your model field)
    events = db.session.execute(
        db.select(Event).order_by(Event.start_at.asc())
    ).scalars().all()
    return render_template('index.html', events=events)


@main_bp.route('/events/<int:event_id>')
def event_details(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        flash("Event not found.", "warning")
        return redirect(url_for('main.index'))

    # Get comments for this event
    comments = db.session.execute(
        db.select(Comment).where(Comment.event_id == event_id).order_by(Comment.created_at.desc())
    ).scalars().all()

    return render_template('event-details.html', event=event, comments=comments)


@main_bp.route('/create', methods=['GET', 'POST'])
def create_event():
    form = EventForm()

    if form.validate_on_submit():
        # Create new Event object
        new_event = Event(
            title=form.title.data,
            region=form.region.data,
            team_size=form.team_size.data,
            mode=form.mode.data,
            prize=form.prize.data,
            start_at=form.start_at.data,
            status='Open',  # default value
        )

        # Save to database
        db.session.add(new_event)
        db.session.commit()

        flash('Tournament created successfully!', 'success')
        return redirect(url_for('main.index'))  # redirect back to dashboard

    return render_template('create-event.html', form=form)

@main_bp.route('/events/<int:event_id>/comment', methods=['POST'])
def add_comment(event_id):
    body = request.form.get('body')
    author = request.form.get('author', 'Anonymous')
    if body:
        comment = Comment(event_id=event_id, body=body, author=author)
        db.session.add(comment)
        db.session.commit()
        flash("Comment posted!", "success")
    return redirect(url_for('main.event_details', event_id=event_id))

from urllib.parse import urlparse
from flask import request

@main_bp.route('/events/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for('main.index'))

    confirm = request.form.get('confirm')
    if confirm != str(event_id):
        flash("Please delete from the event details page.", "warning")
        return redirect(url_for('main.event_details', event_id=event_id))

    ref = request.referrer
    if ref:
        ref_path = urlparse(ref).path
        details_path = url_for('main.event_details', event_id=event_id)
        if ref_path != details_path:
            flash("Please delete from the event details page.", "warning")
            return redirect(details_path)

    db.session.delete(event)
    db.session.commit()
    flash("Tournament deleted successfully!", "success")
    return redirect(url_for('main.index'))



@main_bp.route('/history')
def booking_history():
    return render_template('booking-history.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 1. Instantiate the form object
    form = LoginForm() 
    
    # 2. Add validation logic here
    if form.validate_on_submit():
        # Process login data, redirect user
        # ...
        return redirect(url_for('main.index'))

    # 3. CORRECT FIX: Pass the 'form' object to the template
    # Note: I am using 'login.html' as the template name, based on the Canvas title.
    return render_template('login.html', form=form)

@main_bp.route('/register')
def register():
    return render_template('register.html')
