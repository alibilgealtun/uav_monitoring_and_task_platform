from flask import jsonify, request
from ..models import Drone
from ..extensions import db
from . import bp

@bp.route('/drones', methods=['GET'])
def get_drones():
    drones = Drone.query.all()
    return jsonify([drone.to_dict() for drone in drones])

@bp.route('/drones', methods=['POST'])
def add_drone():
    data = request.get_json()
    drone = Drone(name=data['name'])
    db.session.add(drone)
    db.session.commit()
    return jsonify({'id': drone.id, 'name': drone.name}), 201