from datetime import timedelta
import os
import whisper
import logging


def transcribe_audio(path, filename='result'):
    model = whisper.load_model("whisper_models/small.pt")
    logging.info("Whisper model loaded.")
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))
        text = segment['text']
        # segmentId = segment['id']+1
        segment = f"{startTime} - {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        srtFilename = f'result/{filename}.srt'
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srtFilename

if __name__ == '__main__':
    transcribe_audio(path="result/Возврат товаров неплательщиком НДС в 1С 83 Бухгалтерия.mp3", 
                     filename='test')

# whisper.load_model('small')

