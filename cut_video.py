# Import necessary libraries
import os
from moviepy.editor import VideoFileClip

def cut_video():

    if not os.path.exists('video_clips'):
        os.makedirs('video_clips')

    video = VideoFileClip("airshow.mp4")

    duration = video.duration
    n_clips = int(duration // 60)

    for i in range(n_clips):
        start_time = i * 60
        end_time = (i + 1) * 60

        # If the end time exceeds the total video duration, adjust it to be the video duration
        if end_time > duration:
            end_time = duration

        # Generate a subclip for the current interval
        subclip = video.subclip(start_time, end_time)

        output_file_name = f"video_clips/{start_time}thFrame.mp4"
        subclip.write_videofile(output_file_name, codec='libx264')

if __name__ == "__main__":
    cut_video()
