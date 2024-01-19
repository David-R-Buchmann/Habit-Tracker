from website import create_app
from website.scheduler import start_scheduler

app = create_app()

if __name__ == '__main__':
    start_scheduler(app)
    app.run(debug=True)