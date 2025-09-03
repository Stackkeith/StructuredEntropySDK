# AeonCore v2.0 - The API Server
# This script creates a Flask web server to act as a bridge between the
# user interface and the AeonCore engine (the Orchestrator).

from flask import Flask, jsonify, request, render_template
from .orchestrator import Orchestrator
from .directives import Directive
import threading
import time

# --- Initialization ---
app = Flask(__name__)
conductor = Orchestrator()

# A simple in-memory store for directive results.
# In a production system, this would be a more robust database or cache.
results_store = {}

# --- Frontend Route ---

@app.route("/")
def index():
    """Serves the main control panel."""
    return render_template("index.html")

# --- API Endpoints ---

@app.route("/api/status", methods=["GET"])
def get_status():
    """Returns the current status of all agents in the Quintet."""
    status_report = {agent.name: agent.report_status() for agent in conductor.agents.values()}
    return jsonify(status_report)

@app.route("/api/directives", methods=["POST"])
def create_directive():
    """
    Receives a new directive from the frontend, adds it to the
    Orchestrator's queue, and runs the simulation in a background thread.
    """
    data = request.get_json()
    if not data or "description" not in data or "target_agent_role" not in data:
        return jsonify({"error": "Invalid directive format."}), 400

    # Create and issue the directive
    directive = Directive(
        description=data["description"],
        target_agent_role=data["target_agent_role"],
        params=data.get("params", {})
    )
    conductor.issue_directive(directive)
    results_store[directive.id] = directive # Store for polling

    # Run the simulation in a background thread to avoid blocking the API
    def run_in_background():
        conductor.run_simulation()

    thread = threading.Thread(target=run_in_background)
    thread.start()

    return jsonify({"message": "Directive received.", "directive_id": directive.id}), 202

@app.route("/api/results/<directive_id>", methods=["GET"])
def get_result(directive_id: str):
    """Polls for the result of a specific directive."""
    directive = results_store.get(directive_id)
    if not directive:
        return jsonify({"error": "Directive not found."}), 404

    return jsonify({
        "directive_id": directive.id,
        "status": directive.status,
        "result": directive.result,
        "notes": directive.notes
    })

# --- Main Execution ---

if __name__ == "__main__":
    print("--- Starting AeonCore v2.0 API Server ---")
    # Running in debug mode is not recommended for production,
    # but it is perfect for our development phase.
    app.run(debug=True, port=5000)
