import unittest
from datetime import date, datetime

# The sys.path hack has been removed as it's no longer needed with the proper package structure.
from person_data import PersonData
from person_model import Person


class TestPersonData(unittest.TestCase):

    def setUp(self):
        """This special method runs before each individual test."""
        print(f"\n--- Setting up for {self._testMethodName} ---")
        self.person_manager = PersonData()

    def test_get_sorted_people(self):
        """Tests that we can retrieve both filtered and full lists of people."""
        print("Testing data retrieval...")
        # Test 1: Get only occupied rooms (default)
        occupied_people = self.person_manager.get_sorted_people(
            include_empty_rooms=False
        )
        self.assertIsNotNone(occupied_people)
        if occupied_people:
            for person in occupied_people:
                self.assertIsNotNone(
                    person.nhi,
                    "Found an empty room when only occupied rooms were expected.",
                )

        # Test 2: Get all rooms
        all_rooms = self.person_manager.get_sorted_people(include_empty_rooms=True)
        # [cite_start]Assuming your facility has 19 rooms as per the project brief [cite: 29]
        self.assertGreaterEqual(
            len(all_rooms), 19, "Expected to find at least 19 rooms."
        )

    def test_update_person_notes(self):
        """Tests that a person's special notes can be updated and reverted."""
        print("Testing person update...")
        # SETUP: Find a person to update
        people = self.person_manager.get_sorted_people()
        person_to_update = next((p for p in people if p.nhi is not None), None)
        self.assertIsNotNone(
            person_to_update, "No occupied person found to run update test."
        )

        original_notes = person_to_update.special_notes
        new_note = f"Automated test update on {datetime.now()}"
        person_to_update.special_notes = new_note

        # ACTION
        success = self.person_manager.update_person(person_to_update)
        self.assertTrue(success, "update_person method returned False.")

        # VERIFICATION
        verifier = PersonData()
        verifier.get_sorted_people()
        verified_person = verifier.get_person_by_id(person_to_update.id)
        self.assertEqual(
            verified_person.special_notes,
            new_note,
            "Database was not updated with the new note.",
        )

        # CLEANUP: Revert the change
        verified_person.special_notes = original_notes
        cleanup_success = self.person_manager.update_person(verified_person)
        self.assertTrue(cleanup_success, "Failed to clean up and revert test data.")

    def test_assign_and_remove_person(self):
        """Tests that a new person can be assigned to an empty room and then removed."""
        print("Testing person assignment and removal...")
        # SETUP: Find an empty room
        all_rooms = self.person_manager.get_sorted_people(include_empty_rooms=True)
        empty_room = next((r for r in all_rooms if r.nhi is None), None)
        self.assertIsNotNone(
            empty_room, "No empty room found to run assign/remove test."
        )

        # ACTION 1: Assign a new person
        new_person = Person(name="Test Assign-Remove", nhi="TAR1234")
        assign_success = self.person_manager.assign_person_to_room(
            new_person, empty_room.room
        )
        self.assertTrue(assign_success, "assign_person_to_room returned False.")

        # VERIFICATION 1: Check they were assigned
        verifier1 = PersonData()
        verifier1.get_sorted_people(include_empty_rooms=True)
        person_in_room = verifier1.get_person_by_room(empty_room.room)
        self.assertIsNotNone(person_in_room)
        self.assertEqual(person_in_room.nhi, "TAR1234")

        # ACTION 2: Remove the person we just added
        remove_success = self.person_manager.remove_person(person_in_room.id)
        self.assertTrue(remove_success, "remove_person returned False.")

        # VERIFICATION 2: Check the room is empty again
        verifier2 = PersonData()
        verifier2.get_sorted_people(include_empty_rooms=True)
        room_after_removal = verifier2.get_person_by_room(empty_room.room)
        self.assertIsNotNone(room_after_removal)
        self.assertIsNone(room_after_removal.nhi, "Room was not empty after removal.")


if __name__ == "__main__":
    unittest.main()
