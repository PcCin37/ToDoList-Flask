# create database models
from exts import db
from datetime import datetime


# the database for storing the verification code of each email address
# email, verification code
# id as primary key
class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    verification_code = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


# the database for storing the information of each user
# username, email, password
# id as primary key
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(400), nullable=False)
    available_time = db.Column(db.DateTime, default=datetime.now)


# the database for storing the information of each todolist
# assessment title, module, deadline, importance, status, description
# id as primary key, author id as foreign key
class TodolistModel(db.Model):
    __tablename__ = "todolist"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessment_title = db.Column(db.String(200), nullable=False)
    module = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.DateTime)
    importance = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # use foreign keys to reference other form content
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("UserModel", backref="todolists")
