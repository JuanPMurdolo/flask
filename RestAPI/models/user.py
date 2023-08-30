from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) # unique=True means that the username must be unique
    password = db.Column(db.String(80), nullable=False) # nullable=False means that the password cannot be empty