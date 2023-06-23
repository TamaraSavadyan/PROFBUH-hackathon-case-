import subprocess

model = 'large-v2' # large-v2
command = f'whisper --language ru --model {model} -o ./result -- piter.mp3'
subprocess.run(command, shell=True)

def video_to_text(video_file):
    command = f'!whisper "{video_file}"'
    subprocess.run(command, shell=True)