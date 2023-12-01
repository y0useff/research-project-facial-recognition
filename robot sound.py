from gtts import gTTS
import pygame
import time

#lets say input from detect function can be a name of the person detected.
def play_sound(detect_name):
    text = "Found {}"
    m=text.format(detect_name)
    tts = gTTS(text=m, lang='en',slow=True)
    tts.save("output.mp3")
    play_robot_voice("output.mp3")
    time.sleep(2)
    play_robot_voice("output.mp3")
    time.sleep(2)
    play_robot_voice("output.mp3")



def play_robot_voice(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
play_sound("name")





