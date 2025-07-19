from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db

from app.forms import (
    RegistrationForm, LoginForm, SubjectForm, 
    SyllabusItemForm, StudySessionForm, ReminderForm
)
from app.models import User, Subject, SyllabusItem, StudySession
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/dashboard')
@login_required
def dashboard():
    subjects = Subject.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', subjects=subjects)

@main.route('/add_subject', methods=['GET', 'POST'])
@login_required
def add_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(name=form.name.data, exam_date=form.exam_date.data, user_id=current_user.id)
        db.session.add(subject)
        db.session.commit()
        flash('Subject added!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_subject.html', form=form)

@main.route('/subject/<int:subject_id>')
@login_required
def view_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if subject.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.dashboard'))
    syllabus = SyllabusItem.query.filter_by(subject_id=subject.id).all()
    return render_template('subject_detail.html', subject=subject, syllabus=syllabus)

@main.route('/subject/<int:subject_id>/add_topic', methods=['GET', 'POST'])
@login_required
def add_topic(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if subject.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.dashboard'))
    form = SyllabusItemForm()
    if form.validate_on_submit():
        item = SyllabusItem(title=form.title.data, subject_id=subject.id)
        db.session.add(item)
        db.session.commit()
        flash('Topic added!', 'success')
        return redirect(url_for('main.view_subject', subject_id=subject.id))
    return render_template('add_topic.html', form=form, subject=subject)

@main.route('/log_study', methods=['GET', 'POST'])
@login_required
def log_study():
    form = StudySessionForm()
    if form.validate_on_submit():
        subject = Subject.query.filter_by(name=form.subject.data, user_id=current_user.id).first()
        if not subject:
            flash('Subject not found.', 'danger')
            return redirect(url_for('main.log_study'))
        session = StudySession(
            user_id=current_user.id,
            subject_id=subject.id,
            duration_minutes=form.duration_minutes.data,
            notes=form.notes.data
        )
        db.session.add(session)
        db.session.commit()
        flash('Study session logged!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('log_study.html', form=form)

@main.route('/study_log')
@login_required
def study_log():
    sessions = StudySession.query.filter_by(user_id=current_user.id).order_by(StudySession.timestamp.desc()).all()
    return render_template('study_log.html', sessions=sessions)


# ======== New Route: Set Reminder ========

@main.route('/set_reminder/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def set_reminder(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if subject.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.dashboard'))

    form = ReminderForm()
    if form.validate_on_submit():
        subject.reminder_date = form.remind_time.data  # use form.remind_time here
        db.session.commit()
        flash('Reminder set successfully!', 'success')
        return redirect(url_for('main.view_subject', subject_id=subject.id))

    if request.method == 'GET':
        form.remind_time.data = subject.reminder_date  # and here

    return render_template('set_reminder.html', form=form, subject=subject)
