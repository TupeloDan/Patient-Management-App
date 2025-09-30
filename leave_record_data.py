# leave_record_data.py
from datetime import datetime
from database import get_db_connection
from leave_record_model import LeaveRecord

class LeaveRecordData:
    """Manages all database operations for LeaveRecord objects."""

    def __init__(self):
        """Initializes the data manager."""
        self._leave_cache = {}

    def _load_leave_from_row(self, row: dict) -> LeaveRecord | None:
        """Maps a database row to a LeaveRecord object."""
        if not row:
            return None
        return LeaveRecord(
            id=row.get("ID"),
            nhi=row.get("NHI"),
            patient_name=row.get("Name"),
            leave_date=row.get("LeaveDate"),
            leave_time=row.get("LeaveTime"),
            return_time=row.get("ReturnTime"),
            expected_return_time=row.get("ExpectedReturnTime"),
            leave_type=row.get("LeaveType"),
            is_escorted_leave=bool(row.get("Is Escorted", False)),
            staff_responsible_id=row.get("StaffResponsibleID"),
            leave_description=row.get("LeaveDescription"),
            file_name=row.get("FileName"),
        )

    def get_leave_for_person(self, nhi: str) -> list[dict]:
        """Gets all leave records for a specific person by their NHI."""
        conn = get_db_connection()
        if not conn or not nhi:
            return []
        
        records = []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc("sp_GetLeaveForPerson", (nhi,))
            for result in cursor.stored_results():
                records = result.fetchall()
        except Exception as e:
            print(f"Error getting leave for person: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        
        return records

    def get_people_on_leave(self) -> list[dict]:
        """Fetches a list of people currently on leave for the display app."""
        conn = get_db_connection()
        if not conn: return []
        
        on_leave_list = []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc("sp_GetPeopleOnLeave")
            for result in cursor.stored_results():
                on_leave_list = result.fetchall()
        except Exception as e:
            print(f"Database Error in get_people_on_leave: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return on_leave_list

    # leave_record_data.py
# ... (other methods remain the same) ...

    def add_leave(self, new_leave: LeaveRecord) -> bool:
        """Adds a new leave record to the database."""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            # --- REFINED: Arguments now match the final stored procedure ---
            args = (
                new_leave.nhi,
                new_leave.patient_name,
                new_leave.leave_date,
                new_leave.leave_time,
                new_leave.expected_return_time,
                new_leave.leave_type,
                new_leave.is_escorted_leave,
                new_leave.staff_responsible_id,
                new_leave.staff_nurse_id, # MODIFIED: Pass the staff nurse ID
                new_leave.leave_description,
                new_leave.mse,
                new_leave.risk,
                new_leave.leave_conditions_met,
                new_leave.awol_status,
                new_leave.has_ward_contact_info,
                new_leave.senior_nurse_id,
                new_leave.contact_phone_number,
                0,  # Placeholder for the OUT parameter p_new_id
            )
            result_args = cursor.callproc("sp_AddLeave", args)
            conn.commit()
            
            # The new ID is now the 18th element (index 17)
            new_leave.id = result_args[17]

            print(f"Successfully added new leave record for {new_leave.patient_name}")
            return True
        except Exception as e:
            print(f"Error adding leave record: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()



    def log_return(self, record_id: int, return_time: datetime, signed_in_by_id: int) -> bool:
        """Logs the return of a patient from leave."""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            args = (record_id, return_time, signed_in_by_id)
            cursor.callproc("sp_LogReturn", args)
            conn.commit()
            print(f"Successfully logged return for leave record ID: {record_id}")
            return True
        except Exception as e:
            print(f"Error logging return: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()


    def update_leave_filename(self, leave_id: int, filename: str) -> bool:
        """Updates the FileName for a specific leave record."""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            sql = "UPDATE LeaveLog SET FileName = %s WHERE ID = %s"
            cursor.execute(sql, (filename, leave_id))
            conn.commit()
            print(f"Successfully updated FileName for leave ID: {leave_id}")
            return True
        except Exception as e:
            print(f"Error updating leave filename: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # leave_record_data.py
# ... (inside the LeaveRecordData class)

    def get_leave_by_id(self, leave_id: int) -> LeaveRecord | None:
        """Gets a single leave record by its primary ID."""
        conn = get_db_connection()
        if not conn:
            return None
        
        record = None
        try:
            # Using the vw_LoadLeaveForCurrentPeople view to get rich data
            sql = "SELECT * FROM LeaveLog WHERE ID = %s"
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (leave_id,))
            row = cursor.fetchone()
            if row:
                record = self._load_leave_from_row(row)
        except Exception as e:
            print(f"Error in get_leave_by_id: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        
        return record