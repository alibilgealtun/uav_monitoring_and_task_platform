from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify({'error': 'Resource not found', 'message': str(e)}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'error': 'Bad request', 'message': str(e)}), 400

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred. Please try again later.'}), 500