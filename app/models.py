from app import db

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(20), index=True, unique=False)
    message = db.Column(db.Text(150))

    def __repr__(self):
        return f"<Guest { self.name }>"
