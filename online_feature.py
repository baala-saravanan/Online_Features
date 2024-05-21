import os
import vlc
import time
import gpio as GPIO
import pyttsx3
from pydub import AudioSegment
import sys
sys.path.insert(0, '/home/rock/Desktop/Hearsight/')
from config import *
from play_audio import GTTSA
#from English.machine_voice.machine_voice import MachineVoices

play_file = GTTSA()

# Initialize VLC instance

# Define constants
FEATURE_AUDIO_PATH = '/home/rock/Desktop/Hearsight/English/online_features/'

# Create MachineVoices instance
#machineVoice_obj = MachineVoices()

# Set up GPIO
GPIO.setup(450, GPIO.IN)
GPIO.setup(421, GPIO.IN)
GPIO.setup(447, GPIO.IN)
GPIO.setup(448, GPIO.IN)

engine = pyttsx3.init()

class Reader:
    def exit_button(self):
        play_file.play_audio_file("feature_exited.mp3")
        return
    
    def get_audio_duration(self, filename):
        audio = AudioSegment.from_file(filename)
        duration_in_seconds = len(audio) / 1000  # Convert milliseconds to seconds
        return duration_in_seconds
    
    def play_audio(self,feature_name):
        
        with open(LANG_FILE,'r') as file:
            language = file.read()
            
#        audio_path = f"/home/rock/Desktop/Hearsight/English/online_features/{language}_audio/{feature_name}_audio"
        audio_path = f"/home/rock/Desktop/Hearsight/English/online_features/{feature_name}_audios"
        arr = os.listdir(audio_path)
        file = None
        if not arr:
            play_file.play_audio_file("No files to read.mp3")
            return
        play_file.play_audio_file("press feature button to select the files.mp3")
        limit = len(arr)
        count = -1
        file = None
        while True:         
            time.sleep(0.0001)
            forward = GPIO.input(450)
            backward = GPIO.input(421)
            
            if forward:
                count = (count + 1) % limit
            if backward:
                count = (count - 1) % limit
                
            if forward or backward:
                selected_file = arr[count]
                name = os.path.splitext(selected_file)[0]
#                machineVoice_obj.speak(name + str(count))
#                engine.setProperty('voice', 'english_rp+f3')
#                engine.setProperty('rate', 120)
                engine.setProperty('voice', 'en-gb')
                engine.setProperty('rate', 140)
#                engine.say(name + str(count))
                engine.say(name)
                engine.runAndWait()
                file = os.path.join(audio_path, selected_file)
                
            input_state = GPIO.input(447)
            if input_state == True:
                if file == None:
                    file = os.path.join(audio_path, arr[0])
                time.sleep(1)
                play_file.play_audio_file("feature_confirmed.mp3")
                play_file.play_audio_file(file)
                play_file.play_audio_file("press feature button to select the files.mp3")
                
            input_state = GPIO.input(448)
            if input_state == True:
                play_file.play_audio_file("feature_exited.mp3")
                time.sleep(1)
                break

    def remove_file(self,feature_name):
        
        with open(LANG_FILE,'r') as file:
            language = file.read()
            
#        audio_path = f"/home/rock/Desktop/Hearsight/English/online_features/{language}_audio/{feature_name}_audio"
        audio_path = f"/home/rock/Desktop/Hearsight/English/online_features/{feature_name}_audios"
        arr = os.listdir(audio_path)
        
        if not arr:
            play_file.play_audio_file("No files to delete.mp3")
            return
        
        play_file.play_audio_file("press_feature_button.mp3")
        
        selected_file = None
        selected_index = -1
        
        while True:
            forward = GPIO.input(450)
            backward = GPIO.input(421)
            
            if forward:
                selected_index = (selected_index + 1) % len(arr)
            if backward:
                selected_index = (selected_index - 1) % len(arr)
            
            if forward or backward:
                selected_file = arr[selected_index]
                name = os.path.splitext(selected_file)[0]
#                machineVoice_obj.speak(name + str(selected_index))
#                engine.setProperty('voice', 'english_rp+f3')
#                engine.setProperty('rate', 120)
                engine.setProperty('voice', 'en-gb')
                engine.setProperty('rate', 140)
#                engine.say(name + str(selected_index))
                engine.say(name)
                engine.runAndWait()
                
            input_state = GPIO.input(447)
            if input_state == True and selected_file:
                time.sleep(1)
                play_file.play_audio_file("feature_confirmed.mp3")
                
                file_to_delete = os.path.join(audio_path, selected_file)
                
                try:
                    os.remove(file_to_delete)
                    play_file.play_audio_file("file deleted successfully.mp3")
                except Exception as e:
                    print("Error deleting file:", e)
                    play_file.play_audio_file("Error deleting file.mp3")
                break
                
            input_state = GPIO.input(448)
            if input_state == True:
                play_file.play_audio_file("feature_exited.mp3")
                break




