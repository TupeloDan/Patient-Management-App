import json
import os
from flask import Flask, jsonify, request, render_template, send_from_directory
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
from report_generator import create_leave_report
from role_data import RoleData

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

REPORTS_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')

# --- Initialize all data managers ---
person_manager = PersonData()
leave_manager = LeaveRecordData()
notice_manager = NoticeData()
staff_manager = StaffData()
ui_text_manager = UiTextData()
mha_section_manager = MhaSectionData()
role_manager = RoleData()

# ===================================================================
# --- RENDER ROUTES ---
# ===================================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main-editor')
def main_editor():
    return render_template('main-editor.html')

@app.route('/management')
def management():
    return render_template('management.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
    
@app.route('/staff-management')
def staff_management():
    return render_template('staff-management.html')

@app.route('/reports/<path:filename>')
def serve_report(filename):
    return send_from_directory(REPORTS_DIRECTORY, filename)

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
    response_json = json.dumps(on_leave_list, default=json_serial)
    return app.response_class(response=response_json, status=200, mimetype='application/json')

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

@app.route("/api/ui-text", methods=["GET"])
def get_ui_text():
    context = request.args.get('context')
    if not context: return jsonify({"error": "A 'context' parameter is required."}), 400
    text_elements = ui_text_manager.get_ui_text_by_context(context)
    return jsonify(text_elements)

@app.route("/api/people/<int:person_id>/leaves", methods=["GET"])
def get_person_leaves(person_id):
    person = person_manager.get_person_by_id(person_id)
    if not person or not person.nhi:
        return jsonify({"error": "Person not found or has no NHI"}), 404
    leave_records = leave_manager.get_leave_for_person(person.nhi)
    for record in leave_records:
        leave_time_obj = record.get('LeaveTime')
        if isinstance(leave_time_obj, str):
            leave_time_obj = datetime.fromisoformat(leave_time_obj)
        record['LeaveTime_formatted'] = leave_time_obj.strftime('%I:%M %p') if leave_time_obj else ''
        return_time_obj = record.get('ReturnTime')
        if isinstance(return_time_obj, str):
            return_time_obj = datetime.fromisoformat(return_time_obj)
        record['ReturnTime_formatted'] = return_time_obj.strftime('%I:%M %p') if return_time_obj else 'N/A'
    return jsonify(leave_records)

@app.route("/api/people/<int:person_id>/last-leave-description", methods=["GET"])
def get_last_leave_description(person_id):
    person = person_manager.get_person_by_id(person_id)
    if not person or not person.nhi:
        return jsonify({"error": "Person not found"}), 404
    last_description = leave_manager.get_last_leave_description(person.nhi)
    return jsonify({"last_description": last_description})

@app.route("/api/people/<int:person_id>/assignments", methods=["PUT"])
def update_assignments(person_id):
    data = request.json
    success = person_manager.update_staff_assignments(person_id, data.get('clinician_id'), data.get('case_manager_id'), data.get('case_manager_2nd_id'), data.get('associate_id'), data.get('associate_2nd_id'))
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
    data = request.json
    date_str = data.get("completed_date")
    completed_date = datetime.strptime(date_str, "%d/%m/%Y").date()
    success = person_manager.update_plan_due_date(person_id, completed_date)
    if success: return jsonify({"message": "Plan date updated successfully."}), 200
    return jsonify({"error": "Failed to update plan date."}), 500

@app.route("/api/people/<int:person_id>/update-honos-date", methods=["POST"])
def update_honos_date(person_id):
    data = request.json
    date_str = data.get("completed_date")
    completed_date = datetime.strptime(date_str, "%d/%m/%Y").date()
    success = person_manager.update_honos_due_date(person_id, completed_date)
    if success: return jsonify({"message": "HoNos date updated successfully."}), 200
    return jsonify({"error": "Failed to update HoNos date."}), 500

@app.route("/api/people/<int:person_id>/update-uds-date", methods=["POST"])
def update_uds_date(person_id):
    data = request.json
    date_str = data.get("last_test_date")
    last_test_date = datetime.strptime(date_str, "%d/%m/%Y").date()
    success = person_manager.update_uds_due_date(person_id, last_test_date)
    if success: return jsonify({"message": "UDS date updated successfully."}), 200
    return jsonify({"error": "Failed to update UDS date."}), 500

@app.route("/api/people/assign", methods=["POST"])
def assign_person():
    data = request.json
    new_person = Person(nhi=data.get('nhi'), name=data.get('name'), legal_id=data.get('legal_id'), is_special_patient=data.get('is_special_patient'), has_vnr=data.get('has_vnr'), special_notes=data.get('special_notes'))
    success = person_manager.assign_person_to_room(new_person, data['room'])
    if success: return jsonify({"message": "Person assigned successfully"}), 201
    return jsonify({"error": "Failed to assign person"}), 500

@app.route("/api/people/edit", methods=["PUT"])
def edit_person():
    data = request.json
    person_to_update = person_manager.get_person_by_id(int(data['id']))
    if not person_to_update: return jsonify({"error": "Person not found"}), 404
    person_to_update.nhi = data.get('nhi')
    person_to_update.name = data.get('name')
    person_to_update.legal_id = data.get('legal_id')
    person_to_update.is_special_patient = data.get('is_special_patient')
    person_to_update.has_vnr = data.get('has_vnr')
    person_to_update.special_notes = data.get('special_notes')
    success = person_manager.update_person(person_to_update)
    if success: return jsonify({"message": "Person updated successfully"}), 200
    return jsonify({"error": "Failed to update person"}), 500

@app.route("/api/people/move", methods=["POST"])
def move_person():
    data = request.json
    person_to_move = person_manager.get_person_by_id(int(data['personId']))
    if not person_to_move: return jsonify({"error": "Person not found"}), 404
    success = person_manager.move_person(person_to_move, data['destinationRoom'])
    if success: return jsonify({"message": "Person moved successfully"}), 200
    return jsonify({"error": "Failed to move person"}), 500

@app.route("/api/people/remove/<int:person_id>", methods=["DELETE"])
def remove_person_from_room(person_id):
    success = person_manager.remove_person(person_id)
    if success: return jsonify({"message": "Person removed successfully"}), 200
    return jsonify({"error": "Failed to remove person"}), 500

@app.route("/api/leaves", methods=["POST"])
def add_leave():
    data = request.json
    if not data: return jsonify({"error": "Invalid data provided"}), 400
    staff_responsible_id = data.get('staff_responsible_id')
    staff_mse_id = data.get('staff_mse_id') or staff_responsible_id
    try:
        person = person_manager.get_person_by_nhi(data.get('nhi'))
        if not person: return jsonify({"error": "Patient not found."}), 404
        duration = int(data.get('duration_minutes', 0))
        now = datetime.now()
        new_leave = LeaveRecord(nhi=data.get('nhi'), patient_name=data.get('patient_name'), leave_date=now.date(), leave_time=now, expected_return_time=now + timedelta(minutes=duration), leave_type=data.get('leave_type'), duration_minutes=duration, leave_description=data.get('leave_description'), is_escorted_leave=data.get('is_escorted_leave'), is_special_patient=person.is_special_patient, staff_responsible_id=staff_responsible_id, staff_nurse_id=staff_mse_id, senior_nurse_id=data.get('senior_nurse_id'), contact_phone_number=data.get('contact_phone_number'), mse=data.get('mse_completed'), risk=data.get('risk_assessment_completed'), leave_conditions_met=data.get('leave_conditions_met'), awol_status=data.get('awol_aware'), has_ward_contact_info=data.get('contact_aware'))
        success = leave_manager.add_leave(new_leave)
        if not success or not new_leave.id: raise Exception("Failed to save the initial leave record to the database or get a valid ID.")
        person_manager.update_field(person.id, 'leave_return', new_leave.expected_return_time)
        all_staff_list = staff_manager.get_all_staff()
        staff_map = {staff['ID']: f"{staff['StaffName']} ({staff['Role']})" for staff in all_staff_list}
        staff_details = {'responsible_name': staff_map.get(new_leave.staff_responsible_id), 'mse_staff_name': staff_map.get(new_leave.staff_nurse_id), 'senior_nurse_name': staff_map.get(new_leave.senior_nurse_id)}
        filename_only = create_leave_report(new_leave, person, staff_details)
        if filename_only: leave_manager.update_leave_filename(new_leave.id, filename_only)
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
        if not success: raise Exception("Failed to update LeaveLog in the database.")
        leave_record = leave_manager.get_leave_by_id(leave_id)
        if not leave_record: return jsonify({"error": "Leave record not found after update."}), 404
        person = person_manager.get_person_by_nhi(leave_record.nhi)
        if person: person_manager.update_field(person.id, 'leave_return', None)
        all_staff_list = staff_manager.get_all_staff()
        staff_map = {staff['ID']: f"{staff['StaffName']} ({staff['Role']})" for staff in all_staff_list}
        staff_details = {'responsible_name': staff_map.get(leave_record.staff_responsible_id), 'mse_staff_name': staff_map.get(leave_record.staff_nurse_id), 'senior_nurse_name': staff_map.get(leave_record.senior_nurse_id)}
        return_details = {'return_time': return_time.strftime('%d-%m-%y %I:%M %p'), 'signed_in_by_name': staff_map.get(signed_in_by_id)}
        create_leave_report(leave_record, person, staff_details, return_details)
        return jsonify({"message": "Patient return logged and report updated."}), 200
    except Exception as e:
        print(f"Error logging patient return: {e}")
        return jsonify({"error": "Failed to log patient return."}), 500

@app.route('/api/ui-text/update', methods=['POST'])
def update_ui_texts():
    data = request.json
    context = data.get('context')
    updates = data.get('updates')
    if not context or not updates: return jsonify({"error": "Missing context or updates data"}), 400
    try:
        for control_name, new_text in updates.items():
            ui_text_manager.update_ui_text(context, control_name, new_text)
        return jsonify({"message": "UI text updated successfully"}), 200
    except Exception as e:
        print(f"Error in update_ui_texts: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

@app.route('/api/notices/add', methods=['POST'])
def add_new_notice():
    data = request.json
    notice_text = data.get('notice_text')
    expiry_date_str = data.get('expiry_date')
    if not notice_text or not expiry_date_str: return jsonify({"error": "Missing notice text or expiry date"}), 400
    try:
        expiry_date = datetime.strptime(expiry_date_str, "%d/%m/%Y").date()
        success = notice_manager.add_notice(notice_text, expiry_date)
        if success: return jsonify({"message": "Notice added successfully"}), 201
        return jsonify({"error": "Failed to add notice to database"}), 500
    except Exception as e:
        print(f"Error adding notice: {e}")
        return jsonify({"error": "An internal error occurred"}), 500
    

@app.route('/api/admin/clear-leave-returns', methods=['POST'])
def clear_all_leave_returns():
    try:
        success = person_manager.clear_all_leave_returns()
        if success: return jsonify({"message": "All leave return fields cleared"}), 200
        return jsonify({"error": "Failed to clear leave return fields"}), 500
    except Exception as e:
        print(f"Error clearing leave returns: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/roles', methods=['GET'])
def get_roles():
    roles = role_manager.get_all_roles()
    return jsonify(roles)

@app.route('/api/delegatable-staff', methods=['GET'])
def get_delegatable_staff():
    staff = staff_manager.get_delegatable_staff()
    return jsonify(staff)

@app.route('/api/staff/add', methods=['POST'])
def add_staff_member():
    data = request.json
    success = staff_manager.add_staff(data.get('name'), data.get('role_id'))
    if success: return jsonify({"message": "Staff added successfully"}), 201
    return jsonify({"error": "Failed to add staff"}), 500

@app.route('/api/staff/update/<int:staff_id>', methods=['PUT'])
def update_staff_member(staff_id):
    data = request.json
    success = staff_manager.update_staff(staff_id, data.get('name'), data.get('role_id'))
    if success: return jsonify({"message": "Staff updated successfully"}), 200
    return jsonify({"error": "Failed to update staff"}), 500

@app.route('/api/delegated-staff/update', methods=['POST'])
def update_delegated_staff_list():
    data = request.json
    staff_ids = data.get('staff_ids', [])
    success = staff_manager.update_delegated_staff(staff_ids)
    if success: return jsonify({"message": "Delegated staff updated successfully"}), 200
    return jsonify({"error": "Failed to update delegated staff"}), 500

@app.route('/api/roles/add', methods=['POST'])
def add_role():
    data = request.json
    success = role_manager.add_role(data.get('role_name'), data.get('description'))
    if success: return jsonify({"message": "Role added successfully"}), 201
    return jsonify({"error": "Failed to add role"}), 500

@app.route('/api/roles/update/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    data = request.json
    success = role_manager.update_role(role_id, data.get('role_name'), data.get('description'))
    if success: return jsonify({"message": "Role updated successfully"}), 200
    return jsonify({"error": "Failed to update role"}), 500

@app.route('/api/notices/all', methods=['GET'])
def get_all_notices():
    # Use json.dumps with the serial helper to handle date objects
    notices = notice_manager.get_all_notices()
    response_json = json.dumps(notices, default=json_serial)
    return app.response_class(response=response_json, status=200, mimetype='application/json')

@app.route('/api/notices/update/<int:notice_id>', methods=['PUT'])
def update_existing_notice(notice_id):
    data = request.json
    notice_text = data.get('notice_text')
    expiry_date_str = data.get('expiry_date')
    if not notice_text or not expiry_date_str:
        return jsonify({"error": "Missing notice text or expiry date"}), 400
    try:
        expiry_date = datetime.strptime(expiry_date_str, "%d/%m/%Y").date()
        success = notice_manager.update_notice(notice_id, notice_text, expiry_date)
        if success:
            return jsonify({"message": "Notice updated successfully"}), 200
        return jsonify({"error": "Failed to update notice"}), 500
    except Exception as e:
        print(f"Error updating notice: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/api/notices/delete/<int:notice_id>', methods=['DELETE'])
def delete_existing_notice(notice_id):
    try:
        success = notice_manager.delete_notice(notice_id)
        if success:
            return jsonify({"message": "Notice deleted successfully"}), 200
        return jsonify({"error": "Failed to delete notice"}), 500
    except Exception as e:
        print(f"Error deleting notice: {e}")
        return jsonify({"error": "An internal error occurred"}), 500
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)