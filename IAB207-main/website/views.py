from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user, logout_user
from datetime import datetime
from werkzeug.utils import secure_filename
from urllib.parse import urlparse
import os

from . import db
from .models import Event, Comment, Order, User
from .forms import EventForm, LoginForm, RegisterForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
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

    comments = db.session.execute(
        db.select(Comment).where(Comment.event_id == event_id).order_by(Comment.created_at.desc())
    ).scalars().all()

    return render_template('event-details.html', event=event, comments=comments)

@main_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        new_event = Event(
            title=form.title.data,
            region=form.region.data,
            team_size=form.team_size.data,
            mode=form.mode.data,
            prize=form.prize.data,
            start_at=form.start_at.data,
            status='Open',
            user_id=current_user.id,          # setting the host of the event based on current user
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Tournament created successfully!', 'success')
        return redirect(url_for('main.index'))
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

@main_bp.route('/events/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for('main.index'))

    # Only the host may delete
    if event.user_id != current_user.id:
        flash("You can only delete tournaments you host.", "warning")
        return redirect(url_for('main.event_details', event_id=event_id))

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
@login_required
def booking_history():

    my_events = db.session.execute(
        db.select(Event).where(Event.user_id == current_user.id).order_by(Event.start_at.asc())
    ).scalars().all()
    return render_template('booking-history.html', my_events=my_events)

# Public profile page to view a host and their tournaments ( this is just a brainstorming idea :) )
@main_bp.route('/users/<int:user_id>')
def user_profile(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash("User not found.", "warning")
        return redirect(url_for('main.index'))
    hosted = db.session.execute(
        db.select(Event).where(Event.user_id == user_id).order_by(Event.start_at.asc())
    ).scalars().all()
    return render_template('user-profile.html', user=user, hosted=hosted)

@main_bp.route('/login')
def login():
    form = LoginForm()
    return render_template('user.html', form=form)

@main_bp.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
