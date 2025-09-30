# leave_record_model.py
from dataclasses import dataclass
from datetime import date, datetime

@dataclass
class LeaveRecord:
    """A data class that represents a single patient leave record."""
    id: int = 0
    nhi: str = ""
    patient_name: str = ""
    leave_date: date | None = None
    leave_time: datetime | None = None
    return_time: datetime | None = None
    expected_return_time: datetime | None = None
    leave_type: str | None = None
    duration_minutes: int | None = None
    mse: str | None = None
    risk: str | None = None
    leave_conditions_met: bool = False
    awol_status: bool = False
    has_ward_contact_info: bool = False
    contact_phone_number: str | None = None
    is_special_leave: bool = False
    is_escorted_leave: bool = False
    senior_nurse_notified: bool = False
    senior_nurse_id: int | None = None
    staff_nurse_id: int | None = None
    staff_responsible_id: int | None = None
    leave_signed_in_by_id: int | None = None
    own_phone: bool = False
    file_name: str | None = None
    leave_description: str | None = None