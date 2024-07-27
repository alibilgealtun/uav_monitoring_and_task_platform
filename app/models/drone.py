from ..extensions import db

class Drone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='drone', lazy=True) # One-to-many relationship with Task

    def __repr__(self):
        return '<Drone %r>' %self.id