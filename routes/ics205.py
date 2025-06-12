from flask import Blueprint, request, jsonify, current_app
from utils.auth import require_api_key

ics_bp = Blueprint("ics205", __name__)


@ics_bp.route("/api/ics205", methods=["POST"])
@require_api_key
def generate_ics205():
    data = request.get_json() or {}
    incident = data.get("incident")
    if not incident:
        return jsonify({"error": "incident required"}), 400
    llm_service = current_app.llm_service
    prompt = (
        f"Prepare an ICS 205 Incident Radio Communications Plan for this incident: {incident}. "
        "Return the plan as a Markdown table."
    )
    response = llm_service.generate(prompt)
    return jsonify({"ics205": response})
