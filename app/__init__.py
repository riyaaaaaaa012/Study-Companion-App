import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Redirect if user is not logged in

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import blueprints
    from .routes import main
    # from .auth import auth

    # Register blueprints
    app.register_blueprint(main)
    # app.register_blueprint(auth, url_prefix='/auth')

    # Scheduler setup with guard to avoid multiple starts on debug reload
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        scheduler = BackgroundScheduler()

        def check_reminders():
            with app.app_context():
                from .models import Reminder  # Import here to avoid circular import
                now = datetime.utcnow()
                reminders = Reminder.query.filter(
                    Reminder.remind_time <= now,
                    Reminder.is_done == False
                ).all()
                for reminder in reminders:
                    print(f"Reminder: {reminder.title} at {reminder.remind_time}")
                    reminder.is_done = True
                    db.session.commit()

        # Run every 60 seconds
        scheduler.add_job(func=check_reminders, trigger='interval', seconds=60)
        scheduler.start()

    return app
