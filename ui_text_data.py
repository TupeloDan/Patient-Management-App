# ui_text_data.py
from database import get_db_connection

class UiTextData:
    """Manages database operations for the UIText table."""

    def get_ui_text_by_context(self, context: str) -> dict:
        """Fetches all UI text elements for a given form context."""
        conn = get_db_connection()
        if not conn:
            return {}
        
        text_elements = {}
        try:
            # Fetches the control name and its corresponding caption text
            sql = "SELECT ControlName, CaptionText FROM UIText WHERE FormContext = %s"
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (context,))
            
            for row in cursor.fetchall():
                text_elements[row['ControlName']] = row['CaptionText']

        except Exception as e:
            print(f"Database error in get_ui_text_by_context: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        
        return text_elements