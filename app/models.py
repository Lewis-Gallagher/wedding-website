from enum import unique
from app import db

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attending = db.Column(db.Integer, index=False, unique=False)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(20), index=True, unique=False)
    diet_req = db.Column(db.String(), index=False, unique=False)
    message = db.Column(db.Text(500))

    def __repr__(self):
        return f"<Guest { self.id }-{ self.name }>"