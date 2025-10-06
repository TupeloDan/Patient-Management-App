# notice_data.py
from database import get_db_connection
from datetime import date

class NoticeData:
    """Manages database operations for Notices."""
    def get_active_notices(self) -> list[str]:
        conn = get_db_connection()
        if not conn: return []
        notices = []
        try:
            cursor = conn.cursor()
            # This is the fix: Use a direct SQL query to get unexpired notices.
            sql = "SELECT NoticeText FROM Notices WHERE ExpiryDate >= %s ORDER BY ExpiryDate DESC"
            cursor.execute(sql, (date.today(),))
            notices = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Database error in get_active_notices: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return notices

    def add_notice(self, notice_text: str, expiry_date: date) -> bool:
        """Adds a new notice to the database."""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Notices (NoticeText, ExpiryDate) VALUES (%s, %s)"
            cursor.execute(sql, (notice_text, expiry_date))
            conn.commit()
            print(f"Successfully added notice: '{notice_text}'")
            return True
        except Exception as e:
            print(f"Database error in add_notice: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def get_all_notices(self) -> list[dict]:
        """Fetches all notices, including expired ones."""
        conn = get_db_connection()
        if not conn: return []
        notices = []
        try:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT NoticeID, NoticeText, ExpiryDate FROM Notices ORDER BY ExpiryDate DESC"
            cursor.execute(sql)
            notices = cursor.fetchall()
        except Exception as e:
            print(f"Database error in get_all_notices: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return notices

    def update_notice(self, notice_id: int, notice_text: str, expiry_date: date) -> bool:
        """Updates an existing notice in the database."""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            sql = "UPDATE Notices SET NoticeText = %s, ExpiryDate = %s WHERE NoticeID = %s"
            cursor.execute(sql, (notice_text, expiry_date, notice_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Database error in update_notice: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                conn.close()
                conn.close()

    def delete_notice(self, notice_id: int) -> bool:
        """Deletes a notice from the database."""
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM Notices WHERE NoticeID = %s"
            cursor.execute(sql, (notice_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Database error in delete_notice: {e}")
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                conn.close()
                conn.close()