from ..extensions import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    image_url = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Image %r>' % self.id

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "image_url": self.image_url,
        }
