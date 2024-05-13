# import some modules

import whisper
from moviepy.editor import *
from dotenv import load_dotenv
from pydub import AudioSegment


# Init some variables
input_file = "audio.mp3"
output_folder = "output"
split_duration = 20*30 * 1000  # Split every 10 minutes
text=[]

# split the mp3 in piece of 10 minutes 
def split_mp3(input_file, output_folder, split_duration):
    audio = AudioSegment.from_mp3(input_file)
    duration = len(audio)
    for i, start_time in enumerate(range(0, duration, split_duration)):
        end_time = min(start_time + split_duration, duration)
        split_audio = audio[start_time:end_time]
        split_audio.export(f"{output_folder}/split_{i}.mp3", format="mp3")

# generate mp3 file
def gen_mp3():
    video = VideoFileClip("audio.mp4")
    video.audio.write_audiofile("audio.mp3")
    

# convert mp3 to text
def mp3_to_text(mp3_file_path):
    # Load the model
    model = whisper.load_model("base")

    # Load and transcribe the audio file
    result = model.transcribe(mp3_file_path)
    
    # Print the transcription
    print(result["text"])


# cleaning
def cleaning():
    os.remove("audio.mp3")
    for filename in os.listdir(output_folder):
        os.remove(os.path.dirname(os.path.abspath(filename))+"/output/"+filename)


# Loop through each file in the folder
def process():
    try:
        gen_mp3()
        split_mp3(input_file,output_folder,split_duration)
        for filename in os.listdir(output_folder):
            print("------------------------------------------------------------------")
            print(os.path.dirname(os.path.abspath(filename))+"/output/"+filename)
            mp3_to_text(os.path.dirname(os.path.abspath(filename))+"/output/"+filename)
        cleaning()
    except:
        print("Something wrong happened")


if __name__ == "__main__":
    process()
        




