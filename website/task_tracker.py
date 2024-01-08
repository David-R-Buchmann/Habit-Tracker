from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Note, Task
from . import db

user=current_user


def add_xp(xp_amount):
    user.currentXp += xp_amount
    user.totalXp += xp_amount
    update_level()

def subtract_xp(xp_amount):
    user.currentXp -= xp_amount
    user.totalXp -= xp_amount
    update_level()
    print(5 - (user.level % 5))

def update_level():
    if user.currentXp >= user.levelRequirement:
        user.currentXp -= user.levelRequirement
        user.level += 1
        grant_reward(user.level)
    elif user.currentXp < 0:
        user.currentXp += user.levelRequirement
        user.level -= 1
    
    new_level_progress = int((user.currentXp / user.levelRequirement) * 100)
    user.level_progress = f'{new_level_progress} %'
    db.session.commit()


def grant_reward(level):
    pass