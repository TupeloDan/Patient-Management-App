import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import date, datetime, timedelta

# --- Import our data managers ---
from person_data import PersonData
from person_model import Person
from leave_record_data import LeaveRecordData
from leave_record_model import LeaveRecord
from notice_data import NoticeData
from staff_data import StaffData
from ui_text_data import UiTextData
from mha_section_data import MhaSectionData

# --- Helper function for JSON serialization ---
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

# --- Flask App Initialization ---
app = Flask(__name__, template_folder="templates")
CORS(app)

# --- Initialize our data managers ---
person_manager = PersonData()
leave_manager = LeaveRecordData()
notice_manager = NoticeData()
staff_manager = StaffData()
ui_text_manager = UiTextData()
mha_section_manager = MhaSectionData()

# ===================================================================
# --- RENDER ROUTES ---
# ===================================================================

@app.route('/')
def index():
    return render_template('index.html')

# The '/editor' route is now removed

@app.route('/main-editor')
def main_editor():
    return render_template('main-editor.html')

@app.route('/management')
def management():
    return render_template('management.html')

# ===================================================================
# --- API ROUTES ---
# ===================================================================

@app.route('/data')
def get_whiteboard_data():
    people_list = person_manager.get_sorted_people(include_empty_rooms=True)
    people_json = json.dumps([p.__dict__ for p in people_list], default=json_serial)
    return app.response_class(response=people_json, status=200, mimetype='application/json')

@app.route('/api/notices')
def get_active_notices():
    notices = notice_manager.get_active_notices()
    return jsonify(notices)

@app.route('/api/onleave')
def get_on_leave_data():
    on_leave_list = leave_manager.get_people_on_leave()
    return jsonify(on_leave_list)

@app.route("/api/people", methods=["GET"])
def get_people():
    people_list = person_manager.get_sorted_people(include_empty_rooms=True)
    people_json = json.dumps([p.__dict__ for p in people_list], default=json_serial)
    return app.response_class(response=people_json, status=200, mimetype='application/json')

@app.route("/api/staff", methods=["GET"])
def get_all_staff():
    role_filters = request.args.getlist('role')
    staff = staff_manager.get_all_staff(roles=role_filters if role_filters else None)
    return jsonify(staff)
    
@app.route("/api/mha-sections", methods=["GET"])
def get_mha_sections():
    sections = mha_section_manager.get_all_mha_sections()
    return jsonify(sections)

@app.route("/api/nhi/check/<nhi>", methods=["GET"])
def check_nhi(nhi):
    person = person_manager.get_person_by_nhi(nhi)
    return jsonify({"exists": person is not None})

@app.route("/api/delegated-staff", methods=["GET"])
def get_delegated_staff():
    staff = staff_manager.get_delegated_staff()
    return jsonify(staff)

@app.route("/api/people/<int:person_id>/leaves", methods=["GET"])
def get_person_leaves(person_id):
    person = person_manager.get_person_by_id(person_id)
    if not person or not person.nhi:
        return jsonify({"error": "Person not found or has no NHI"}), 404
    leave_records = leave_manager.get_leave_for_person(person.nhi)
    leaves_json = json.dumps(leave_records, default=json_serial)
    return app.response_class(response=leaves_json, status=200, mimetype='application/json')

@app.route("/api/people/<int:person_id>/assignments", methods=["PUT"])
def update_assignments(person_id):
    data = request.json
    success = person_manager.update_staff_assignments(
        person_id=person_id, clinician_id=data.get('clinician_id'),
        cm_id=data.get('case_manager_id'), cm_2nd_id=data.get('case_manager_2nd_id'),
        assoc_id=data.get('associate_id'), assoc_2nd_id=data.get('associate_2nd_id')
    )
    if success: return jsonify({"message": "Assignments updated successfully"}), 200
    return jsonify({"error": "Failed to update assignments"}), 500

@app.route("/api/people/<int:person_id>/update-field", methods=["PATCH"])
def update_person_field(person_id):
    data = request.json
    field_name = data.get("field_name")
    new_value = data.get("new_value")
    if not field_name: return jsonify({"error": "Missing field_name"}), 400
    success = person_manager.update_field(person_id, field_name, new_value)
    if success: return jsonify({"message": f"Field {field_name} updated successfully"}), 200
    return jsonify({"error": f"Failed to update field {field_name}"}), 500

@app.route("/api/people/<int:person_id>/update-plan-date", methods=["POST"])
def update_plan_date(person_id):
    data = request.json; date_str = data.get("completed_date")
    completed_date = datetime.strptime(date_str, "%d/%m/%Y").date()
    success = person_manager.update_plan_due_date(person_id, completed_date)
    if success: return jsonify({"message": "Plan date updated successfully."}), 200
    return jsonify({"error": "Failed to update plan date."}), 500

@app.route("/api/people/<int:person_id>/update-honos-date", methods=["POST"])
def update_honos_date(person_id):
    data = request.json; date_str = data.get("completed_date")
    completed_date = datetime.strptime(date_str, "%d/%m/%Y").date()
    success = person_manager.update_honos_due_date(person_id, completed_date)
    if success: return jsonify({"message": "HoNos date updated successfully."}), 200
    return jsonify({"error": "Failed to update HoNos date."}), 500

@app.route("/api/people/<int:person_id>/update-uds-date", methods=["POST"])
def update_uds_date(person_id):
    data = request.json; date_str = data.get("last_test_date")
    last_test_date = datetime.strptime(date_str, "%d/%m/%Y").date()
    success = person_manager.update_uds_due_date(person_id, last_test_date)
    if success: return jsonify({"message": "UDS date updated successfully."}), 200
    return jsonify({"error": "Failed to update UDS date."}), 500

@app.route("/api/ui-text", methods=["GET"])
def get_ui_text():
    context = request.args.get('context')
    if not context: return jsonify({"error": "A 'context' parameter is required."}), 400
    text_elements = ui_text_manager.get_ui_text_by_context(context)
    return jsonify(text_elements)

@app.route("/api/people/assign", methods=["POST"])
def assign_person():
    data = request.json
    new_person = Person(
        nhi=data.get('nhi'), 
        name=data.get('name'), 
        legal_id=data.get('legal_id'), 
        is_special_patient=data.get('is_special_patient'), 
        has_vnr=data.get('has_vnr'), 
        special_notes=data.get('special_notes')
    )
    success = person_manager.assign_person_to_room(new_person, data['room'])
    if success:
        return jsonify({"message": "Person assigned successfully"}), 201
    else:
        return jsonify({"error": "Failed to assign person"}), 500

@app.route("/api/people/edit", methods=["PUT"])
def edit_person():
    data = request.json
    person_to_update = person_manager.get_person_by_id(int(data['id']))
    if not person_to_update:
        return jsonify({"error": "Person not found"}), 404
    
    person_to_update.nhi = data.get('nhi')
    person_to_update.name = data.get('name')
    person_to_update.legal_id = data.get('legal_id')
    person_to_update.is_special_patient = data.get('is_special_patient')
    person_to_update.has_vnr = data.get('has_vnr')
    person_to_update.special_notes = data.get('special_notes')

    success = person_manager.update_person(person_to_update)
    if success:
        return jsonify({"message": "Person updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update person"}), 500

@app.route("/api/people/move", methods=["POST"])
def move_person():
    data = request.json
    person_to_move = person_manager.get_person_by_id(int(data['personId']))
    if not person_to_move:
        return jsonify({"error": "Person not found"}), 404
    
    success = person_manager.move_person(person_to_move, data['destinationRoom'])
    if success:
        return jsonify({"message": "Person moved successfully"}), 200
    else:
        return jsonify({"error": "Failed to move person"}), 500

@app.route("/api/leaves", methods=["POST"])
def add_leave():
    # This is the simplified, original add_leave function
    data = request.json
    if not data: return jsonify({"error": "Invalid data provided"}), 400
    try:
        leave_date = date.today()
        leave_time = datetime.now()
        duration = int(data.get('duration_minutes', 0))
        expected_return = leave_time + timedelta(minutes=duration)
        new_leave = LeaveRecord(
            nhi=data.get('nhi'), patient_name=data.get('patient_name'),
            leave_date=leave_date, leave_time=leave_time,
            expected_return_time=expected_return,
            leave_type=data.get('leave_type'),
            leave_description=data.get('leave_description'),
            is_escorted_leave=data.get('is_escorted_leave')
        )
        success = leave_manager.add_leave(new_leave)
        if success: return jsonify({"message": "Leave created successfully"}), 201
        else: raise Exception("Failed to save to database.")
    except Exception as e:
        print(f"Error creating leave record: {e}")
        return jsonify({"error": "Failed to create leave record."}), 500

# --- RUN THE APP ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)