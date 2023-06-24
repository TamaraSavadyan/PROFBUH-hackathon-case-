# import subprocess

# model = 'large-v2' # large-v2
# command = f'whisper --language ru --model {model} -o ./result -- GSPD.mp3'
# subprocess.run(command, shell=True)

# def video_to_text(video_file):
#     command = f'!whisper "{video_file}"'
#     subprocess.run(command, shell=True)

# import whisper

# def create_model_instance(model_type: str):
#     return whisper.load_model(model_type)

# model = whisper.load_model("C:/Users/Tamara/.cache/whisper/large-v2.pt")
# result = model.transcribe("result/GSPD.mp3")
# print(result["text"])

# import whisper
# import hashlib
# from pytube import YouTube
# from datetime import timedelta
# import os

# def download_video(url):
#     print("Start downloading", url)
#     yt = YouTube(url)

#     hash_file = hashlib.md5()
#     hash_file.update(yt.title.encode())

#     file_name = f'{hash_file.hexdigest()}.mp4'

#     yt.streams.first().download("", file_name)
#     print("Downloaded to", file_name)

#     return {
#         "file_name": file_name,
#         "title": yt.title
#     }

# def transcribe_audio(path):
#     model = whisper.load_model("base") # Change this to your desired model
#     print("Whisper model loaded.")
#     video = download_video(path)
#     transcribe = model.transcribe(video["file_name"])
#     os.remove(video["file_name"])
#     segments = transcribe['segments']

#     for segment in segments:
#         startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
#         endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
#         text = segment['text']
#         segmentId = segment['id']+1
#         segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

#         srtFilename = os.path.join(r"C:\Transcribe_project", "your_srt_file_name.srt")
#         with open(srtFilename, 'a', encoding='utf-8') as srtFile:
#             srtFile.write(segment)

#     return srtFilename

# link = "https://www.youtube.com/watch?v=8qpwqDnvTok"
# result = transcribe_audio(link)

from datetime import timedelta
import os
import whisper
import logging

def transcribe_audio(path, filename='result'):
    model = whisper.load_model("C:/Users/Tamara/.cache/whisper/small.pt") # Change this to your desired model
    logging.info("Whisper model loaded.")
    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        srtFilename = f'result/{filename}.srt'
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srtFilename

if __name__ == '__main__':
    transcribe_audio(path="result/Возврат товаров неплательщиком НДС в 1С 83 Бухгалтерия.mp3", filename='test')

# whisper.load_model('small')

