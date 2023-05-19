


# Apex Coding Assignment

This repository contains the code for the Apex Coding Assignment, which involves cutting a video into 1-minute clips, creating a PostgreSQL table, and ingesting video data into the table.

## Environment Setup

1. Clone this repository to your local machine.
2. Make sure you have Python 3.x installed.
3. Set up a virtual environment (optional but recommended).
4. Install the required packages by running the following command in your terminal or command prompt:

   ```bash
   pip install -r requirements.txt
   ```

5. Install PostgreSQL and set up the necessary database (e.g., `apexdb`) and user (e.g., `postgres`) with appropriate privileges.

## Running the Code

1. Cut the video into 1-minute clips by running the following command:

   ```bash
   python cut_video.py
   ```

   This will generate the video clips in the `video_clips` folder.

2. Create the PostgreSQL table by running the following command:

   ```bash
   python create_table.py
   ```

   This will create the `video_data` table in the database.

3. Ingest the video data into the table by running the following command:

   ```bash
   python ingest_video_data.py
   ```

   This will insert the video data into the `video_data` table and generate a CSV report in the `report` folder.

## Additional Notes

- The `cut_video.py` script uses the `moviepy` library to cut the video into clips. Make sure you have the necessary codecs and ffmpeg installed.
- The PostgreSQL connection details (database, user, password, host, port) are hardcoded in the code. Update them accordingly before running the scripts.
- Please ensure that you have the required permissions and access to the necessary files and directories.
- For detailed explanations of the code and its functionality, refer to the comments within each script file.



