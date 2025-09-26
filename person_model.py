# person_model.py
from dataclasses import dataclass
from datetime import date, datetime

@dataclass
class Person:
    """
    A complete data class that represents all data for a person,
    combining the direct table fields and the calculated view fields.
    """
    # --- Core Identity ---
    id: int = 0
    room: str = ""
    nhi: str | None = None
    name: str | None = None
    legal_id: int | None = None

    # --- Due Dates ---
    treatment_plans_due: date | None = None
    honos_due: date | None = None
    uds_due: date | None = None
    
    # --- Last Completed Dates (Essential for Calculations) ---
    last_treatment_plan: date | None = None
    last_honos: date | None = None
    last_uds: date | None = None

    # --- Status Flags ---
    has_vnr: bool = False
    is_special_patient: bool = False
    rel_security: bool = False
    profile: bool = False
    metobolic: bool = False
    bloods: bool = False
    flight_risk: bool = False
    no_uds: bool = False

    # --- Other Details ---
    uds_frequency: str | None = None
    mdt_day: str | None = None
    leave_return: datetime | None = None
    progress_percent: float = 0.0
    special_notes: str | None = None

    # --- Staff Foreign Key IDs ---
    clinician_id: int | None = None
    case_manager_id: int | None = None
    case_manager_2nd_id: int | None = None
    associate_id: int | None = None
    associate_2nd_id: int | None = None
    
    # --- Fields from vw_WhiteboardData (for display) ---
    legal: str | None = None
    clinician_name: str | None = None
    case_managers: str | None = None
    associates: str | None = None