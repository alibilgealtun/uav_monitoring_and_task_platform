from flask import jsonify, request
from ..models import Drone
from ..extensions import db
from . import bp

@bp.route('/drones', methods=['GET'])
def get_drones():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    drones = Drone.query.paginate(page, per_page, False)
    return jsonify({
        'drones': [{'id': drone.id, 'name': drone.name} for drone in drones.items],
        'total': drones.total,
        'pages': drones.pages,
        'current_page': drones.page
    })

@bp.route('/drones', methods=['POST'])
def add_drone():
    data = request.get_json()
    drone = Drone(name=data['name'])
    db.session.add(drone)
    db.session.commit()
    return jsonify({'id': drone.id, 'name': drone.name}), 201