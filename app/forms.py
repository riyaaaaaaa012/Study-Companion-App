from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Subject Form
class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired()])
    exam_date = DateField('Exam Date (optional)', format='%Y-%m-%d', validators=[])
    submit = SubmitField('Add Subject')

# Syllabus Item Form
class SyllabusItemForm(FlaskForm):
    title = StringField('Topic/Chapter Title', validators=[DataRequired()])
    is_completed = BooleanField('Completed')
    submit = SubmitField('Add Topic')

# Study Session Log Form
class StudySessionForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    duration_minutes = IntegerField('Duration (minutes)', validators=[DataRequired()])
    notes = TextAreaField('Notes (optional)')
    submit = SubmitField('Log Study Session')

class ReminderForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    remind_time = DateTimeField('Remind Time (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Add Reminder')