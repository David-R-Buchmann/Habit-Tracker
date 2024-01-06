from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Note, Task

# user=current_user

# task_number = 0
# for task in user.tasks:
#     task_number += 1


