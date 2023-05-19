# Import necessary modules
import unittest
import psycopg2
from psycopg2 import sql
from create_table import create_table

# Define a test case class for testing the create_table function
class TestCreateTable(unittest.TestCase):

    # Set up the test environment before each test
    def setUp(self):
        # Connect to the PostgreSQL database
        self.conn = psycopg2.connect(database="apexdb", user="postgres", host="127.0.0.1", port="5432")

    # Clean up the test environment after each test
    def tearDown(self):
        # Close the database connection
        self.conn.close()

    # Define a test case for testing the table creation function
    def test_table_creation(self):
        # Call the create_table function
        create_table(self.conn)

        # Open a cursor to perform database operations
        cur = self.conn.cursor()

        # Check if the table exists
        cur.execute("""
            SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE  table_name   = 'video_data'
            );
        """)
        table_exists = cur.fetchone()[0]
        
        # Assert that the table does exist
        self.assertTrue(table_exists)

        # Check the structure of the table
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns
            WHERE table_name = 'video_data'
            ORDER BY ordinal_position;
        """)
        columns = cur.fetchall()

        # Expected column structure of the table
        expected_columns = [
            ('clip_name', 'text'),
            ('clip_file_extension', 'text'),
            ('clip_duration', 'double precision'),
            ('clip_location', 'text'),
            ('insert_timestamp', 'timestamp without time zone'),
        ]

        # Assert that the actual column structure matches the expected column structure
        self.assertEqual(columns, expected_columns)

        # Check if the table is empty
        cur.execute("SELECT * FROM video_data")
        rows = cur.fetchall()
        
        # Assert that the table is empty
        self.assertEqual(rows, [])

# Run the tests if this module is the main module
if __name__ == "__main__":
    unittest.main()
