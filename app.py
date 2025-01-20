#main application, handles backend logic

import os
from flask import Flask, request, url_for, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import init_db
from database import add_reported_content
from ml_pipeline import analyze_content
from blockchain_integration import store_to_blockchain
from transformers import pipeline
import sqlite3
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
csrf = CSRFProtect(app)
classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS analysis_results
                      (id INTEGER PRIMARY KEY, text TEXT, result TEXT)''')
    conn.commit()
    conn.close()

init_db()

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    feedback = TextAreaField('Feedback', validators=[DataRequired()])

class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    result = db.Column(db.String(100), nullable=False)

class AnalyzeForm(FlaskForm):
    text = TextAreaField('Text to Analyze', validators=[DataRequired()])


'''
@app.route('/')
def index():
    form = FeedbackForm()
    return render_template('index.html', form=form)

    '''
@app.route('/')
def index():
    register_form = RegisterForm()  # Use RegisterForm for registration
    feedback_form = FeedbackForm()  # Use FeedbackForm for feedback
    return render_template('index.html', register_form=register_form, feedback_form=feedback_form)


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    form = AnalyzeForm()
    if form.validate_on_submit():
        text = form.text.data  
        result = classifier(text)
        label = result[0]['label']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO analysis_results (text, result) VALUES (?, ?)", (text, label))
        conn.commit()
        conn.close()
        return render_template('result.html', text=text, analysis_result=label)
    return render_template('analyze.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered. Please log in."
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('registration_success'))
    return render_template('register.html', form=form)

@app.route('/registration_success')
def registration_success():
    return "Registration successful!"

@app.route('/contact-form', methods=['POST'])
def submit_feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        feedback_message = form.feedback.data
        feedback = Feedback(name=name, email=email, message=feedback_message)
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('feedback_page'))
    else:
        return "An error occurred. Please ensure all fields are filled correctly.", 400

@app.route('/feedback-page')
def feedback_page():
    return render_template('feedbackpage.html')

@app.route("/api/analyze", methods=["POST"])
def analyze_content_api():
    content = request.json.get("content")
    result = analyze_content(content)
    if result["is_flagged"]:
        blockchain_hash = store_to_blockchain(content)
        add_reported_content(content, blockchain_hash)
        result["blockchain_hash"] = blockchain_hash
    return jsonify(result)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)


