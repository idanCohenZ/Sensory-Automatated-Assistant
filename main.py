import time
import pyttsx3
from pymata4 import pymata4
import pywhatkit

# connect an arduino and find port
board = pymata4.Pymata4()
echoPin = 11
triggerPin = 12
engine = pyttsx3.init()




def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        command = input("Enter your command, my master: ")
        #will take commands by input
        if 'Alexa' in command:
            command = command.lower()
            command = command.replace('alexa', '')
            print(command)

    except:
        pass
    return command


# internet version that looks good - distance with ultra - sonic:
def check_distance():
    board.set_pin_mode_sonar(triggerPin, echoPin, the_callback)
    engine.say("checking distance now")
    engine.runAndWait()
    while True:
        try:
            time.sleep(0.5)
            board.sonar_read(triggerPin)
        except Exception:
            print("error")


def the_callback(data):
    print("Distance ", data[2])








def run_alexa():
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)

    if 'distance' in command:
        check_distance()


run_alexa()