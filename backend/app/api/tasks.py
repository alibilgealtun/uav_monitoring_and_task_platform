from flask import jsonify, request
from ..models import Task, Image, Drone
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

    # Retrieve the images for the task
    images = Image.query.filter_by(task_id=task.id).all()
    image_data = [image.to_dict() for image in images]

    return jsonify({'message': 'Task executed', 'images': image_data}), 200


@bp.route('/tasks/<int:id>/images', methods=['GET'])
def get_task_images(id):
    images = Image.query.filter_by(task_id=id).all()
    return jsonify([{'id': image.id, 'image_url': image.image_url} for image in images])

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


@bp.route('/tasks/<int:task_id>/assign', methods=['PUT'])
def assign_task(task_id):
    data = request.get_json()
    drone_id = data.get('drone_id')

    if not drone_id:
        return jsonify({'error': 'Drone ID is required'}), 400

    task = Task.query.get_or_404(task_id)
    drone = Drone.query.get_or_404(drone_id)

    task.drone_id = drone_id
    db.session.commit()

    return jsonify({'message': f'Task {task_id} assigned to drone {drone_id}'}), 200


@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    drone_id = data.get('drone_id')  # Assuming each task is assigned to one drone

    if not name:
        return jsonify({'error': 'Task name is required'}), 400

    # Optional: Validate drone_id if provided
    if drone_id:
        drone = Drone.query.get(drone_id)
        if not drone:
            return jsonify({'error': 'Invalid drone ID'}), 400

    # Create and add new task to the database
    new_task = Task(name=name, description=description, drone_id=drone_id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201