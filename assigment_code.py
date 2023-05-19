import requests
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import psycopg2
from psycopg2 import sql
import datetime
import pandas as pd

# Paso 1: Descargar el archivo de vídeo
file_url = "https://www.dropbox.com/sh/782f7a0hmw3mn59/AADcJpRoFB0IIfi7-nR-7Eifa/airshow.mp4?dl=1" 
r = requests.get(file_url, stream = True)
with open("airshow.mp4", "wb") as file:
    for block in r.iter_content(chunk_size = 1024):
        if block:
            file.write(block)

# Paso 2: Cortar el vídeo en clips de 1 minuto
directory = "video_clips"
if not os.path.exists(directory):
    os.makedirs(directory)
clip = VideoFileClip("airshow.mp4")
duration = clip.duration
n_clips = int(duration // 60)
for i in range(n_clips):
    start_time = i * 60
    end_time = (i+1) * 60
    output_file_name = f"{directory}/{start_time}thFrame.mov"
    ffmpeg_extract_subclip("airshow.mp4", start_time, end_time, targetname=output_file_name)

# Paso 3 y 4: Crear tabla en PostgreSQL e insertar los datos del clip
conn = psycopg2.connect(database="your_database_name", user="your_user_name", password="your_password", host="127.0.0.1", port="5432")
cur = conn.cursor()
table_name = "video_data"
fields = {
    "clip_name": "TEXT",
    "clip_file_extension": "TEXT",
    "clip_duration": "FLOAT",
    "clip_location": "TEXT",
    "insert_timestamp": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
}
cur.execute(
    sql.SQL("CREATE TABLE {} ({})").format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(sql.SQL("{} {}").format(sql.Identifier(k), sql.SQL(v)) for k, v in fields.items())
    )
)
conn.commit()
for i in range(n_clips):
    clip_name = f"{i * 60}thFrame"
    clip_file_extension = "mov"
    video = VideoFileClip(f"{directory}/{clip_name}.{clip_file_extension}")
    clip_duration = video.duration
    clip_location = os.path.abspath(f"{directory}/{clip_name}.{clip_file_extension}")
    insert_timestamp = datetime.datetime.now()
    cur.execute(
        "INSERT INTO video_data (clip_name, clip_file_extension, clip_duration, clip_location, insert_timestamp) VALUES (%s, %s, %s, %s, %s)",
        (clip_name, clip_file_extension, clip_duration, clip_location, insert_timestamp)
    )
conn.commit()

# Paso 5: Generar el archivo CSV
cur.execute("SELECT * FROM video_data")
rows = cur.fetchall()
columns = [desc[0] for desc in cur.description]
df = pd.DataFrame(rows, columns=columns)
report
