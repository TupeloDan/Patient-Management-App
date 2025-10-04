# role_data.py
from database import get_db_connection

class RoleData:
    """Manages all database operations for the Roles table."""

    def get_all_roles(self) -> list[dict]:
        """Fetches all roles from the database."""
        conn = get_db_connection()
        if not conn: return []
        
        roles = []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT ID, Role, Description FROM Roles ORDER BY Role")
            roles = cursor.fetchall()
        except Exception as e:
            print(f"Database error in get_all_roles: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return roles