from flask import jsonify
from ..models import Task, Image
from ..extensions import db
from ..api.images import create_and_upload_images
from . import bp

@bp.route('/tasks/<int:id>/execute', methods=['POST'])
def execute_task(id):
    task = Task.query.get_or_404(id)
    print(f"Executing task: {task.id}")  # Debugging line

    # Fetch or generate image URLs associated with the task
    image_urls = create_and_upload_images(task.id)

    for url in image_urls:
        if url is not None:
            image = Image(task_id=task.id, image_url=url)
            db.session.add(image)
            print(f"Added image for task_id {task.id} with URL {url}")  # Debugging line
        else:
            print(f"Skipping image with None URL for task_id {task.id}")  # Debugging line

    db.session.commit()

    return jsonify({'message': 'Task executed, images captured, and task deleted from database'}), 200



@bp.route('/tasks/<int:id>/images', methods=['GET'])
def get_task_images(id):
    images = Image.query.filter_by(task_id=id).all()
    return jsonify([{'id': image.id, 'image_url': image.image_url} for image in images])
