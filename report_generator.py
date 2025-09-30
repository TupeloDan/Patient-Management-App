import os
from datetime import datetime
from flask import render_template
from weasyprint import HTML

# Create a directory to store reports if it doesn't exist
REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

def create_leave_report(leave_record, person, staff_details):
    """
    Generates a PDF leave report from a template and saves it.

    Args:
        leave_record (LeaveRecord): The leave record object.
        person (Person): The person object for the patient.
        staff_details (dict): A dictionary with the names of the assigned staff.

    Returns:
        str: The relative path to the saved PDF file.
    """
    try:
        # Format dates and times for display
        leave_date_str = leave_record.leave_date.strftime('%d-%b-%y')
        leave_time_str = leave_record.leave_time.strftime('%I:%M %p')
        expected_return_str = leave_record.expected_return_time.strftime('%d-%m-%y %I:%M %p')
        
        # Prepare the context for rendering the template
        context = {
            "leave_record": {
                **leave_record.__dict__,
                "leave_date": leave_date_str,
                "leave_time": leave_time_str,
                "expected_return_time": expected_return_str
            },
            "person": person,
            "staff_details": staff_details,
            "generation_time": datetime.now().strftime('%d-%m-%y %I:%M %p')
        }

        # Render the HTML template with the data
        html_string = render_template('leave_report_template.html', **context)

        # Generate a unique filename
        filename = f"{person.nhi}-LeaveEvent-{leave_record.id}-{leave_record.leave_date.strftime('%d-%b-%y')}.pdf"
        relative_path = os.path.join('reports', filename)
        output_path = os.path.join(REPORTS_DIR, filename)

        # Create PDF from HTML
        HTML(string=html_string).write_pdf(output_path)

        print(f"Successfully generated report: {output_path}")
        return filename

    except Exception as e:
        print(f"Error generating PDF report: {e}")
        return None