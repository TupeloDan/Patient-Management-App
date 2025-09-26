# staff_data.py
from database import get_db_connection

class StaffData:
    """Manages all database operations for Staff objects."""

    def get_all_staff(self, roles: list = None) -> list[dict]:
        """
        Fetches a list of all staff members, with optional filtering by role.
        """
        conn = get_db_connection()
        if not conn:
            return []
        
        staff_list = []
        try:
            # Base SQL query
            sql = """
                SELECT s.ID, s.StaffName, r.Role
                FROM Staff AS s
                LEFT JOIN Roles AS r ON s.RoleID = r.ID
            """
            params = []

            # Dynamically add a WHERE clause if roles are provided
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