# views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user, logout_user
from datetime import datetime
from werkzeug.utils import secure_filename
from urllib.parse import urlparse
import os

from . import db
from .models import Event, Comment, Order, User, Booking
from .forms import EventForm, LoginForm, RegisterForm, BookingForm

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
    form = BookingForm()
    if not event:
        flash("Event not found.", "warning")
        return redirect(url_for('main.index'))

    comments = db.session.execute(
        db.select(Comment).where(Comment.event_id == event_id).order_by(Comment.created_at.desc())
    ).scalars().all()

    return render_template('event-details.html', event=event, comments=comments, form=form)

@main_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        banner_path = None
        if form.banner_upload.data:
            file = form.banner_upload.data
            filename = secure_filename(file.filename)
            img_dir = os.path.join(current_app.static_folder, 'img')
            os.makedirs(img_dir, exist_ok=True)
            filepath = os.path.join(img_dir, filename)
            file.save(filepath)
            banner_path = f'img/{filename}'
        elif form.banner_url.data:
            banner_path = form.banner_url.data.strip()

        start_at = datetime.combine(form.date.data, form.time.data)

        new_event = Event(
            title=form.title.data,
            category=form.category.data,
            region=form.region.data,
            team_size=form.team_size.data,
            mode=form.mode.data,
            prize=form.prize.data,
            start_at=start_at,
            status='Open',
            description=form.description.data,
            banner=banner_path,
            user_id=current_user.id,
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Tournament created successfully!', 'success')
        return redirect(url_for('main.event_details', event_id=new_event.id))
    return render_template('create-event.html', form=form)

@main_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for('main.index'))

    if event.user_id != current_user.id:
        flash("You can only edit tournaments you created.", "warning")
        return redirect(url_for('main.event_details', event_id=event_id))

    form = EventForm(obj=event)

    if request.method == 'GET' and event.start_at:
        form.date.data = event.start_at.date()
        form.time.data = event.start_at.time().replace(second=0, microsecond=0)

    if request.method == 'POST' and not form.validate():
        flash(str(form.errors), 'danger')

    if form.validate_on_submit():
        event.title       = form.title.data
        event.category    = form.category.data
        event.region      = form.region.data
        event.team_size   = form.team_size.data
        event.mode        = form.mode.data
        event.prize       = form.prize.data
        event.description = form.description.data
        event.start_at = datetime.combine(form.date.data, form.time.data)

        uploaded = form.banner_upload.data
        if uploaded and uploaded.filename:
            filename  = secure_filename(uploaded.filename)
            img_dir   = os.path.join(current_app.static_folder, 'img')
            os.makedirs(img_dir, exist_ok=True)
            filepath  = os.path.join(img_dir, filename)
            uploaded.save(filepath)
            event.banner = f'img/{filename}'
        elif form.banner_url.data:
            event.banner = form.banner_url.data.strip()

        db.session.commit()
        flash('Tournament updated successfully!', 'success')
        return redirect(url_for('main.index'))  # back to dashboard

    # Reuse existing create template 
    return render_template('create-event.html',
                           form=form,
                           page_title="Edit Tournament",
                           submit_text="Save Changes",
                           event=event)

@main_bp.route('/events/<int:event_id>/comment', methods=['POST'])
@login_required
def add_comment(event_id):
    body = request.form.get('body')
    author = current_user.name if getattr(current_user, "name", None) else "User"
    if body:
        comment = Comment(event_id=event_id, body=body, author=author)
        db.session.add(comment)
        db.session.commit()
        flash("Comment posted!", "success")
    return redirect(url_for('main.event_details', event_id=event_id))

@main_bp.route('/events/<int:event_id>/cancel', methods=['POST'])
@login_required
def cancel_event(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for('main.index'))

    # Making cancelling restricted to hosts :)
    if event.user_id != current_user.id:
        flash("You can only cancel tournaments you host.", "warning")
        return redirect(url_for('main.event_details', event_id=event_id))

    # Ensures it cancels from the rigt page
    confirm = request.form.get('confirm')
    if confirm != str(event_id):
        flash("Please cancel from the event details page.", "warning")
        return redirect(url_for('main.event_details', event_id=event_id))

    # Adding cancel logic as requested by tutor
    event.status = "Cancelled"
    db.session.commit()

    flash("Tournament cancelled successfully!", "warning")
    return redirect(url_for('main.index'))

@main_bp.route('/events/<int:event_id>/reopen', methods=['POST'])
@login_required
def reopen_event(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for('main.index'))

    # Host-only restriction
    if event.user_id != current_user.id:
        flash("You can only reopen tournaments you host.", "warning")
        return redirect(url_for('main.event_details', event_id=event_id))

    # Can only change to open from cancelled
    if (event.status or 'Open') != 'Cancelled':
        flash("Only cancelled tournaments can be reopened.", "warning")
        return redirect(url_for('main.event_details', event_id=event_id))
    
    # Changing status back to Open
    event.status = "Open"
    db.session.commit()

    flash("Tournament is open for booking again.", "event")
    return redirect(url_for('main.event_details', event_id=event_id))


@main_bp.route('/events/<int:event_id>/book', methods=['POST'])
@login_required
def book_event(event_id):
    form = BookingForm()
    if form.validate_on_submit():
        qty = form.quantity.data
    else:
        # Fallback in case the form wasn't rendered via WTForms for some reason
        qty_raw = request.form.get('quantity', '')
        try:
            qty = int(qty_raw)
        except (TypeError, ValueError):
            flash('Please enter a valid quantity.', 'danger')
            return redirect(url_for('main.event_details', event_id=event_id))

    if qty <= 0:
        flash('Invalid quantity.', 'danger')
        return redirect(url_for('main.event_details', event_id=event_id))

    booking = Booking(
        order_id=Booking.new_order_id(),
        user_id=current_user.id,
        event_id=event_id,
        quantity=qty,
        booked_at=datetime.utcnow(),
        status='Confirmed',
    )
    db.session.add(booking)
    db.session.commit()
    flash(f'Booking successful! Order ID: {booking.order_id}', 'success')
    return redirect(url_for('main.booking_history'))


@main_bp.route('/history')
@login_required
def booking_history():
    bookings = db.session.execute(
        db.select(Booking)
        .where(Booking.user_id == current_user.id)
        .order_by(Booking.booked_at.desc())
    ).scalars().all()
    return render_template('booking-history.html', bookings=bookings)

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
