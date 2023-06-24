import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
from PIL import Image
from utils import time_decorator


def extract_audio_from_video(video_path):
    base_path, filename = os.path.split(video_path)
    filename_without_ext = os.path.splitext(filename)[0]
    
    audio_path = os.path.join(base_path, f"{filename_without_ext}.mp3")
    
    video_clip = VideoFileClip(video_path)
    
    audio_clip = video_clip.audio
    
    audio_clip.write_audiofile(audio_path)
    

    return audio_path


def capture_screenshots(video_url, output_dir, interval):
    yt = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)

    stream = yt.streams.get_highest_resolution()

    video_file = stream.download(output_path='result')

    audio_file = extract_audio_from_video(video_file)

    # os.makedirs(output_dir, exist_ok=True)

    timestamp = 0
    screenshot_index = 1
    while True:
        screenshot_filename = f'{output_dir}/{video_file}_screenshot_{screenshot_index}_{timestamp}.jpg'
        video_clip = VideoFileClip(video_file)
        frame = video_clip.get_frame(timestamp)

        image = Image.fromarray(frame)
        image.save(screenshot_filename, quality=100)

        timestamp += interval
        screenshot_index += 1

        if timestamp > video_clip.duration:
            break

        video_clip.close()
    
    return video_file, audio_file
    # эту строчку использовать после распознавания
    # os.remove(video_file)

video_url = 'https://www.youtube.com/watch?v=rVUHUgEO6qE&ab_channel=%D0%91%D1%83%D1%85%D0%AD%D0%BA%D1%81%D0%BF%D0%B5%D1%80%D1%828-%D0%BE%D1%84%D0%B8%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%D0%BA%D0%B0%D0%BD%D0%B0%D0%BB'
output_dir = 'screenshots'
interval = 5  # Интервал между скриншотами (в секундах)


if __name__ == '__main__':
    capture_screenshots(video_url, output_dir, interval)