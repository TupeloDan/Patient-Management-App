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
        # You can add more fields here in the future (e.g., "MDTDay", "SpecialNotes")
    }

    def __init__(self):
        """Initializes the data manager."""
        self._people_cache = {}

    def _load_person_from_row(self, row: dict) -> Person | None:
        """Maps a database row (from the People table/view) to a Person object."""
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
        )

    def get_sorted_people(self, include_empty_rooms: bool = False) -> list[Person]:
        """
        Fetches people from the database, sorted by room.
        By default, it returns only occupied rooms.
        """
        conn = get_db_connection()
        if not conn:
            return []

        query = "SELECT * FROM vw_GetSortedPeople"
        results_list = []
        self._people_cache.clear()

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            all_rows = cursor.fetchall()

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
        """Retrieves a single person from the in-memory cache by their ID."""
        return self._people_cache.get(person_id)

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

    def update_person(self, person: Person) -> bool:
        """Updates an existing person's core details in the database."""
        sql = """UPDATE People SET
                     NHI = %s, PersonName = %s, LegalStatusID = %s,
                     IsSpecialPatient = %s, HasVNR = %s, SpecialNotes = %s
                 WHERE ID = %s"""
        values = (
            person.nhi,
            person.name,
            person.legal_id,
            person.is_special_patient,
            person.has_vnr,
            person.special_notes,
            person.id,
        )
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            conn.start_transaction()
            check_sql = "SELECT ID FROM People WHERE NHI = %s AND ID <> %s"
            cursor.execute(check_sql, (person.nhi, person.id))
            if cursor.fetchone():
                raise ValueError(
                    f"NHI '{person.nhi}' is already in use by another person."
                )
            cursor.execute(sql, values)
            conn.commit()
            self._people_cache[person.id] = person
            print(f"Successfully updated person: {person.name}")
            return True
        except Exception as e:
            print(f"Error updating person: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def move_person(self, person_to_move: Person, destination_room_name: str) -> bool:
        """Moves a person from their current room to a new room in a single transaction."""
        if person_to_move.room == destination_room_name:
            print("Error: Source and destination rooms are the same.")
            return False

        destination_room = self.get_person_by_room(destination_room_name)
        if not destination_room:
            print(f"Error: Destination room '{destination_room_name}' not found.")
            return False

        if destination_room.nhi is not None:
            print(
                f"Error: Destination room '{destination_room_name}' is already occupied."
            )
            return False

        sql_clear_old_room = """UPDATE People SET
            NHI=NULL, PersonName=NULL, LegalStatusID=NULL, HasVNR=NULL, TreatmentPlans=NULL, 
            HoNos=NULL, UDSDue=NULL, RelSecurity=NULL, Profile=NULL, Metobolic=NULL, 
            Bloods=NULL, FlightRisk=NULL, UDSFrequency=NULL, MDTDay=NULL, LeaveReturn=NULL, 
            ClinicianID=NULL, CaseManagerID=NULL, CaseManager2ndID=NULL, AssociateID=NULL, 
            Associate2ndID=NULL, `Progress%`=NULL, SpecialNotes=NULL, IsSpecialPatient=NULL
            WHERE ID = %s"""

        sql_populate_new_room = """UPDATE People SET
            NHI=%s, PersonName=%s, LegalStatusID=%s, HasVNR=%s, TreatmentPlans=%s, 
            HoNos=%s, UDSDue=%s, RelSecurity=%s, Profile=%s, Metobolic=%s, 
            Bloods=%s, FlightRisk=%s, UDSFrequency=%s, MDTDay=%s, 
            ClinicianID=%s, CaseManagerID=%s, CaseManager2ndID=%s, AssociateID=%s, 
            Associate2ndID=%s, `Progress%`=%s, SpecialNotes=%s, IsSpecialPatient=%s
            WHERE ID = %s"""

        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            conn.start_transaction()
            cursor.execute(sql_clear_old_room, (person_to_move.id,))

            values_to_populate = (
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
                destination_room.id,
            )
            cursor.execute(sql_populate_new_room, values_to_populate)

            conn.commit()
            print(
                f"Successfully moved {person_to_move.name} from room {person_to_move.room} to {destination_room_name}."
            )

            self._people_cache[person_to_move.id].nhi = (
                None  # Mark old room in cache as empty
            )
            person_to_move.id = destination_room.id
            person_to_move.room = destination_room_name
            self._people_cache[destination_room.id] = (
                person_to_move  # Update cache with new info
            )
            return True

        except Exception as e:
            print(f"Error moving person: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # In person_data.py, add this inside the PersonData class

    def assign_person_to_room(
        self, new_person_details: Person, destination_room_name: str
    ) -> bool:
        """
        Assigns a new person to a specified empty room.

        Args:
            new_person_details: A Person object containing the new person's info (name, NHI, etc.).
            destination_room_name: The name of the empty room to assign them to.

        Returns:
            True on success, False on failure.
        """
        # --- 1. Validation Checks ---
        if not new_person_details or not new_person_details.nhi:
            print("Error: New person details are incomplete.")
            return False

        destination_room = self.get_person_by_room(destination_room_name)
        if not destination_room:
            print(f"Error: Destination room '{destination_room_name}' not found.")
            return False

        if destination_room.nhi is not None:
            print(
                f"Error: Destination room '{destination_room_name}' is already occupied."
            )
            return False

        # --- 2. Define SQL Query ---
        # This query updates the empty room's record with the new person's data
        sql = """UPDATE People SET
                     NHI=%s, PersonName=%s, LegalStatusID=%s, HasVNR=%s, IsSpecialPatient=%s,
                     TreatmentPlans=%s, HoNos=%s, UDSDue=%s, `Progress%`=%s, SpecialNotes=%s
                 WHERE ID = %s"""

        # --- 3. Execute the Transaction ---
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            conn.start_transaction()

            # Check for duplicate NHI across all other records
            check_sql = "SELECT ID FROM People WHERE NHI = %s"
            cursor.execute(check_sql, (new_person_details.nhi,))
            if cursor.fetchone():
                raise ValueError(
                    f"NHI '{new_person_details.nhi}' is already in use by another person."
                )

            today = datetime.now().date()
            values_to_update = (
                new_person_details.nhi,
                new_person_details.name,
                new_person_details.legal_id,
                new_person_details.has_vnr,
                new_person_details.is_special_patient,
                today,
                today,
                today,  # Set default due dates to today
                0.0,  # Default progress
                new_person_details.special_notes,
                destination_room.id,  # The ID of the empty room's record
            )
            cursor.execute(sql, values_to_update)

            conn.commit()
            print(
                f"Successfully assigned {new_person_details.name} to room {destination_room_name}."
            )

            # --- 4. Update In-Memory Cache ---
            # Update the passed-in object with its new database ID and room
            new_person_details.id = destination_room.id
            new_person_details.room = destination_room_name
            # Add the now-complete person object to the cache
            self._people_cache[destination_room.id] = new_person_details

            return True

        except Exception as e:
            print(f"Error assigning person: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # In person_data.py, add this inside the PersonData class

    def remove_person(self, person_id: int) -> bool:
        """
        Clears a person's data from a room record, effectively "removing" them.
        This is a transactional update, not a DELETE.

        Args:
            person_id: The ID of the record (room) to clear.

        Returns:
            True on success, False on failure.
        """
        # This SQL is identical to the one used in the move_person method
        sql_clear_room = """UPDATE People SET
            NHI=NULL, PersonName=NULL, LegalStatusID=NULL, HasVNR=NULL, TreatmentPlans=NULL, 
            HoNos=NULL, UDSDue=NULL, RelSecurity=NULL, Profile=NULL, Metobolic=NULL, 
            Bloods=NULL, FlightRisk=NULL, UDSFrequency=NULL, MDTDay=NULL, LeaveReturn=NULL, 
            ClinicianID=NULL, CaseManagerID=NULL, CaseManager2ndID=NULL, AssociateID=NULL, 
            Associate2ndID=NULL, `Progress%`=NULL, SpecialNotes=NULL, IsSpecialPatient=NULL
            WHERE ID = %s"""

        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            conn.start_transaction()

            cursor.execute(sql_clear_room, (person_id,))

            conn.commit()
            print(f"Successfully removed person from record ID: {person_id}")

            # Update the in-memory cache
            if person_id in self._people_cache:
                # Instead of deleting, we update the cached object to be "empty"
                self._people_cache[person_id].nhi = None
                self._people_cache[person_id].name = None
                # ... etc for other fields if necessary

            return True

        except Exception as e:
            print(f"Error removing person: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # In person_data.py, inside the PersonData class

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
        Updates all staff assignments for a single person record in the database.
        Returns True on success, False on failure.
        """
        # --- RESTORED: These variable definitions were missing ---
        sql = """UPDATE People SET
                     ClinicianID = %s,
                     CaseManagerID = %s,
                     CaseManager2ndID = %s,
                     AssociateID = %s,
                     Associate2ndID = %s
                 WHERE ID = %s"""

        values = (clinician_id, cm_id, cm_2nd_id, assoc_id, assoc_2nd_id, person_id)
        # --- END RESTORED SECTION ---

        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            conn.start_transaction()
            print(f"DEBUG: Executing UPDATE with values: {values}")
            cursor.execute(sql, values)

            if cursor.rowcount == 0:
                raise Exception(
                    f"Update failed because no record with ID {person_id} was found."
                )

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
            conn.rollback()
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
            values = (new_due_date, completed_date, person_id)

            # Update the database
            self._execute_transactional_update(sql, values)

            # Update the cache
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
            values = (new_due_date, completed_date, person_id)

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
            # Replicate the logic from your VBA Select Case
            frequency = (
                person.uds_frequency.upper() if person.uds_frequency else "WEEKLY"
            )
            if frequency == "BI-WEEKLY":
                new_due_date = last_test_date + timedelta(days=14)
            elif frequency == "WEEKLY":
                new_due_date = last_test_date + timedelta(weeks=1)
            elif frequency == "MONTHLY":
                new_due_date = last_test_date + relativedelta(months=1)
            elif frequency == "RANDOM":
                new_due_date = date.today() + timedelta(days=random.randint(7, 28))
            else:  # ONREQUEST or other
                new_due_date = last_test_date

            sql = "UPDATE People SET UDSDue = %s, LastUDS = %s WHERE ID = %s"
            values = (new_due_date, last_test_date, person_id)

            self._execute_transactional_update(sql, values)

            if person_id in self._people_cache:
                self._people_cache[person_id].uds_due = new_due_date
                self._people_cache[person_id].last_uds = last_test_date

            print(f"Successfully updated UDS Due Date for person ID: {person_id}")
            return True
        except Exception as e:
            print(f"Error updating UDS Due Date: {e}")
            return False

    def _execute_transactional_update(self, sql: str, values: tuple):
        """A private helper to run any transactional update."""
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to the database.")
        try:
            cursor = conn.cursor()
            conn.start_transaction()
            cursor.execute(sql, values)
            if cursor.rowcount == 0:
                raise Exception(
                    f"Update failed because no record was found for the given ID."
                )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e  # Re-raise the exception to be caught by the calling function
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()


# --- This block allows you to run the class as a command-line tool ---
if __name__ == "__main__":
    import sys

    # Check if the user provided the correct number of arguments
    if len(sys.argv) != 4:
        print("Usage: python person_data.py <person_id> <field_name> <new_value>")
        print("Example: python person_data.py 1 rel_security True")
        sys.exit(1)  # Exit the script if arguments are wrong

    # --- Parse the arguments from the command line ---
    try:
        person_id_arg = int(sys.argv[1])
        field_name_arg = sys.argv[2]
        # Convert the string 'True' or 'False' to a boolean
        new_value_arg = sys.argv[3].lower() in ("true", "1", "t")
    except ValueError:
        print("Error: person_id must be a number.")
        sys.exit(1)

    # --- Create an instance of the data manager and call the method ---
    print(
        f"Attempting to update field '{field_name_arg}' for person ID {person_id_arg} to '{new_value_arg}'..."
    )

    person_data_manager = PersonData()

    # We need to load the cache so the in-memory update works correctly
    person_data_manager.get_sorted_people(include_empty_rooms=True)

    success = person_data_manager.update_field(
        person_id=person_id_arg, field_name=field_name_arg, new_value=new_value_arg
    )

    if success:
        print("✅ Update completed successfully.")
    else:
        print("❌ Update failed. Check the error message above.")
