import datetime
import psycopg2
import os
from psycopg2 import sql
from moviepy.editor import VideoFileClip
import pandas as pd

# Function to ingest video data into PostgreSQL database
def ingest_video_data(conn):
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Load the video clip and calculate the number of 1-minute clips
    clip = VideoFileClip("airshow.mp4")
    duration = clip.duration
    n_clips = int(duration // 60)
    directory = "video_clips"

    # Loop through each 1-minute clip
    for i in range(n_clips):
        # Generate the name of the clip
        clip_name = f"{i * 60}thFrame"
        clip_file_extension = "mp4"
        
        # Load the clip and get the duration and absolute path
        video = VideoFileClip(f"{directory}/{clip_name}.{clip_file_extension}")
        clip_duration = video.duration
        clip_location = os.path.abspath(f"{directory}/{clip_name}.{clip_file_extension}")
        
        # Get the current timestamp
        insert_timestamp = datetime.datetime.now()
        
        # Insert the data into the database
        cur.execute(
            "INSERT INTO video_data (clip_name, clip_file_extension, clip_duration, clip_location, insert_timestamp) VALUES (%s, %s, %s, %s, %s)",
            (clip_name, clip_file_extension, clip_duration, clip_location, insert_timestamp)
        )

    # Commit the changes to the database
    conn.commit()

    # Execute SQL SELECT statement to get all the rows from the table
    cur.execute("SELECT * FROM video_data")
    rows = cur.fetchall()
    
    # Get column names
    columns = [desc[0] for desc in cur.description]

    # Create a  DataFrame from the fetched data
    df = pd.DataFrame(rows, columns=columns)

    # Define the directory for storing the report
    report_directory = "report"
    
    # If the directory doesn't exist, create it
    if not os.path.exists(report_directory):
        os.makedirs(report_directory)

    # Save the DataFrame to a CSV file
    df.to_csv(f"{report_directory}/generated_video_files.csv", index=False)


if __name__ == "__main__":
    conn = psycopg2.connect(database="apexdb", user="postgres", password="your_password", host="127.0.0.1", port="5432")
    ingest_video_data(conn)