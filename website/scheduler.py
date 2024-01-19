from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pytz import timezone
from .models import User, Task
from flask import current_app
from . import db

def daily_update():
    
    with current_app.app_context():
        print("Daily update at: ", datetime.now()) 
        all_users = User.query.all() # Retrieves all users from the database as 'all_users'
        for user in all_users:
            for task in user.tasks:
                if task.scheduling_interval == 'daily': # only targets daily tasks
                    task.is_done = False # Resets the 'done' state of a task to False again
                    db.session.commit()

def weekly_update(): # see daily update
    
    with current_app.app_context():
        print("Weekly update at: ", datetime.now())
        all_users = User.query.all()
        for user in all_users:
            for task in user.tasks:
                if task.scheduling_interval == 'weekly': # only targets weekly tasks
                    task.is_done = False
                    db.session.commit()

def monthly_update(): # see daily update
    
    with current_app.app_context():
        print("Monthly update at: ", datetime.now())
        all_users = User.query.all()
        for user in all_users:
            for task in user.tasks:
                if task.scheduling_interval == 'monthly': # only targets monthly tasks
                    task.is_done = False
                    db.session.commit()


def start_scheduler():
    # Define the timezone as CET (for Europe/Berlin)
    cet_timezone = timezone('Europe/Berlin')

    # Initiate the scheduler with CET as timezone
    scheduler = BackgroundScheduler(timezone=cet_timezone)

    # Daily update at 06:00 CET (Central European Time)
    scheduler.add_job(daily_update, trigger="cron", hour=14, minute=26)
    # Weekly update every Monday at 10:00 CET
    scheduler.add_job(weekly_update, trigger="cron", day_of_week="fri", hour=14, minute=26)

    # Monthly update on the first day of the month at 10:00 CET
    scheduler.add_job(monthly_update, trigger="cron", day="19", hour=14, minute=26)

    # Start the initiated scheduler
    scheduler.start()
