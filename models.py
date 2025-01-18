#defines database schema

from database import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False
    password = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    message=Column(Text, nullable=False)

    def __repr__(self):
        return f'<Feedback {self.name}>'