from ..extensions import db

task_drones = db.Table('task_drones',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('drone_id', db.Integer, db.ForeignKey('drone.id'), primary_key=True)
)