import unittest
from datetime import datetime, date
from leave_record_data import LeaveRecordData
from leave_record_model import LeaveRecord
from person_data import PersonData

class TestLeaveRecordData(unittest.TestCase):

    def setUp(self):
        """This runs before each test."""
        self.leave_manager = LeaveRecordData()
        self.person_manager = PersonData()

    def test_get_leave_for_current_people(self):
        """Tests that we can retrieve leave records for current patients."""
        print("Testing leave data retrieval...")
        leave_records = self.leave_manager.get_leave_for_current_people()
        self.assertIsNotNone(leave_records)

    def test_add_and_log_return(self):
        """Tests that a new leave record can be added and a return logged."""
        print("Testing leave creation and return logging...")
        # SETUP: Find a person to create a leave record for
        people = self.person_manager.get_sorted_people()
        person_on_leave = next((p for p in people if p.nhi is not None), None)
        self.assertIsNotNone(person_on_leave, "No person found to create leave for.")

        # ACTION 1: Add a new leave record
        new_leave = LeaveRecord(
            nhi=person_on_leave.nhi,
            patient_name=person_on_leave.name,
            leave_date=date.today(),
            leave_time=datetime.now(),
            expected_return_time=datetime.now(),
            leave_type="Escorted",
            is_escorted_leave=True,
            staff_responsible_id=1,
            leave_description="Test leave"
        )
        add_success = self.leave_manager.add_leave(new_leave)
        self.assertTrue(add_success, "add_leave returned False.")
        self.assertNotEqual(new_leave.id, 0, "Leave ID was not updated after adding.")

        # ACTION 2: Log the return
        return_time = datetime.now()
        signed_in_by_id = 2 
        log_return_success = self.leave_manager.log_return(new_leave.id, return_time, signed_in_by_id)
        self.assertTrue(log_return_success, "log_return returned False.")


if __name__ == "__main__":
    unittest.main()