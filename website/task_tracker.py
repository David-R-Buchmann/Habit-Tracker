from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Note, Task

user=current_user

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
        user.currentXp - 250
        user.level += 1
    elif user.currentXp < 0:
        user.currentXp + 250
        user.level -= 1

