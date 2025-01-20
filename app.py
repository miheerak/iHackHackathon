#main application, handles backend logic

import os
from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('registrationpage'))
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/registrationpage')
def registrationpage():
    return render_template('registrationpage.html')

@app.route('/contact-form', methods=['POST'])
def submit_feedback():
    try:
        name = request.form['name']
        email = request.form['email']
        feedback_message = request.form['feedback']
        feedback = Feedback(name=name, email=email, message=feedback_message)
        db.session.add(feedback)
        db.session.commit()
        return "Feedback submitted successfully!"
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)