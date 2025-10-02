# mha_section_data.py
from database import get_db_connection

class MhaSectionData:
    """Manages database operations for MHA_Sections."""
    def get_all_mha_sections(self) -> list[dict]:
        conn = get_db_connection()
        if not conn: return []
        sections = []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT ID, LegalStatus FROM MHA_Sections ORDER BY LegalStatus")
            sections = cursor.fetchall()
        except Exception as e:
            print(f"Database error in get_all_mha_sections: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return sections