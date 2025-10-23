# models.py
from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

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
