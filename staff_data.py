# staff_data.py
from database import get_db_connection

class StaffData:
    """Manages all database operations for Staff objects."""

    def get_all_staff(self, roles: list = None) -> list[dict]:
        """Fetches a list of all staff members, with optional filtering by role."""
        conn = get_db_connection()
        if not conn:
            return []
        
        staff_list = []
        try:
            sql = "SELECT s.ID, s.StaffName, r.Role, s.RoleID FROM Staff AS s LEFT JOIN Roles AS r ON s.RoleID = r.ID"
            params = []
            if roles:
                placeholders = ', '.join(['%s'] * len(roles))
                sql += f" WHERE r.Role IN ({placeholders})"
                params.extend(roles)
            sql += " ORDER BY s.StaffName"
            
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params)
            staff_list = cursor.fetchall()
        except Exception as e:
            print(f"Database error in get_all_staff: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return staff_list
    
    def get_delegated_staff(self) -> list[dict]:
        """Fetches a list of staff members who are marked as delegated."""
        conn = get_db_connection()
        if not conn:
            return []
        
        delegated_list = []
        try:
            sql = "SELECT s.ID, s.StaffName, r.Role FROM DelegatedStaff ds JOIN Staff s ON ds.StaffID = s.ID JOIN Roles r ON s.RoleID = r.ID ORDER BY s.StaffName;"
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            delegated_list = cursor.fetchall()
        except Exception as e:
            print(f"Database error in get_delegated_staff: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return delegated_list

    def add_staff(self, name: str, role_id: int) -> bool:
        """Adds a new staff member to the database."""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Staff (StaffName, RoleID) VALUES (%s, %s)"
            cursor.execute(sql, (name, role_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Database error in add_staff: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def update_staff(self, staff_id: int, name: str, role_id: int) -> bool:
        """Updates an existing staff member's details."""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            sql = "UPDATE Staff SET StaffName = %s, RoleID = %s WHERE ID = %s"
            cursor.execute(sql, (name, role_id, staff_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Database error in update_staff: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def update_delegated_staff(self, staff_ids: list[int]) -> bool:
        """Overwrites the DelegatedStaff table with a new list of staff IDs."""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE DelegatedStaff")
            if staff_ids:
                sql = "INSERT INTO DelegatedStaff (StaffID) VALUES (%s)"
                data_to_insert = [(staff_id,) for staff_id in staff_ids]
                cursor.executemany(sql, data_to_insert)
            conn.commit()
            print("Delegated staff list updated successfully.")
            return True
        except Exception as e:
            print(f"Database error in update_delegated_staff: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()