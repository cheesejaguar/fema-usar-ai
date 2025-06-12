from flask import Blueprint, request, jsonify, current_app
from utils.auth import require_api_key

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/api/chat", methods=["POST"])
@require_api_key
def chat():
    data = request.get_json() or {}
    message = data.get("message")
    if not message:
        return jsonify({"error": "message required"}), 400
    llm_service = current_app.llm_service
    response = llm_service.generate(message)
    return jsonify({"response": response})
