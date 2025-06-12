from .chat import chat_bp
from .ics205 import ics_bp


def register_routes(app):
    app.register_blueprint(chat_bp)
    app.register_blueprint(ics_bp)
