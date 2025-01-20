#defines database schema

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, create_engine, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Feedback {self.name}>'

Base = declarative_base()

class ReportedContent(Base):
    __tablename__ = "reported_content"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    blockchain_hash = Column(String(256), nullable=True)
    flagged_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    engine = create_engine("sqlite:///database.db")
    Base.metadata.create_all(engine)

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    result = db.Column(db.String(100))

    def __repr__(self):
        return f'<AnalysisResult {self.id} {self.result}>'
