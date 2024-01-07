from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Note, Task
from . import db

user=current_user

rewards = [{'reward': '5 € Steam Guthaben', 'date': '07.01.2024'}]

def add_xp(xp_amount):
    user.currentXp += xp_amount
    user.totalXp += xp_amount
    update_level()

def subtract_xp(xp_amount):
    user.currentXp -= xp_amount
    user.totalXp -= xp_amount
    update_level()

def update_level():
    if user.currentXp >= 250:
        user.currentXp -= 250
        user.level += 1
        grant_reward(user.level)
    elif user.currentXp < 0:
        user.currentXp += 250
        user.level -= 1
    
    new_level_progress = int((user.currentXp / 250) * 100)
    user.level_progress = f'{new_level_progress} %'
    db.session.commit()


def grant_reward(level):
    pass