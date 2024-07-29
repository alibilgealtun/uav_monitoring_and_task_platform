from flask import jsonify

def register_error_handlers(app):
    """
    Registers custom error handlers for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """

    @app.errorhandler(404)
    def resource_not_found(e):
        """
        Handles 404 Not Found errors.

        Args:
            e (Exception): The exception that was raised.

        Returns:
            Response: A JSON response with the error message and a 404 status code.
        """
        return jsonify({'error': 'Resource not found', 'message': str(e)}), 404

    @app.errorhandler(400)
    def bad_request(e):
        """
        Handles 400 Bad Request errors.

        Args:
            e (Exception): The exception that was raised.

        Returns:
            Response: A JSON response with the error message and a 400 status code.
        """
        return jsonify({'error': 'Bad request', 'message': str(e)}), 400

    @app.errorhandler(500)
    def internal_server_error(e):
        """
        Handles 500 Internal Server Error errors.

        Args:
            e (Exception): The exception that was raised.

        Returns:
            Response: A JSON response with the error message and a 500 status code.
        """
        return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred. Please try again later.'}), 500

    @app.errorhandler(401)
    def unauthorized(e):
        """
        Handles 401 Unauthorized errors.

        Args:
            e (Exception): The exception that was raised.

        Returns:
            Response: A JSON response with the error message and a 401 status code.
        """
        return jsonify({'error': 'Unauthorized', 'message': str(e)}), 401

    @app.errorhandler(403)
    def forbidden(e):
        """
        Handles 403 Forbidden errors.

        Args:
            e (Exception): The exception that was raised.

        Returns:
            Response: A JSON response with the error message and a 403 status code.
        """
        return jsonify({'error': 'Forbidden', 'message': str(e)}), 403