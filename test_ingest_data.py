# Import necessary modules
import unittest
import os
import psycopg2
from moviepy.editor import VideoFileClip
import pandas as pd

# Import the function to be tested
from ingest_video_data import ingest_video_data

# Define a test case class for testing the ingest_video_data function
class TestIngestVideoData(unittest.TestCase):

    # Set up the test environment before each test
    def setUp(self):
        # Connect to the PostgreSQL database
        self.conn = psycopg2.connect(database="apexdb", user="postgres", host="127.0.0.1", port="5432")
        
        # Set up a single clip for testing: Take the first 60 seconds of "airshow.mp4" and write it to a new video file "0thFrame.mp4"
        self.clip = VideoFileClip("airshow.mp4").subclip(0, 60)
        self.clip.write_videofile("video_clips/0thFrame.mp4", codec='libx264')

    # Clean up the test environment after each test
    def tearDown(self):
        # Close the database connection
        self.conn.close()

    # Define a test case for testing the data ingestion function
    def test_data_ingestion(self):
        # Call the ingest_video_data function
        ingest_video_data(self.conn) 

        # Retrieve data from the video_data table
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM video_data")
        rows = cur.fetchall()

        # Assert that the inserted data matches the data of the test clip
        self.assertEqual(rows[0][0], "0thFrame")
        self.assertEqual(rows[0][1], "mp4")
        self.assertAlmostEqual(rows[0][2], self.clip.duration, places=1)
        self.assertEqual(rows[0][3], "/Users/jorge/Desktop/apex_coding_assignment/video_clips/0thFrame.mp4")

        # Assert that the timestamp is not null
        self.assertIsNotNone(rows[0][4])

    # Define a test case for testing the CSV file generation
    def test_csv_generation(self):
        # Call the ingest_video_data function
        ingest_video_data(self.conn)

        # Assert that the CSV file has been created
        csv_file_path = "report/generated_video_files.csv"
        self.assertTrue(os.path.exists(csv_file_path), f"CSV file was not created at {csv_file_path}")

        # Load the CSV file into a DataFrame and assert that it has the expected content
        df = pd.read_csv(csv_file_path)
        self.assertTrue(len(df) > 0, "CSV file is empty")
        expected_columns = ['clip_name', 'clip_file_extension', 'clip_duration', 'clip_location', 'insert_timestamp']
        self.assertTrue(all(column in df.columns for column in expected_columns), "CSV file does not have expected columns")


# Run the tests if this module is the main module
if __name__ == "__main__":
    unittest.main()
