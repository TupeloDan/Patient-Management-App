# At the top of person_data.py

import random
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from database import get_db_connection
from person_model import Person


class PersonData:
    """Manages all database operations for Person objects."""

    # This dictionary acts as a secure "whitelist" of fields that are allowed to be updated.
    # It maps a simple name (used in the code) to the actual database column name.
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
        # You can add more fields here in the future (e.g., "MDTDay", "SpecialNotes")
    }

    def __init__(self):
        """Initializes the data manager."""
        self._people_cache = {}

    def _load_person_from_row(self, row: dict) -> Person | None:
        """
        Maps a database row from the vw_WhiteboardData view to the complete Person object.
        This is the single source of truth for creating person objects.
        """
        if not row:
            return None

        # This now maps ALL the fields from the definitive database view
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
            # Staff Assignment IDs
            clinician_id=row.get("ClinicianID"),
            case_manager_id=row.get("CaseManagerID"),
            case_manager_2nd_id=row.get("CaseManager2ndID"),
            associate_id=row.get("AssociateID"),
            associate_2nd_id=row.get("Associate2ndID"),
            # Last Completed Dates
            last_treatment_plan=row.get("LastTreatmentPlan"),
            last_honos=row.get("LastHonos"),
            last_uds=row.get("LastUDS"),
            no_uds=bool(row.get("NoUDS", False)),
            # Joined User-Friendly Names
            legal=row.get("Legal"),
            clinician_name=row.get("ClinicianName"),
            case_managers=row.get("CaseManagers"),
            associates=row.get("Associates"),
        )

    # In person_data.py, replace the get_sorted_people method

    def get_sorted_people(self, include_empty_rooms: bool = False) -> list[Person]:
        """
        Fetches all people from the database by calling the sp_GetSortedPeople stored procedure.
        """
        conn = get_db_connection()
        if not conn:
            return []

        results_list = []
        self._people_cache.clear()

        try:
            cursor = conn.cursor(dictionary=True)

            # --- CHANGED: Call the stored procedure by name ---
            cursor.callproc("sp_GetSortedPeople")

            # When using callproc, results must be retrieved from an iterator
            for result in cursor.stored_results():
                all_rows = result.fetchall()

            # The rest of the logic remains the same
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
        """
        Retrieves a single person from the database by their ID.
        This is a more robust method that doesn't rely on the cache.
        """
        # First, check the cache for speed
        if person_id in self._people_cache:
            return self._people_cache.get(person_id)

        # If not in cache, fetch directly from the database
        conn = get_db_connection()
        if not conn:
            return None

        person = None
        try:
            # Use our main view to get all the rich data for the person
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM vw_WhiteboardData WHERE ID = %s", (person_id,))
            row = cursor.fetchone()
            if row:
                person = self._load_person_from_row(row)
                # Store it in the cache for next time
                self._people_cache[person_id] = person
        except Exception as e:
            print(f"An error occurred in get_person_by_id: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        
        return person

    def get_person_by_room(self, room_name: str) -> Person | None:
        """Finds a room's basic details (ID, NHI) from the base People table."""
        conn = get_db_connection()
        if not conn:
            return None

        query = "SELECT ID, Room, NHI FROM People WHERE Room = %s"
        person_stub = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (room_name,))
            row = cursor.fetchone()
            if row:
                person_stub = Person(
                    id=row.get("ID"), room=row.get("Room"), nhi=row.get("NHI")
                )
        except Exception as e:
            print(f"An error occurred in get_person_by_room: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return person_stub

    # In person_data.py, replace the update_person method

    def update_person(self, person: Person) -> bool:
        """
        Updates an existing person's record by calling the sp_UpdatePerson stored procedure.
        """
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            # Create a tuple of arguments in the exact order the procedure expects them
            args = (
                person.id,
                person.nhi,
                person.name,
                person.legal_id,
                person.is_special_patient,
                person.has_vnr,
                person.special_notes,
            )

            # Call the stored procedure
            cursor.callproc("sp_UpdatePerson", args)

            # Important: You must commit any changes made by a stored procedure
            conn.commit()

            # Update the in-memory cache
            self._people_cache[person.id] = person
            print(f"Successfully updated person: {person.name}")
            return True

        except Exception as e:
            print(f"Error updating person: {e}")
            # No need for rollback() here as commit() won't be reached on error
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # In person_data.py, replace the move_person method

    def move_person(self, person_to_move: Person, destination_room_name: str) -> bool:
        """
        Moves a person to a new room by calling the sp_MovePerson stored procedure.
        Returns True on success, False on failure.
        """
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            # Prepare the arguments tuple in the exact order the procedure expects.
            # The last argument (0) is a placeholder for the OUT parameter.
            args = (
                person_to_move.id,
                person_to_move.nhi,
                person_to_move.name,
                person_to_move.legal_id,
                person_to_move.has_vnr,
                person_to_move.treatment_plans_due,
                person_to_move.honos_due,
                person_to_move.uds_due,
                person_to_move.rel_security,
                person_to_move.profile,
                person_to_move.metobolic,
                person_to_move.bloods,
                person_to_move.flight_risk,
                person_to_move.uds_frequency,
                person_to_move.mdt_day,
                person_to_move.clinician_id,
                person_to_move.case_manager_id,
                person_to_move.case_manager_2nd_id,
                person_to_move.associate_id,
                person_to_move.associate_2nd_id,
                person_to_move.progress_percent,
                person_to_move.special_notes,
                person_to_move.is_special_patient,
                destination_room_name,
                0,  # Placeholder for the p_new_id OUT parameter
            )

            # Call the stored procedure and get the results
            result_args = cursor.callproc("sp_MovePerson", args)
            new_id = result_args[
                24
            ]  # The new ID is the 25th element in the returned tuple

            conn.commit()
            print(
                f"Successfully moved {person_to_move.name} to {destination_room_name}."
            )

            # Update the in-memory cache
            self._people_cache[person_to_move.id].nhi = None  # Mark old room as empty
            person_to_move.id = new_id
            person_to_move.room = destination_room_name
            self._people_cache[new_id] = person_to_move

            return True

        except Exception as e:
            print(f"Error moving person: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # In person_data.py, add this inside the PersonData class

    # In person_data.py, replace the assign_person_to_room method

    def assign_person_to_room(
        self, new_person_details: Person, destination_room_name: str
    ) -> bool:
        """
        Assigns a new person to a specified empty room by calling the sp_AssignPersonToRoom stored procedure.
        """
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            # Prepare arguments in the exact order the procedure expects.
            # The last argument (0) is a placeholder for the OUT parameter.
            args = (
                new_person_details.nhi,
                new_person_details.name,
                new_person_details.legal_id,
                new_person_details.has_vnr,
                new_person_details.is_special_patient,
                new_person_details.special_notes,
                destination_room_name,
                0,  # Placeholder for p_record_id OUT parameter
            )

            # Call the stored procedure and get the results
            result_args = cursor.callproc("sp_AssignPersonToRoom", args)
            new_id = result_args[
                7
            ]  # The new ID is the 8th element in the returned tuple

            conn.commit()
            print(
                f"Successfully assigned {new_person_details.name} to room {destination_room_name}."
            )

            # Update the in-memory cache
            new_person_details.id = new_id
            new_person_details.room = destination_room_name
            self._people_cache[new_id] = new_person_details

            return True

        except Exception as e:
            print(f"Error assigning person: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # In person_data.py, add this inside the PersonData class

    # In person_data.py, replace the remove_person method

    def remove_person(self, person_id: int) -> bool:
        """
        Clears a person's data from a room by calling the sp_RemovePerson stored procedure.
        """
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            # The stored procedure only needs one argument: the person's record ID.
            args = (person_id,)
            cursor.callproc("sp_RemovePerson", args)

            conn.commit()
            print(f"Successfully removed person from record ID: {person_id}")

            # Update the in-memory cache
            if person_id in self._people_cache:
                self._people_cache[person_id].nhi = None
                self._people_cache[person_id].name = None

            return True

        except Exception as e:
            print(f"Error removing person: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # In person_data.py, inside the PersonData class

    # In person_data.py, replace the update_staff_assignments method

    def update_staff_assignments(
        self,
        person_id: int,
        clinician_id: int,
        cm_id: int,
        cm_2nd_id: int,
        assoc_id: int,
        assoc_2nd_id: int,
    ) -> bool:
        """
        Updates staff assignments for a person by calling the sp_UpdateStaffAssignments stored procedure.
        """
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            # Prepare the tuple of arguments in the exact order the procedure expects
            args = (person_id, clinician_id, cm_id, cm_2nd_id, assoc_id, assoc_2nd_id)

            # Call the stored procedure
            cursor.callproc("sp_UpdateStaffAssignments", args)

            # Commit the changes made by the procedure
            conn.commit()
            print(f"Successfully updated staff assignments for person ID: {person_id}")

            # Update the in-memory cache
            if person_id in self._people_cache:
                person = self._people_cache[person_id]
                person.clinician_id = clinician_id
                person.case_manager_id = cm_id
                person.case_manager_2nd_id = cm_2nd_id
                person.associate_id = assoc_id
                person.associate_2nd_id = assoc_2nd_id

            return True

        except Exception as e:
            print(f"Error updating staff assignments: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # In person_data.py, inside the PersonData class

    def update_field(self, person_id: int, field_name: str, new_value) -> bool:
        """
        Updates a single field for a person in the database.

        Args:
            person_id: The ID of the person to update.
            field_name: The simple name of the field from the VALID_UPDATE_FIELDS whitelist.
            new_value: The new value to set for the field.

        Returns:
            True on success, False on failure.
        """
        # --- Security Check: Ensure the field is in our whitelist ---
        if field_name not in self.VALID_UPDATE_FIELDS:
            print(f"Error: '{field_name}' is not a valid field for updating.")
            return False

        db_column_name = self.VALID_UPDATE_FIELDS[field_name]

        # Use backticks (`) around the column name to handle special characters
        sql = f"UPDATE People SET `{db_column_name}` = %s WHERE ID = %s"
        values = (new_value, person_id)

        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            conn.start_transaction()
            cursor.execute(sql, values)

            if cursor.rowcount == 0:
                raise Exception(
                    f"Update failed because no record with ID {person_id} was found."
                )

            conn.commit()
            print(f"Successfully updated '{db_column_name}' for person ID: {person_id}")

            # Update the in-memory cache dynamically using setattr
            if person_id in self._people_cache:
                person = self._people_cache[person_id]
                # setattr allows us to set an attribute on an object using a string name
                setattr(person, field_name, new_value)

            return True

        except Exception as e:
            print(f"Error updating field '{db_column_name}': {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # In person_data.py, inside the PersonData class

    def update_plan_due_date(self, person_id: int, completed_date: date) -> bool:
        """Calculates a new Plan Due date (3 months) and updates the database."""
        try:
            new_due_date = completed_date + relativedelta(months=3)
            sql = "UPDATE People SET TreatmentPlans = %s, LastTreatmentPlan = %s WHERE ID = %s"
            
            # THE FIX: Convert date objects to YYYY-MM-DD strings before sending to the DB
            values = (new_due_date.strftime('%Y-%m-%d'), completed_date.strftime('%Y-%m-%d'), person_id)

            self._execute_transactional_update(sql, values)

            if person_id in self._people_cache:
                self._people_cache[person_id].treatment_plans_due = new_due_date
                self._people_cache[person_id].last_treatment_plan = completed_date

            print(f"Successfully updated Plan Due Date for person ID: {person_id}")
            return True
        except Exception as e:
            print(f"Error updating Plan Due Date: {e}")
            return False

    def update_honos_due_date(self, person_id: int, completed_date: date) -> bool:
        """Calculates a new HoNos Due date (3 months) and updates the database."""
        try:
            new_due_date = completed_date + relativedelta(months=3)
            sql = "UPDATE People SET HoNos = %s, LastHonos = %s WHERE ID = %s"

            # THE FIX: Convert date objects to YYYY-MM-DD strings
            values = (new_due_date.strftime('%Y-%m-%d'), completed_date.strftime('%Y-%m-%d'), person_id)

            self._execute_transactional_update(sql, values)

            if person_id in self._people_cache:
                self._people_cache[person_id].honos_due = new_due_date
                self._people_cache[person_id].last_honos = completed_date

            print(f"Successfully updated HoNos Due Date for person ID: {person_id}")
            return True
        except Exception as e:
            print(f"Error updating HoNos Due Date: {e}")
            return False

    def update_uds_due_date(self, person_id: int, last_test_date: date) -> bool:
        """Calculates a new UDS Due date based on frequency and updates the database."""
        person = self.get_person_by_id(person_id)
        if not person:
            print(f"Error: Could not find person with ID {person_id} in cache.")
            return False

        try:
            frequency = (person.uds_frequency.upper() if person.uds_frequency else "WEEKLY")
            if frequency == "BI-WEEKLY":
                new_due_date = last_test_date + timedelta(days=14)
            elif frequency == "WEEKLY":
                new_due_date = last_test_date + timedelta(weeks=1)
            elif frequency == "MONTHLY":
                new_due_date = last_test_date + relativedelta(months=1)
            elif frequency == "RANDOM":
                new_due_date = date.today() + timedelta(days=random.randint(7, 28))
            elif frequency == "ONREQUEST":
                new_due_date = date.today()
            else:
                new_due_date = last_test_date

            sql = "UPDATE People SET UDSDue = %s, LastUDS = %s WHERE ID = %s"

            # THE FIX: Convert date objects to YYYY-MM-DD strings
            values = (new_due_date.strftime('%Y-%m-%d'), last_test_date.strftime('%Y-%m-%d'), person_id)

            self._execute_transactional_update(sql, values)

            if person_id in self._people_cache:
                self._people_cache[person_id].uds_due = new_due_date
                self._people_cache[person_id].last_uds = last_test_date

            print(f"Successfully updated UDS Due Date for person ID: {person_id}")
            return True
        except Exception as e:
            print(f"Error updating UDS Due Date: {e}")
            return False
        
        # ... (inside the PersonData class)

    def get_person_by_nhi(self, nhi: str) -> Person | None:
        """
        Retrieves a single person from the database by their NHI number.
        """
        conn = get_db_connection()
        if not conn:
            return None

        person = None
        try:
            # Use our main view to get all the rich data for the person
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

# ... (rest of the class)

    def _execute_transactional_update(self, sql: str, values: tuple):
        """A private helper to run any transactional update."""
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to the database.")
        try:
            cursor = conn.cursor()
            conn.start_transaction()

            # Step 1: Verify the record exists BEFORE trying to update it.
            # The person's ID is always the last parameter in our 'values' tuple.
            person_id_to_check = values[-1]
            cursor.execute("SELECT ID FROM People WHERE ID = %s", (person_id_to_check,))
            
            # If fetchone() returns None, the record truly doesn't exist.
            if cursor.fetchone() is None:
                raise Exception(f"Update failed because no record was found for ID: {person_id_to_check}")

            # Step 2: Now that we know the record exists, perform the update.
            # We no longer need to check cursor.rowcount here, because 0 is a valid result.
            cursor.execute(sql, values)
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e  # Re-raise the exception to be caught by the calling function
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()