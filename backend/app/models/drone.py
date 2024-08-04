from ..extensions import db

class Drone(db.Model):
    """
    Drone model representing a drone.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Drone %r>' % self.id

    def to_dict(self):
        """
        Converts the Drone object to a dictionary, including its tasks.
        """
        tasks = [task.to_dict() for task in self.tasks]
        return {
            "id": self.id,
            "name": self.name,
            "tasks": tasks,
        }
