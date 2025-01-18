#main application, handles backend logic

import os
from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(f'C:\\Users\\ksmih\\iHackfolder\\iHackHackathon\\app.py'))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()

app = Flask(__name__)
@app.route("/")
def index():
	return render_template("index.html")
if __name__ == "__main__":
	app.run()

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registration successful!"})

@app.route('contact-form', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    feedback = Feedback(name=name, email=email)
    db.session.add(feedback)
    db.session.commit()
    return "Feedback submitted successfully!"
