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
from role_data import RoleData # <-- FIX #1: This import was missing

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

# --- Initialize our data managers ---
person_manager = PersonData()
leave_manager = LeaveRecordData()
notice_manager = NoticeData()
staff_manager = StaffData()
ui_text_manager = UiTextData()
mha_section_manager = MhaSectionData()
role_manager = RoleData() # <-- FIX #2: This instance was missing

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
    if not context: 
        return jsonify({"error": "A 'context' parameter is required."}), 400
    
    text_elements = ui_text_manager.get_ui_text_by_context(context)
    return jsonify(text_elements)

# ... (the rest of your API routes are unchanged)

# --- NEW STAFF AND ROLE MANAGEMENT ROUTES ---
@app.route('/api/roles', methods=['GET'])
def get_roles():
    roles = role_manager.get_all_roles()
    return jsonify(roles)

@app.route('/api/staff/add', methods=['POST'])
def add_staff_member():
    data = request.json
    success = staff_manager.add_staff(data.get('name'), data.get('role_id'))
    if success:
        return jsonify({"message": "Staff added successfully"}), 201
    return jsonify({"error": "Failed to add staff"}), 500

@app.route('/api/staff/update/<int:staff_id>', methods=['PUT'])
def update_staff_member(staff_id):
    data = request.json
    success = staff_manager.update_staff(staff_id, data.get('name'), data.get('role_id'))
    if success:
        return jsonify({"message": "Staff updated successfully"}), 200
    return jsonify({"error": "Failed to update staff"}), 500

@app.route('/api/delegated-staff/update', methods=['POST'])
def update_delegated_staff_list():
    data = request.json
    staff_ids = data.get('staff_ids', [])
    success = staff_manager.update_delegated_staff(staff_ids)
    if success:
        return jsonify({"message": "Delegated staff updated successfully"}), 200
    return jsonify({"error": "Failed to update delegated staff"}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)