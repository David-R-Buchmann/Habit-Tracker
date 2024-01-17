from flask import Blueprint, render_template, request, redirect, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note, User, Task, Reward
from .task_tracker import add_xp, subtract_xp, update_level
from . import db
import schedule
import time as tm
from datetime import time, timedelta, datetime
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route('/rewards', methods=['GET', 'POST'])
@login_required
def rewards():
    return render_template("rewards.html", user=current_user)

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!')
    
    return render_template("notes.html", user=current_user)


@views.route('/tasks', methods=['GET', 'POST'])
@login_required
def task():    
    return render_template("tasks.html", user=current_user)


@views.route('/add-task/<int:taskXp>', methods=['POST'])
def add_task(taskXp):
    task = request.form.get('task')
    if len(task) < 1:
        flash('Task name too short!', category='error')
    else:
        new_task = Task(data=task, user_id=current_user.id, xp=taskXp)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added!')
        print(new_task.is_done)
    return redirect(url_for("views.task"))


@views.route('/edit/<int:taskId>', methods=['GET', 'POST'])
def edit_tasks(taskId):
    # task = json.loads(request.data)
    # taskId = task['taskId']
    task = Task.query.get(taskId)
    if request.method == "POST":
        task.data = request.form['task']
        db.session.commit()
        return redirect(url_for("views.task"))
    else:
        return render_template("edit.html", task=task, user=current_user)


@views.route('/check/<int:taskId>')
def check_tasks(taskId):
    checked_task = Task.query.get(taskId)
    checked_task.is_done = not checked_task.is_done
    if checked_task.is_done == True:
        add_xp(checked_task.xp)
    else:
        subtract_xp(checked_task.xp)
    db.session.commit()
    return redirect(url_for("views.task"))


@views.route('/delete/<int:taskId>')
def delete_tasks(taskId):
    task = Task.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted', category='error')
    
    return redirect(url_for("views.task"))


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})


@views.route('/add-reward', methods=['POST'])
def add_rewards():
    reward = request.form.get('reward')
    if len(reward) < 1:
        flash('Reward name too short!', category='error')
    else:
        new_reward = Reward(data=reward, user_id=current_user.id)
        db.session.add(new_reward)
        db.session.commit()
        flash('Reward added!')
    return redirect(url_for("views.rewards"))


@views.route('/check-reward/<int:rewardId>')
def check_rewards(rewardId):
    checked_reward = Reward.query.get(rewardId)
    checked_reward.is_claimed = not checked_reward.is_claimed
    if checked_reward.is_claimed == True:
        checked_reward.date = datetime.now()
    db.session.commit()
    return redirect(url_for("views.rewards"))


@views.route('/edit-reward/<int:rewardId>', methods=['GET', 'POST'])
def edit_rewards(rewardId):
    reward = Reward.query.get(rewardId)
    if request.method == "POST":
        reward.data = request.form['reward']
        db.session.commit()
        return redirect(url_for("views.rewards"))
    else:
        return render_template("edit-reward.html", reward=reward, user=current_user)


@views.route('/delete-reward/<int:rewardId>')
def delete_rewards(rewardId):
    reward = Reward.query.get(rewardId)
    if reward:
        if reward.user_id == current_user.id:
            db.session.delete(reward)
            db.session.commit()
            flash('Reward deleted', category='error')
    
    return redirect(url_for("views.rewards"))

@views.route('/update-value', methods=['POST'])
def update_value():
    if request.method == 'POST':
        if 'dailyXp_update' in request.form:
            updatedDailyXpValue = int(request.form['dailyXp_update'])
            if updatedDailyXpValue >= current_user.weeklyXpValue:
                flash('Daily XP task value has to be lower than weekly XP task value!', category='error')
            else:
                current_user.dailyXpValue = updatedDailyXpValue
        if 'weeklyXp_update' in request.form:
            updatedWeeklyXpValue = int(request.form['weeklyXp_update'])
            if updatedWeeklyXpValue <= current_user.dailyXpValue:
                flash('Weekly XP task value has to be higher than daily XP task value!', category='error')
            elif updatedWeeklyXpValue >= current_user.monthlyXpValue:
                flash('Weekly XP task value has to be lower than monthly XP task value')
            else:
                current_user.weeklyXpValue = updatedWeeklyXpValue
        if 'monthlyXp_update' in request.form:
            updatedMonthlyXpValue = int(request.form['monthlyXp_update'])
            if updatedMonthlyXpValue <= current_user.weeklyXpValue:
                flash('Monthly Xp task value has to be higher than weekly XP task value!', category='error')
            current_user.monthlyXpValue = updatedMonthlyXpValue
        if 'levelRequirement_update' in request.form:
            current_user.levelRequirement = request.form['levelRequirement_update']
        db.session.commit()
    
    return redirect(url_for('views.profile'))
