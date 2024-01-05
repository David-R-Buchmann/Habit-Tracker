from flask import Blueprint, render_template, request, redirect, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from .task_tracker import tasks

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


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
    return render_template("tasks.html", user=current_user, tasks=tasks)

@views.route('/add-task', methods=['POST'])
def add_task():
    task = request.form['todo']
    tasks.append({'todo': task, 'done': False})
    return redirect(url_for("views.task"))

@views.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_tasks(index):
    task = tasks[index]
    if request.method == "POST":
        task['todo'] = request.form['task']
        return redirect(url_for("views.task"))
    else:
        return render_template("edit.html", task=task, index=index, user=current_user)
    
@views.route('/check/<int:index>')
def check_tasks(index):
    tasks[index]['done'] = not tasks[index]['done']
    return redirect(url_for("views.task"))

@views.route('/delete/<int:index>')
def delete_tasks(index):
    del tasks[index]
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