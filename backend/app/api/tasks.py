from flask import jsonify, request
from ..models import Task, Image, Drone
from ..extensions import db
from . import bp
from flask_httpauth import HTTPBasicAuth

from ..utils.img_utils import ImageUtils

auth = HTTPBasicAuth()

# since I will use HTTPAuth only here, I am using a dictionary as temporary to test.
# if needed, carry to config and reformat the functions as wanted
users = {
    "admin": "admin"
}


@auth.verify_password
def verify_password(username, password):
    if username in users and (users.get(username) == password):
        return username


@bp.route('/tasks/<int:id>/execute', methods=['POST'])
@auth.login_required
def execute_task(id):
    """
    POST /tasks/<int:id>/execute
    Executes a task by generating and uploading images, and associating them with the task.

    Args:
        id (int): The ID of the task to execute.

    Returns:
        JSON response with a message and the associated images.
    """
    task = Task.query.get_or_404(id)
    # Fetch or generate image URLs associated with the task
    image_urls = ImageUtils.create_and_upload_images(task.id)
    if not image_urls:
        return jsonify({'error': 'Error executing task.'})
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
    """
    GET /tasks/<int:id>/images
    Fetches all images associated with a specific task.

    Args:
        id (int): The ID of the task.

    Returns:
        JSON response with a list of images.
    """
    images = Image.query.filter_by(task_id=id).all()

    return jsonify([{'task_id': id, 'image_id': image.id, 'image_url': image.image_url} for image in images])


@bp.route('/tasks', methods=['GET'])
def get_tasks():
    """
    GET /tasks
    Fetches all tasks from the database and returns them as a JSON list.

    Returns:
        JSON response with a list of tasks.
    """
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


@bp.route('/tasks/<int:task_id>/assign', methods=['PUT'])
def assign_task(task_id):
    """
    PUT /tasks/<int:task_id>/assign
    Assigns drones to a specific task.

    Args:
        task_id (int): The ID of the task to assign drones to.

    Returns:
        JSON response with a message indicating success or failure.
    """
    data = request.get_json()
    drone_ids = data.get('drone_ids', [])
    if not drone_ids:
        return jsonify({'error': 'Drone IDs are required'}), 400
    task = Task.query.get_or_404(task_id)
    # Clear current drone assignments
    task.drones = []
    for drone_id in drone_ids:
        drone = Drone.query.get_or_404(drone_id)
        task.drones.append(drone)

    db.session.commit()

    return jsonify({'message': f'Drones assigned to task {task_id}'}), 200


@bp.route('/tasks', methods=['POST'])
def create_task():
    """
    POST /tasks
    Creates a new task and assigns drones to it.

    Returns:
        JSON response with the created task.
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    drone_ids = data.get('drone_ids')

    if not name:
        return jsonify({'error': 'Task name is required'}), 400

    # Create and add new task to the database
    new_task = Task(name=name, description=description)

    db.session.add(new_task)
    db.session.flush()  # Ensure the new task gets an ID before assigning drones
    if drone_ids:
        drones = Drone.query.filter(Drone.id.in_(drone_ids)).all()
        new_task.drones.extend(drones)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201
