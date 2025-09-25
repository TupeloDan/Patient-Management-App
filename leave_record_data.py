# leave_record_data.py
from datetime import datetime, date
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
        # This mapping is simplified for clarity; you can expand it to match all fields
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

    def get_leave_for_current_people(self) -> list[LeaveRecord]:
        """Fetches all leave records for currently admitted people."""
        conn = get_db_connection()
        if not conn:
            return []
        results_list = []
        self._leave_cache.clear()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc("sp_GetLeaveForCurrentPeople")
            for result in cursor.stored_results():
                rows = result.fetchall()
            for row in rows:
                leave = self._load_leave_from_row(row)
                if leave:
                    self._leave_cache[leave.id] = leave
                    results_list.append(leave)
        except Exception as e:
            print(f"An error occurred while fetching leave records: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return results_list

    def add_leave(self, new_leave: LeaveRecord) -> bool:
        """Adds a new leave record to the database."""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            args = (
                new_leave.nhi,
                new_leave.patient_name,
                new_leave.leave_date,
                new_leave.leave_time,
                new_leave.expected_return_time,
                new_leave.leave_type,
                new_leave.is_escorted_leave,
                new_leave.staff_responsible_id,
                new_leave.leave_description,
                0,
            )
            result_args = cursor.callproc("sp_AddLeave", args)
            new_id = result_args[9]
            conn.commit()
            new_leave.id = new_id
            self._leave_cache[new_id] = new_leave
            print(f"Successfully added new leave record for {new_leave.patient_name}")
            return True
        except Exception as e:
            print(f"Error adding leave record: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def log_return(
        self, record_id: int, return_time: datetime, signed_in_by_id: int
    ) -> bool:
        """Logs the return of a patient from leave."""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            args = (record_id, return_time, signed_in_by_id)
            cursor.callproc("sp_LogReturn", args)
            conn.commit()
            if record_id in self._leave_cache:
                self._leave_cache[record_id].return_time = return_time
                self._leave_cache[record_id].leave_signed_in_by_id = signed_in_by_id
            print(f"Successfully logged return for leave record ID: {record_id}")
            return True
        except Exception as e:
            print(f"Error logging return: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # --- NEW METHODS ---

    def is_person_on_leave(self, nhi: str) -> bool:
        """Checks if a person is currently on an un-returned leave."""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            args = (nhi, 0)  # 0 is a placeholder for the OUT param
            result_args = cursor.callproc("sp_IsPersonOnLeave", args)
            return bool(result_args[1])
        except Exception as e:
            print(f"Error checking if person is on leave: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def get_leave_by_date_range(
        self, start_date: date, end_date: date, nhi: str = None
    ) -> list[LeaveRecord]:
        """Gets leave records for a date range, optionally for a specific person."""
        conn = get_db_connection()
        if not conn:
            return []
        results_list = []
        try:
            cursor = conn.cursor(dictionary=True)
            args = (start_date, end_date, nhi)
            cursor.callproc("sp_GetLeaveByDateRange", args)
            for result in cursor.stored_results():
                rows = result.fetchall()
            for row in rows:
                leave = self._load_leave_from_row(row)
                if leave:
                    results_list.append(leave)
        except Exception as e:
            print(f"Error getting leave by date range: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return results_list

    def get_leave_for_person(self, nhi: str) -> list[LeaveRecord]:
        """Gets all leave records for a specific person."""
        conn = get_db_connection()
        if not conn:
            return []
        results_list = []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc("sp_GetLeaveForPerson", (nhi,))
            for result in cursor.stored_results():
                rows = result.fetchall()
            for row in rows:
                leave = self._load_leave_from_row(row)
                if leave:
                    results_list.append(leave)
        except Exception as e:
            print(f"Error getting leave for person: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return results_list

    def update_file_name(self, record_id: int, file_name: str) -> bool:
        """Updates the filename for a specific leave record."""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            args = (record_id, file_name)
            cursor.callproc("sp_UpdateLeaveFileName", args)
            conn.commit()
            if record_id in self._leave_cache:
                self._leave_cache[record_id].file_name = file_name
            print(f"Successfully updated FileName for leave record ID: {record_id}")
            return True
        except Exception as e:
            print(f"Error updating file name: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # Add this method inside the LeaveRecordData class
    def get_people_on_leave(self) -> list[dict]:
        """Fetches a list of people currently on leave with relevant details."""
        conn = get_db_connection()
        if not conn:
            return []

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
