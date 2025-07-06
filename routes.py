"""
Registers all the routes for the application
"""
from flask import Blueprint, jsonify

def register_routes(app):
    """
    Registers all the routes for the application
    """
    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint
        """
        return jsonify({'status': 'ok'}), 200
