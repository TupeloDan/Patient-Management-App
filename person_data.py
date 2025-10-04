# person_data.py
import random
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from database import get_db_connection
from person_model import Person


class PersonData:
    """Manages all database operations for Person objects."""

    VALID_UPDATE_FIELDS = {
        "rel_security": "RelSecurity",
        "profile": "Profile",
        "metobolic": "Metobolic",
        "bloods": "Bloods",
        "flight_risk": "FlightRisk",
        "no_uds": "NoUDS",
        "uds_frequency": "UDSFrequency",
        "mdt_day": "MDTDay",
        "last_treatment_plan": "LastTreatmentPlan",
        "last_honos": "LastHonos",
        "last_uds": "LastUDS",
         "leave_return": "LeaveReturn",
    }

    def __init__(self):
        """Initializes the data manager."""
        self._people_cache = {}

    def _load_person_from_row(self, row: dict) -> Person | None:
        """Maps a database row from the vw_WhiteboardData view to the complete Person object."""
        if not row:
            return None

        return Person(
            id=row.get("ID"),
            room=row.get("Room"),
            nhi=row.get("NHI"),
            name=row.get("PersonName"),
            legal_id=row.get("LegalStatusID"),
            has_vnr=bool(row.get("HasVNR", False)),
            treatment_plans_due=row.get("TreatmentPlans"),
            honos_due=row.get("HoNos"),
            uds_due=row.get("UDSDue"),
            rel_security=bool(row.get("RelSecurity", False)),
            profile=bool(row.get("Profile", False)),
            metobolic=bool(row.get("Metobolic", False)),
            bloods=bool(row.get("Bloods", False)),
            flight_risk=bool(row.get("FlightRisk", False)),
            uds_frequency=row.get("UDSFrequency"),
            mdt_day=row.get("MDTDay"),
            leave_return=row.get("LeaveReturn"),
            progress_percent=row.get("Progress%", 0.0),
            special_notes=row.get("SpecialNotes"),
            is_special_patient=bool(row.get("IsSpecialPatient", False)),
            clinician_id=row.get("ClinicianID"),
            case_manager_id=row.get("CaseManagerID"),
            case_manager_2nd_id=row.get("CaseManager2ndID"),
            associate_id=row.get("AssociateID"),
            associate_2nd_id=row.get("Associate2ndID"),
            last_treatment_plan=row.get("LastTreatmentPlan"),
            last_honos=row.get("LastHonos"),
            last_uds=row.get("LastUDS"),
            no_uds=bool(row.get("NoUDS", False)),
            legal=row.get("Legal"),
            clinician_name=row.get("ClinicianName"),
            case_managers=row.get("CaseManagers"),
            associates=row.get("Associates"),
        )

    def get_sorted_people(self, include_empty_rooms: bool = False) -> list[Person]:
        """Fetches all people from the database by calling the sp_GetSortedPeople stored procedure."""
        conn = get_db_connection()
        if not conn:
            return []

        results_list = []
        self._people_cache.clear()

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc("sp_GetSortedPeople")
            for result in cursor.stored_results():
                all_rows = result.fetchall()

            for row in all_rows:
                person = self._load_person_from_row(row)
                if person:
                    self._people_cache[person.id] = person
                    if include_empty_rooms or person.nhi is not None:
                        results_list.append(person)

        except Exception as e:
            print(f"An error occurred while fetching people: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

        return results_list

    def get_person_by_id(self, person_id: int) -> Person | None:
        """Retrieves a single person from the database by their ID."""
        if person_id in self._people_cache:
            return self._people_cache.get(person_id)

        conn = get_db_connection()
        if not conn:
            return None

        person = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM vw_WhiteboardData WHERE ID = %s", (person_id,))
            row = cursor.fetchone()
            if row:
                person = self._load_person_from_row(row)
                self._people_cache[person_id] = person
        except Exception as e:
            print(f"An error occurred in get_person_by_id: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        
        return person

    def update_person(self, person: Person) -> bool:
        """Updates an existing person's record by calling the sp_UpdatePerson stored procedure."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            args = (
                person.id,
                person.nhi,
                person.name,
                person.legal_id,
                person.is_special_patient,
                person.has_vnr,
                person.special_notes,
            )
            cursor.callproc("sp_UpdatePerson", args)
            conn.commit()
            self._people_cache[person.id] = person
            print(f"Successfully updated person: {person.name}")
            return True

        except Exception as e:
            print(f"Error updating person: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def move_person(self, person_to_move: Person, destination_room_name: str) -> bool:
        """Moves a person to a new room by updating existing records via the sp_MovePerson stored procedure."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            args = (person_to_move.id, destination_room_name)
            cursor.callproc("sp_MovePerson", args)
            conn.commit()
            print(f"Successfully moved {person_to_move.name} to {destination_room_name}.")
            return True

        except Exception as e:
            print(f"Error moving person: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def assign_person_to_room(self, new_person_details: Person, destination_room_name: str) -> bool:
        """Assigns a new person's data to a specified empty room record."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            # THIS IS THE FIX: This now sends the correct 8 arguments in the right order.
            args = (
                new_person_details.nhi,
                new_person_details.name,
                new_person_details.legal_id,
                new_person_details.has_vnr,
                new_person_details.is_special_patient,
                new_person_details.special_notes,
                destination_room_name,
                0,  # Placeholder for the OUT parameter
            )
            cursor.callproc("sp_AssignPersonToRoom", args)
            conn.commit()
            print(f"Successfully assigned {new_person_details.name} to room {destination_room_name}.")
            return True

        except Exception as e:
            print(f"Error assigning person: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def remove_person(self, person_id: int) -> bool:
        """Clears a person's data from a room by calling the sp_RemovePerson stored procedure."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            args = (person_id,)
            cursor.callproc("sp_RemovePerson", args)
            conn.commit()
            print(f"Successfully removed person from record ID: {person_id}")
            return True

        except Exception as e:
            print(f"Error removing person: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def update_staff_assignments(self, person_id: int, clinician_id: int, cm_id: int, cm_2nd_id: int, assoc_id: int, assoc_2nd_id: int) -> bool:
        """Updates staff assignments for a person."""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            args = (person_id, clinician_id, cm_id, cm_2nd_id, assoc_id, assoc_2nd_id)
            cursor.callproc("sp_UpdateStaffAssignments", args)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating staff assignments: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def update_field(self, person_id: int, field_name: str, new_value) -> bool:
        """Updates a single field for a person in the database."""
        if field_name not in self.VALID_UPDATE_FIELDS:
            return False
        db_column_name = self.VALID_UPDATE_FIELDS[field_name]
        sql = f"UPDATE People SET `{db_column_name}` = %s WHERE ID = %s"
        return self._execute_update(sql, (new_value, person_id))

    def update_plan_due_date(self, person_id: int, completed_date: date) -> bool:
        """Calculates and updates the next treatment plan due date."""
        new_due_date = completed_date + relativedelta(months=3)
        sql = "UPDATE People SET TreatmentPlans = %s, LastTreatmentPlan = %s WHERE ID = %s"
        return self._execute_update(sql, (new_due_date, completed_date, person_id))

    def update_honos_due_date(self, person_id: int, completed_date: date) -> bool:
        """Calculates and updates the next HoNos due date."""
        new_due_date = completed_date + relativedelta(months=3)
        sql = "UPDATE People SET HoNos = %s, LastHonos = %s WHERE ID = %s"
        return self._execute_update(sql, (new_due_date, completed_date, person_id))

    def update_uds_due_date(self, person_id: int, last_test_date: date) -> bool:
        """Calculates and updates the next UDS due date based on frequency."""
        person = self.get_person_by_id(person_id)
        if not person: return False
        
        frequency = (person.uds_frequency or "WEEKLY").upper()
        if frequency == "BI-WEEKLY": new_due_date = last_test_date + timedelta(days=14)
        elif frequency == "WEEKLY": new_due_date = last_test_date + timedelta(weeks=1)
        elif frequency == "MONTHLY": new_due_date = last_test_date + relativedelta(months=1)
        elif frequency == "RANDOM": new_due_date = date.today() + timedelta(days=random.randint(7, 28))
        else: new_due_date = date.today()

        sql = "UPDATE People SET UDSDue = %s, LastUDS = %s WHERE ID = %s"
        return self._execute_update(sql, (new_due_date, last_test_date, person_id))
        
    def get_person_by_nhi(self, nhi: str) -> Person | None:
        """Retrieves a single person from the database by their NHI number."""
        conn = get_db_connection()
        if not conn: return None
        person = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM vw_WhiteboardData WHERE NHI = %s", (nhi,))
            row = cursor.fetchone()
            if row:
                person = self._load_person_from_row(row)
        except Exception as e:
            print(f"An error occurred in get_person_by_nhi: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return person
    
    def clear_all_leave_returns(self) -> bool:
        """Sets the LeaveReturn field to NULL for all records in the People table."""
        sql = "UPDATE People SET LeaveReturn = NULL"
        return self._execute_update(sql, ())

    def _execute_update(self, sql: str, values: tuple) -> bool:
        """A private helper to run simple update queries."""
        conn = get_db_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error during DB update: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                conn.close()