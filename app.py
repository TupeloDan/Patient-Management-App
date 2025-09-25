import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# --- Import our new MySQL data managers ---
from person_data import PersonData
from person_model import Person
from leave_record_data import LeaveRecordData
from notice_data import NoticeData


# A helper function to handle date serialization
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    from datetime import date, datetime

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


# --- FLASK APP INITIALIZATION ---
app = Flask(__name__, template_folder="templates")
CORS(app)

# --- Initialize our data managers ---
person_manager = PersonData()
leave_manager = LeaveRecordData()
notice_manager = NoticeData()


# --- DISPLAY ROUTES (from your original app) ---


@app.route("/")
def index():
    """Renders the main HTML page."""
    return render_template("index.html")


@app.route("/data")
def get_whiteboard_data():
    """
    Fetches the main whiteboard data from MySQL.
    This now calls our PersonData manager instead of using pyodbc.
    """
    try:
        # We fetch the full list of people, including empty rooms for the display
        people_list = person_manager.get_sorted_people(include_empty_rooms=True)
        # Convert objects to dictionaries for JSON serialization
        people_dicts = [p.__dict__ for p in people_list]
        people_json = json.dumps(people_dicts, default=json_serial)
        return app.response_class(
            response=people_json, status=200, mimetype="application/json"
        )
    except Exception as e:
        print(f"Error in get_whiteboard_data: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/notices")
def get_active_notices():
    """Fetches active notices from MySQL."""
    try:
        notices = notice_manager.get_active_notices()
        return jsonify(notices)
    except Exception as e:
        print(f"Error in get_active_notices: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/onleave")
def get_on_leave_data():
    """Fetches a list of all people currently on leave from MySQL."""
    try:
        on_leave_list = leave_manager.get_people_on_leave()
        return jsonify(on_leave_list)
    except Exception as e:
        print(f"Error in get_on_leave_data: {e}")
        return jsonify({"error": str(e)}), 500


# --- EDITOR API ENDPOINTS (our new code) ---


@app.route("/api/people", methods=["GET"])
def get_people():
    """API endpoint to get the list of all people."""
    include_empty = request.args.get("include_empty", "false").lower() == "true"
    people_list = person_manager.get_sorted_people(include_empty_rooms=include_empty)
    people_json = json.dumps([p.__dict__ for p in people_list], default=json_serial)
    return app.response_class(
        response=people_json, status=200, mimetype="application/json"
    )


@app.route("/api/people/<int:person_id>", methods=["GET"])
def get_person(person_id):
    """API endpoint to get details for a single person."""
    person = person_manager.get_person_by_id(person_id)
    if person:
        person_json = json.dumps(person.__dict__, default=json_serial)
        return app.response_class(
            response=person_json, status=200, mimetype="application/json"
        )
    return jsonify({"error": "Person not found"}), 404


@app.route("/api/people/<int:person_id>", methods=["PUT"])
def update_person(person_id):
    """API endpoint to update a person's details."""
    data = request.json
    person_to_update = Person(**data)
    person_to_update.id = person_id
    success = person_manager.update_person(person_to_update)
    if success:
        return jsonify({"message": "Person updated successfully"}), 200
    return jsonify({"error": "Failed to update person"}), 500


@app.route("/api/people/assign", methods=["POST"])
def assign_person():
    """API endpoint to assign a new person to an empty room."""
    data = request.json
    room_name = data.get("room")
    person_details = data.get("person")
    if not room_name or not person_details:
        return jsonify({"error": "Missing room or person details"}), 400
    new_person = Person(**person_details)
    success = person_manager.assign_person_to_room(new_person, room_name)
    if success:
        return jsonify({"message": f"Assigned {new_person.name} to {room_name}"}), 201
    return jsonify({"error": "Failed to assign person"}), 500


@app.route("/api/people/remove/<int:person_id>", methods=["DELETE"])
def remove_person(person_id):
    """API endpoint to remove a person's details from a room."""
    success = person_manager.remove_person(person_id)
    if success:
        return jsonify({"message": "Person removed successfully"}), 200
    return jsonify({"error": "Failed to remove person"}), 500


# --- RUN THE APP ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
