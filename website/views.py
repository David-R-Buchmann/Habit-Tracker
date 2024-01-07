from flask import Blueprint, render_template, request, redirect, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note, User, Task, Reward
from .task_tracker import add_xp, subtract_xp, update_level
from . import db
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


@views.route('/edit-task/<int:rewardId>', methods=['GET', 'POST'])
def edit_rewards(rewardId):
    reward = Reward.query.get(rewardId)
    if request.method == "POST":
        reward.data = request.form['reward']
        db.session.commit()
        return redirect(url_for("views.rewards"))
    else:
        return render_template("edit-reward.html", reward=reward, user=current_user)


@views.route('/delete-task/<int:rewardId>')
def delete_rewards(rewardId):
    reward = Reward.query.get(rewardId)
    if reward:
        if reward.user_id == current_user.id:
            db.session.delete(reward)
            db.session.commit()
            flash('Reward deleted', category='error')
    
    return redirect(url_for("views.rewards"))