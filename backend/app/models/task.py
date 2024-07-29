from ..extensions import db

class Task(db.Model):
    """
        Database task model representing a task assigned to a drone. 
        # TODO: Ask if it needs multiple drones. DB Schema documentation says one-to-many..
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    drone_id = db.Column(db.Integer, db.ForeignKey('drone.id'), nullable=False)
    images = db.relationship('Image', backref='task', lazy=True)

    def __repr__(self):
        return '<Task %r>' % self.id

    def to_dict(self):
        """
            Converts the Task object to a dictionary.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'drone_id': self.drone_id
        }