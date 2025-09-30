# tupelodan/patient-management-app/Patient-Management-App-11280d08229d043412bbfeabe6ca9e8da6cbe246/app.py
import json
import os
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from datetime import date, datetime, timedelta

# --- Import our data managers ---
from person_data import PersonData
from leave_record_data import LeaveRecordData
from notice_data import NoticeData
from staff_data import StaffData
from ui_text_data import UiTextData
from report_generator import create_leave_report
from leave_record_model import LeaveRecord

# --- Helper function for JSON serialization ---
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    raise TypeError(f"Type {type(obj)} not serializable")

# --- Flask App Initialization ---
app = Flask(__name__, template_folder="templates")
CORS(app)

# --- Define Constants ---
REPORTS_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')

# --- Initialize our data managers ---
person_manager = PersonData()
leave_manager = LeaveRecordData()
notice_manager = NoticeData()
staff_manager = StaffData()
ui_text_manager = UiTextData()

# ===================================================================
# --- RENDER & FILE SERVING ROUTES ---
# ===================================================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/editor')
def editor():
    return render_template('editor.html')

@app.route('/main-editor')
def main_editor():
    return render_template('main-editor.html')

@app.route('/reports/<path:filename>')
def serve_report(filename):
    return send_from_directory(REPORTS_DIRECTORY, filename)

# ===================================================================
# --- API ROUTES ---
# ===================================================================
@app.route('/data')
def get_whiteboard_data():
    people_list = person_manager.get_sorted_people(include_empty_rooms=True)
    return json.dumps([p.__dict__ for p in people_list], default=json_serial)

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
    return jsonify([p.__dict__ for p in people_list])

@app.route("/api/staff", methods=["GET"])
def get_all_staff():
    role_filters = request.args.getlist('role')
    staff = staff_manager.get_all_staff(roles=role_filters if role_filters else None)
    return jsonify(staff)

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

    # --- FIX: Robustly format the dates and times on the server ---
    for record in leave_records:
        # The database may return datetime objects or ISO strings. Handle both.
        leave_time_obj = record.get('LeaveTime')
        if isinstance(leave_time_obj, str):
            leave_time_obj = datetime.fromisoformat(leave_time_obj)
        record['LeaveTime_formatted'] = leave_time_obj.strftime('%I:%M %p') if leave_time_obj else ''
        
        return_time_obj = record.get('ReturnTime')
        if isinstance(return_time_obj, str):
            return_time_obj = datetime.fromisoformat(return_time_obj)
        record['ReturnTime_formatted'] = return_time_obj.strftime('%I:%M %p') if return_time_obj else 'N/A'
    # --- END FIX ---
            
    return jsonify(leave_records)

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

@app.route("/api/leaves", methods=["POST"])
def add_leave():
    data = request.json
    if not data: return jsonify({"error": "Invalid data provided"}), 400

    existing_leaves = leave_manager.get_leave_for_person(data.get('nhi'))
    if any(leave.get('ReturnTime') is None for leave in existing_leaves):
        return jsonify({"error": "This patient is already on an active leave."}), 409

    required_fields = ['nhi', 'patient_name', 'leave_type', 'duration_minutes', 'staff_responsible_id', 'staff_mse_id', 'senior_nurse_id', 'leave_description']
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    try:
        duration = int(data.get('duration_minutes', 0))
        leave_date = date.today()
        leave_time = datetime.now()
        expected_return = leave_time + timedelta(minutes=duration)
        
        new_leave = LeaveRecord(
            nhi=data.get('nhi'), patient_name=data.get('patient_name'), leave_date=leave_date,
            leave_time=leave_time, expected_return_time=expected_return, leave_type=data.get('leave_type'),
            duration_minutes=duration, leave_description=data.get('leave_description'), is_escorted_leave=data.get('is_escorted_leave'),
            staff_responsible_id=data.get('staff_responsible_id'), staff_nurse_id=data.get('staff_mse_id'),
            senior_nurse_id=data.get('senior_nurse_id'), contact_phone_number=data.get('contact_phone_number'),
            mse=data.get('mse_completed'), risk=data.get('risk_assessment_completed'),
            leave_conditions_met=data.get('leave_conditions_met'), awol_status=data.get('awol_aware'),
            has_ward_contact_info=data.get('contact_aware')
        )
        
        success = leave_manager.add_leave(new_leave)
        if not success:
            raise Exception("Failed to save the initial leave record to the database.")

        person = person_manager.get_person_by_nhi(data.get('nhi'))
        if person:
            person_manager.update_field(person.id, 'leave_return', new_leave.expected_return_time)
        
        all_staff_list = staff_manager.get_all_staff()
        staff_map = {staff['ID']: f"{staff['StaffName']} ({staff['Role']})" for staff in all_staff_list}
        
        staff_details = {
            'responsible_name': staff_map.get(new_leave.staff_responsible_id),
            'mse_staff_name': staff_map.get(new_leave.staff_nurse_id),
            'senior_nurse_name': staff_map.get(new_leave.senior_nurse_id)
        }

        filename_only = create_leave_report(new_leave, person, staff_details)
        if filename_only:
            leave_manager.update_leave_filename(new_leave.id, filename_only)
        
        return jsonify({"message": "Leave created and report generated successfully"}), 201

    except Exception as e:
        print(f"Error in the leave creation process: {e}")
        return jsonify({"error": "Failed to create leave record or report."}), 500

@app.route('/api/leaves/<int:leave_id>/return', methods=['POST'])
def log_leave_return(leave_id):
    data = request.json
    signed_in_by_id = data.get('signed_in_by_id')
    if not signed_in_by_id: return jsonify({"error": "Missing signed_in_by_id"}), 400
    try:
        return_time = datetime.now()
        success = leave_manager.log_return(leave_id, return_time, signed_in_by_id)
        if not success:
            raise Exception("Failed to update LeaveLog.")
        
        leave_record = leave_manager.get_leave_by_id(leave_id)
        if not leave_record:
             return jsonify({"error": "Leave record not found."}), 404

        person = person_manager.get_person_by_nhi(leave_record.nhi)
        if person:
            person_manager.update_field(person.id, 'leave_return', None)
        else:
            print(f"Warning: Could not find person with NHI {leave_record.nhi} to clear LeaveReturn status.")

        all_staff_list = staff_manager.get_all_staff()
        staff_map = {staff['ID']: f"{staff['StaffName']} ({staff['Role']})" for staff in all_staff_list}
        
        staff_details = {
            'responsible_name': staff_map.get(leave_record.staff_responsible_id),
            'mse_staff_name': staff_map.get(leave_record.staff_nurse_id),
            'senior_nurse_name': staff_map.get(leave_record.senior_nurse_id)
        }
        return_details = {
            'return_time': return_time.strftime('%d-%m-%y %I:%M %p'),
            'signed_in_by_name': staff_map.get(signed_in_by_id)
        }
        
        create_leave_report(leave_record, person, staff_details, return_details)

        return jsonify({"message": "Patient return logged and report updated."}), 200
        
    except Exception as e:
        print(f"Error logging patient return: {e}")
        return jsonify({"error": "Failed to log patient return."}), 500

# --- RUN THE APP ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)