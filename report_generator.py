import os
from datetime import datetime
from flask import render_template
from weasyprint import HTML

REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

# MODIFIED: Function now correctly accepts optional return_details
def create_leave_report(leave_record, person, staff_details, return_details=None):
    """
    Generates or regenerates a PDF leave report and saves it, overwriting if it exists.
    """
    try:
        context = {
            "leave_record": {
                **leave_record.__dict__,
                "leave_date": leave_record.leave_date.strftime('%d-%b-%y'),
                "leave_time": leave_record.leave_time.strftime('%I:%M %p'),
                "expected_return_time": leave_record.expected_return_time.strftime('%d-%m-%y %I:%M %p')
            },
            "person": person,
            "staff_details": staff_details,
            "return_details": return_details, # Pass the new details to the template
            "generation_time": datetime.now().strftime('%d-%m-%y %I:%M %p')
        }

        html_string = render_template('leave_report_template.html', **context)

        # Use existing filename from the record if available, otherwise create a new one
        if hasattr(leave_record, 'file_name') and leave_record.file_name:
            filename = os.path.basename(leave_record.file_name)
        else:
            filename = f"{person.nhi}-LeaveEvent-{leave_record.id}-{leave_record.leave_date.strftime('%d-%b-%y')}.pdf"
        
        output_path = os.path.join(REPORTS_DIR, filename)

        HTML(string=html_string).write_pdf(output_path)
        
        print(f"Successfully generated/updated report: {output_path}")
        return filename

    except Exception as e:
        print(f"Error generating PDF report: {e}")
        return None