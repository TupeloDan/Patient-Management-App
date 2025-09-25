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
            # The stored procedure expects today's date as an argument
            cursor.callproc("sp_GetActiveNotices", (date.today(),))
            for result in cursor.stored_results():
                # Stored procedure returns rows, and we need the first item in each row
                notices = [row[0] for row in result.fetchall()]
        except Exception as e:
            print(f"Database error in get_active_notices: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return notices