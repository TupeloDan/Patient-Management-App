import mysql.connector
from mysql.connector import errorcode
import configparser


def get_db_connection():
    """
    Reads connection details from config.ini and establishes a connection
    to the MySQL database. Returns the connection object.
    """
    config = configparser.ConfigParser()
    config.read("config.ini")

    try:
        conn = mysql.connector.connect(
            host=config["MySQL"]["host"],
            port=config["MySQL"]["port"],
            user=config["MySQL"]["user"],
            password=config["MySQL"]["password"],
            database=config["MySQL"]["database"],
            autocommit=False,  # <-- THE CRITICAL CHANGE
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None
    except configparser.NoSectionError:
        print("Error: [MySQL] section not found in config.ini")
        return None
    except KeyError as e:
        print(f"Error: Missing key '{e.args[0]}' in [MySQL] section of config.ini")
        return None


# --- This block allows you to test the connection directly ---
if __name__ == "__main__":
    print("Attempting to connect to the database...")
    connection = get_db_connection()
    if connection and connection.is_connected():
        print("✅ Connection successful!")
        connection.close()
        print("Connection closed.")
    else:
        print(
            "❌ Connection failed. Please check your config.ini and that the Docker container is running."
        )
