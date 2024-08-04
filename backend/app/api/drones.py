from flask import jsonify, request
from ..models import Drone
from ..extensions import db
from . import bp


@bp.route('/drones', methods=['GET'])
def get_drones():
    """
    GET /drones
    Fetches drones from the database with pagination.

    Query Parameters:
        page (int): The page number to retrieve.
        per_page (int): The number of drones per page.

    Returns:
        JSON response with a list of drones and pagination info.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    drones_query = Drone.query.paginate(page=page, per_page=per_page, error_out=False)
    drones = [drone.to_dict() for drone in drones_query.items]

    return jsonify({
        'drones': drones,
        'total': drones_query.total,
        'pages': drones_query.pages,
        'current_page': drones_query.page,
    })

@bp.route('/drones', methods=['POST'])
def add_drone():
    """
    POST /drones
    Adds a new drone to the database.
    Expects a JSON payload with a 'name' field.
    """
    data = request.get_json()
    drone = Drone(name=data['name'])
    db.session.add(drone)
    db.session.commit()
    return jsonify({'id': drone.id, 'name': drone.name}), 201
