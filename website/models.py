from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    xp = db.Column(db.Integer, default=10)
    is_done = db.Column(db.Boolean, default=False)

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    is_claimed = db.Column(db.Boolean, default=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    tasks = db.relationship('Task')
    rewards = db.relationship('Reward')
    totalXp = db.Column(db.Integer, default=0)
    currentXp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=0)
    level_progress = db.Column(db.String(1000), default = '0 %')
    dailyXpValue = db.Column(db.Integer, default=10)
    weeklyXpValue = db.Column(db.Integer, default=25)
    monthlyXpValue = db.Column(db.Integer, default=50)
    levelRequirement = db.Column(db.Integer, default=500)
    tasksCompleted = db.Column(db.Integer, default=0)