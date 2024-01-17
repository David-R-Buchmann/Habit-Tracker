from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# sets up the models for all important parts of the website:
# one for Notes, Tasks, Rewards and Users each
# The values they possess are all represented by a column of various types in the database.

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True) # sets a unique id for each note
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # also uses the user's unique id
    data = db.Column(db.String(10000)) # the text of the note is stored as a string in data
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # the data where the note was added is also stored

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True) # sets a unique id for each task
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # also uses the user's unique id
    data = db.Column(db.String(10000)) # the text of the task is stores as a string in data
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # the date where the task was added is also stored
    xp = db.Column(db.Integer, default=10) # each task has its own XP value with a standard value of 10
    is_done = db.Column(db.Boolean, default=False) # this boolean signifies if the task is completed or not

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True) # see Task/Note
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # see Task/Note
    data = db.Column(db.String(10000)) # see Task/Note
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # see Task/Note
    is_claimed = db.Column(db.Boolean, default=False) # this booleon signifies if the rewards has already been claimed or not

class User(db.Model, UserMixin): # the user class has the most variables:
    id = db.Column(db.Integer, primary_key=True) # every user has a unique id
    userName = db.Column(db.String(150), unique=True) # the username has to be unique and is fetched on signup
    password = db.Column(db.String(150)) # the password doesn't have to be unique and is fetched on signup
    first_name = db.Column(db.String(150)) # the first name doesn't have to be unique and is fetched on signup
    notes = db.relationship('Note') # creates a relationship from Notes, Tasks and Rewards to their corresponding users
    tasks = db.relationship('Task')
    rewards = db.relationship('Reward')
    claimableRewards = db.Column(db.Integer, default=0) # stores how many rewards can be claimed by the user
    totalXp = db.Column(db.Integer, default=0) # stores total and current XP as well as level and level progress as integers for each user
    currentXp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=0)
    level_progress = db.Column(db.String(1000), default = '0 %')
    dailyXpValue = db.Column(db.Integer, default=10) # these default values
    weeklyXpValue = db.Column(db.Integer, default=25) #  for the task XP and 
    monthlyXpValue = db.Column(db.Integer, default=50) #  level requirement can be changed
    levelRequirement = db.Column(db.Integer, default=500) # in the profile section
    tasksCompleted = db.Column(db.Integer, default=0) # tracks the number of completed tasks for each user