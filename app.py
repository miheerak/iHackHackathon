#main application, handles backend logic

import os
from flask import Flask, request, url_for, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import init_db
from database import add_reported_content
from ml_pipeline import analyze_content
from blockchain_integration import store_to_blockchain

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

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS analysis_results
                      (id INTEGER PRIMARY KEY, text TEXT, result TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze_text():
    text = request.form['text']  
    result = classifier(text)
    label = result[0]['label']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO analysis_results (text, result) VALUES (?, ?)", (text, label))
    conn.commit()
    conn.close()
    return render_template('result.html', text=text, analysis_result=label)


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
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route("/api/analyze", methods=["POST"])
def analyze_text():
    content = request.json.get("content")
    result = analyze_content(content)
    if result["is_flagged"]:
        blockchain_hash = store_to_blockchain(content)
        add_reported_content(content, blockchain_hash)
        result["blockchain_hash"] = blockchain_hash
    return jsonify(result)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

