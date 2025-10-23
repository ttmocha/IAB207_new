# models.py
from . import db
from datetime import datetime
from flask_login import UserMixin
import uuid

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    region = db.Column(db.String(64))
    team_size = db.Column(db.String(16))
    mode = db.Column(db.String(64))
    prize = db.Column(db.String(64))
    category = db.Column(db.String(64))  # category field for form :)
    status = db.Column(db.String(32), default='Open')
    start_at = db.Column(db.DateTime)
    description = db.Column(db.Text) # description field for form :)
    banner = db.Column(db.String(255)) 
    
    #im adding this to link created tournaments to users/
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    host = db.relationship('User', backref=db.backref('events', lazy='dynamic'))

    bookings = db.relationship('Booking', backref='event', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    author = db.Column(db.String(64))
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(12), unique=True, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    booked_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(24), default='Confirmed', nullable=False)  # Confirmed / Cancelled etc.

    @staticmethod
    def new_order_id():
        # short, human-friendly order id (e.g., 8C2F-A1D9)
        raw = uuid.uuid4().hex[:8].upper()
        return f"{raw[:4]}-{raw[4:]}"