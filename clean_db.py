import phoenixdb
import os

def clean_database_table(database_url, table_name, **opts):
    """
    Deletes all records from the specified table in the database while keeping the table structure.
    
    :param database_url: URL of the Phoenix database.
    :param table_name: Name of the table to clean.
    :param opts: Additional options such as authentication for the database connection.
    """
    # Connect to Phoenix
    conn = phoenixdb.connect(database_url, autocommit=True, **opts)
    cursor = conn.cursor()

    # SQL statement to delete all records from the table
    delete_query = f"DELETE FROM {table_name}"

    # Execute the delete query
    cursor.execute(delete_query)
    print(f"All records have been deleted from the table: {table_name}")

    # Close the cursor and connection
    cursor.close()
    conn.close()

if __name__ == '__main__':
    # Database configuration
    database_url = os.getenv('DATABASE_URL')
    table_name = "INVOICES"  # Replace with your actual table name

    # Additional options for database connection
    opts = {
        'authentication': os.getenv('AUTHENTICATION'),  # Default to 'BASIC' if not set
        'serialization': os.getenv('SERIALIZATION'),  # Default to 'PROTOBUF' if not set
        'avatica_user': os.getenv('AVATICA_USER'),
        'avatica_password': os.getenv('AVATICA_PASSWORD')
    }

    # Call the function to clean the table
    clean_database_table(database_url, table_name, **opts)
