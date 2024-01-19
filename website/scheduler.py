from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pytz import timezone
from .models import User, Task
from flask import current_app
from . import db

def daily_update(app):
    with app.app_context():
        print("Daily update at: ", datetime.now()) 
        all_users = User.query.all() # Retrieves all users from the database as 'all_users'
        for user in all_users:
            for task in user.tasks:
                if task.scheduling_interval == 'daily': # only targets daily tasks
                    task.is_done = False # Resets the 'done' state of a task to False again
                    print("Daily task refreshed!")
                    db.session.commit()
                else:
                    print("Task scheduling interval is not daily.")

def weekly_update(app): # see daily update
    with app.app_context():
        print("Weekly update at: ", datetime.now())
        all_users = User.query.all()
        for user in all_users:
            for task in user.tasks:
                if task.scheduling_interval == 'weekly': # only targets weekly tasks
                    task.is_done = False
                    print("Weekly task refreshed!")
                    db.session.commit()
                else:
                    print("Task scheduling interval is not weekly.")

def monthly_update(app): # see daily update
    with app.app_context():
        print("Monthly update at: ", datetime.now())
        all_users = User.query.all()
        for user in all_users:
            for task in user.tasks:
                if task.scheduling_interval == 'monthly': # only targets monthly tasks
                    task.is_done = False
                    print("Monthly task refreshed!")
                    db.session.commit()
                else:
                    print("Task scheduling interval is not monthly.")


def start_scheduler(app):
    # Define the timezone as CET (for Europe/Berlin)
    cet_timezone = timezone('Europe/Berlin')

    # Initiate the scheduler with CET as timezone
    scheduler = BackgroundScheduler(timezone=cet_timezone)

    # Daily update at 06:00 CET (Central European Time)
    scheduler.add_job(daily_update, args=[app], trigger="cron", hour=16, minute=47)
    # Weekly update every Monday at 10:00 CET
    scheduler.add_job(weekly_update, args=[app], trigger="cron", day_of_week="fri", hour=16, minute=47)

    # Monthly update on the first day of the month at 10:00 CET
    scheduler.add_job(monthly_update, args=[app], trigger="cron", day="19", hour=16, minute=47)

    # Start the initiated scheduler
    scheduler.start()
