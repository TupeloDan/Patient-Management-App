import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import date, datetime

# --- Import our data managers ---
from person_data import PersonData
from person_model import Person
from leave_record_data import LeaveRecordData
from notice_data import NoticeData
from staff_data import StaffData


# --- Helper function for JSON serialization ---
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


# --- Flask App Initialization ---
app = Flask(__name__, template_folder="templates")
CORS(app)

# --- Initialize our data managers ---
person_manager = PersonData()
leave_manager = LeaveRecordData()
notice_manager = NoticeData()
staff_manager = StaffData()

# ===================================================================
# --- DISPLAY APP ROUTES ---
# ===================================================================


@app.route("/")
def index():
    """Renders the main display HTML page."""
    return render_template("index.html")


@app.route("/data")
def get_whiteboard_data():
    """Fetches the main whiteboard data from MySQL for the display."""
    try:
        people_list = person_manager.get_sorted_people(include_empty_rooms=True)
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


# ===================================================================
# --- EDITOR APP ROUTES & API ---
# ===================================================================


@app.route("/editor")
def editor():
    """Renders the main editor HTML page."""
    return render_template("editor.html")


@app.route("/api/people", methods=["GET"])
def get_people():
    """API endpoint to get the list of all people for the editor."""
    include_empty = request.args.get("include_empty", "false").lower() == "true"
    people_list = person_manager.get_sorted_people(include_empty_rooms=include_empty)
    people_json = json.dumps([p.__dict__ for p in people_list], default=json_serial)
    return app.response_class(
        response=people_json, status=200, mimetype="application/json"
    )


@app.route("/api/staff", methods=["GET"])
def get_all_staff():
    """API endpoint to get a list of all staff, with optional role filtering."""
    role_filters = request.args.getlist("role")
    staff = staff_manager.get_all_staff(roles=role_filters if role_filters else None)
    return jsonify(staff)


@app.route("/api/people/<int:person_id>/assignments", methods=["PUT"])
def update_assignments(person_id):
    """API endpoint to update all staff assignments for a person."""
    data = request.json
    success = person_manager.update_staff_assignments(
        person_id=person_id,
        clinician_id=data.get("clinician_id"),
        cm_id=data.get("case_manager_id"),
        cm_2nd_id=data.get("case_manager_2nd_id"),
        assoc_id=data.get("associate_id"),
        assoc_2nd_id=data.get("associate_2nd_id"),
    )
    if success:
        return jsonify({"message": "Assignments updated successfully"}), 200
    return jsonify({"error": "Failed to update assignments"}), 500


@app.route("/api/people/<int:person_id>/update-field", methods=["PATCH"])
def update_person_field(person_id):
    """API endpoint to update a single field for a person."""
    data = request.json
    field_name = data.get("field_name")
    new_value = data.get("new_value")
    if not field_name or new_value is None:
        return jsonify({"error": "Missing field_name or new_value"}), 400
    success = person_manager.update_field(person_id, field_name, new_value)
    if success:
        return jsonify({"message": f"Field {field_name} updated successfully"}), 200
    return jsonify({"error": f"Failed to update field {field_name}"}), 500

@app.route('/main-editor')
def main_editor():
    """Renders the main editor page."""
    return render_template('main-editor.html')

# --- RUN THE APP ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
