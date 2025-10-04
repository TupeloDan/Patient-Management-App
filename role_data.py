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
    def add_role(self, role_name: str, description: str) -> bool:
        """Adds a new role to the database."""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Roles (Role, Description) VALUES (%s, %s)"
            cursor.execute(sql, (role_name, description))
            conn.commit()
            return True
        except Exception as e:
            print(f"Database error in add_role: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                conn.close()

    def update_role(self, role_id: int, role_name: str, description: str) -> bool:
        """Updates an existing role in the database."""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            sql = "UPDATE Roles SET Role = %s, Description = %s WHERE ID = %s"
            cursor.execute(sql, (role_name, description, role_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Database error in update_role: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                conn.close()