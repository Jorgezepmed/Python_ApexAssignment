import os
from moviepy.editor import VideoFileClip

# Function to cut a longer video into 1-minute clips
def cut_video():
    # Check if the directory for saving video clips exists. If it doesn't, create it.
    if not os.path.exists('video_clips'):
        os.makedirs('video_clips')

    # Load the video file that we want to cut into smaller clips
    video = VideoFileClip("airshow.mp4")

    # Retrieve the total duration of the video (in seconds)
    duration = video.duration
    n_clips = int(duration // 60)

    # Loop through each of the 1-minute intervals
    for i in range(n_clips):
        # Define the start time and end time (in seconds) for each clip
        start_time = i * 60
        end_time = (i + 1) * 60

        # If the end time exceeds the total video duration, adjust it to be the video duration
        if end_time > duration:
            end_time = duration

        # Generate a subclip for the current interval
        subclip = video.subclip(start_time, end_time)

        # Define the output file name for the current subclip, using the start time as the identifier
        output_file_name = f"video_clips/{start_time}thFrame.mp4"

        # Write the subclip to a file with the defined file name
        subclip.write_videofile(output_file_name, codec='libx264')


if __name__ == "__main__":
    cut_video()