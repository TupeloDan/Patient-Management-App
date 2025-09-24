# person_model.py
from dataclasses import dataclass
from datetime import date, datetime

@dataclass
class Person:
    """A data class that directly represents a row in the People table."""
    id: int = 0
    room: str = ""
    nhi: str | None = None
    name: str | None = None
    legal_id: int | None = None
    has_vnr: bool = False
    treatment_plans_due: date | None = None
    honos_due: date | None = None
    uds_due: date | None = None
    rel_security: bool = False
    profile: bool = False
    metobolic: bool = False
    bloods: bool = False
    flight_risk: bool = False
    uds_frequency: str | None = None
    mdt_day: str | None = None
    leave_return: datetime | None = None
    progress_percent: float = 0.0
    special_notes: str | None = None
    is_special_patient: bool = False
    # --- Staff Foreign Key IDs ---
    clinician_id: int | None = None
    case_manager_id: int | None = None
    case_manager_2nd_id: int | None = None
    associate_id: int | None = None
    associate_2nd_id: int | None = None
    last_treatment_plan: date | None = None
    last_honos: date | None = None
    last_uds: date | None = None