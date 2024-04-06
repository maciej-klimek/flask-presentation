from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column, relationship


db = SQLAlchemy()

class User(db.Model):
    id = mapped_column(db.Integer, primary_key=True)
    username = mapped_column(db.String(50), unique=True, nullable=False)
    password = mapped_column(db.String(100), nullable=False)
    notes = relationship('Note', backref='user', lazy=True)

class Note(db.Model):
    id = mapped_column(db.Integer, primary_key=True)
    title = mapped_column(db.String(100), nullable=False)
    content = mapped_column(db.Text, nullable=False)
    user_id = mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)
