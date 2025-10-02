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
        # Using 'with' statements ensures resources are properly managed
        try:
            with conn.cursor(dictionary=True) as cursor:
                sql = "SELECT ControlName, CaptionText FROM UIText WHERE FormContext = %s"
                cursor.execute(sql, (context,))
                
                for row in cursor.fetchall():
                    text_elements[row['ControlName']] = row['CaptionText']

        except Exception as e:
            print(f"Database error in get_ui_text_by_context: {e}")
        finally:
            if conn and conn.is_connected():
                conn.close()
        
        return text_elements

    def update_ui_text(self, context: str, control_name: str, new_text: str) -> bool:
        """Updates a single UI text entry in the database."""
        conn = get_db_connection()
        if not conn:
            return False
        
        success = False
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE UIText SET CaptionText = %s WHERE FormContext = %s AND ControlName = %s"
                cursor.execute(sql, (new_text, context, control_name))
            
            conn.commit()
            
            if cursor.rowcount > 0:
                success = True
                print(f"Successfully updated UIText for {context} - {control_name}")

        except Exception as e:
            print(f"Database error in update_ui_text: {e}")
            conn.rollback()
        finally:
            if conn and conn.is_connected():
                conn.close()
        
        return success