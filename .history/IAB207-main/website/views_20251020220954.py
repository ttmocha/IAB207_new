from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/events/<slug>')
def event_details(slug):
    return render_template('event-details.html')

@main_bp.route('/create')
def create_event():
    return render_template('create-event.html')

@main_bp.route('/history')
def booking_history():
    return render_template('booking-history.html')

