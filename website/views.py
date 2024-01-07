from flask import Blueprint, render_template, request, redirect, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note, User, Task
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

@views.route('/add-task', methods=['POST'])
def add_task():
    task = request.form.get('task')
    new_task = Task(data=task, user_id=current_user.id)
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
    print(current_user.currentXp)
    db.session.commit()
    print(f"Task {taskId} checked!")
    print(f"Task belongs to User {current_user.id}")
    print(checked_task.is_done)
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