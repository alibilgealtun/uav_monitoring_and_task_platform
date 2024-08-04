from ..extensions import db
from .association import task_drones

class Task(db.Model):
    """
        Database task model representing a task assigned to a drone.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    drones = db.relationship('Drone', secondary=task_drones, backref=db.backref('tasks', lazy=True), lazy='subquery')
    # images = db.relationship('Image', backref='task', lazy=True)

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
            'drones': [drone.id for drone in self.drones]
        }
