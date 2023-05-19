# Import necessary modules
import datetime
import psycopg2
import os
from psycopg2 import sql
from moviepy.editor import VideoFileClip
import pandas as pd


def ingest_video_data(conn):
    cur = conn.cursor()
    clip = VideoFileClip("airshow.mp4")
    duration = clip.duration
    n_clips = int(duration // 60)
    directory = "video_clips"


    for i in range(n_clips):
        clip_name = f"{i * 60}thFrame"
        clip_file_extension = "mp4"
        
        video = VideoFileClip(f"{directory}/{clip_name}.{clip_file_extension}")
        clip_duration = video.duration
        clip_location = os.path.abspath(f"{directory}/{clip_name}.{clip_file_extension}")
        
        insert_timestamp = datetime.datetime.now()
        

        cur.execute(
            "INSERT INTO video_data (clip_name, clip_file_extension, clip_duration, clip_location, insert_timestamp) VALUES (%s, %s, %s, %s, %s)",
            (clip_name, clip_file_extension, clip_duration, clip_location, insert_timestamp)
        )


    conn.commit()

    # Execute SQL SELECT statement to get all the rows from the table
    cur.execute("SELECT * FROM video_data")
    rows = cur.fetchall()
    
    # Get column names
    columns = [desc[0] for desc in cur.description]

    df = pd.DataFrame(rows, columns=columns)


    report_directory = "report"
    
    if not os.path.exists(report_directory):
        os.makedirs(report_directory)


    df.to_csv(f"{report_directory}/generated_video_files.csv", index=False)



if __name__ == "__main__":
    conn = psycopg2.connect(database="apexdb", user="postgres", host="127.0.0.1", port="5432")
    ingest_video_data(conn)
