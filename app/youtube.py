import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from PIL import Image
from datetime import datetime
from utils import transliterate_russian


def extract_audio_from_video(video_path):
    base_path, filename = os.path.split(video_path)
    filename_without_ext = os.path.splitext(filename)[0]
    
    audio_path = os.path.join(base_path, f"{filename_without_ext}.mp3")
    
    video_clip = VideoFileClip(video_path)
    
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)

    return audio_path


def capture_screenshots(video_url, output_dir, interval, start_time = None, end_time = None):
    
    yt = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
    
    stream = yt.streams.get_highest_resolution()
    

    duration = yt.length

    video_file = stream.download(output_path='result')
    video_title = yt.streams[0].title

    if start_time or end_time:
        output_file_partial = f'result/{video_title}_partial.mp4'            
        if start_time and not end_time:
            end_time = duration
        elif not start_time and end_time:
            start_time = 0

        ffmpeg_extract_subclip(video_file, start_time, end_time, targetname=output_file_partial)
        video_file = output_file_partial

    audio_file = extract_audio_from_video(video_file)

    timestamp = 0
    shot_index = 1
    screenshots_name = video_title[:-4].replace(" ", "_")
    screenshots_name_translit = transliterate_russian(screenshots_name)
    new_dir = f'{output_dir}/{screenshots_name_translit}'
    try:
        os.mkdir(new_dir)
    except FileExistsError:
        print('Folder exists, ignored...')

    while True:
        created_at = datetime.now().strftime("%Y%m%d%H%M%S")
        screenshot_filename = f'{new_dir}/{created_at}_screenshot_{timestamp}.jpg'
        video_clip = VideoFileClip(video_file)
        frame = video_clip.get_frame(timestamp)

        image = Image.fromarray(frame)
        image.save(screenshot_filename, quality=100)

        timestamp += interval
        shot_index += 1

        if timestamp > video_clip.duration:
            break

        video_clip.close()
    
    return video_title, audio_file, new_dir


if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=rVUHUgEO6qE&ab_channel=%D0%91%D1%83%D1%85%D0%AD%D0%BA%D1%81%D0%BF%D0%B5%D1%80%D1%828-%D0%BE%D1%84%D0%B8%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%D0%BA%D0%B0%D0%BD%D0%B0%D0%BB'
    output_dir = 'screenshots'
    interval = 5  # Интервал между скриншотами (в секундах)

    capture_screenshots(video_url, output_dir, interval)