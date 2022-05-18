import time
import pyttsx3
from pymata4 import pymata4
from pyfirmata import Arduino, SERVO
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



def check_distance(): # working
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




def check_temperature(): #LM-35 TEMPERATURE - working!! woks for A1 too
    board.set_pin_mode_analog_input(0)
    for x in range(6):
        voltage, time_stamp = board.analog_read(0)
        temperature_c = (voltage * 5000) / 1024
        print("The temperture is : ", temperature_c / 10)
        time.sleep(2)


def check_LightingMode(): #LDR -work!! (somethimes will skip the first text and show 0 due to speed
    #thus the few repeated tests
    board.set_pin_mode_analog_input(1)
    for x in range(6):
        voltage, time_stamp = board.analog_read(1)
        # light_level = (voltage * 5000) / 1024
        print("The light level is : ", voltage)
        time.sleep(2)
        if (voltage < 420):
            print("It's a little dark, turn on the light!")
        else:
            print("it's so bright!!")

    if (voltage < 420):
         talk("It's a little dark, turn on the light!")
    else:
        talk("it's so bright!!")



def rotate_servo(): #needs checking but i think it would work
    # set the pin mode
    board.set_pin_mode_servo(10)
    board.servo_write(10, 0)
    time.sleep(1)
    board.servo_write(10, 90)
    time.sleep(1)




def run_alexa():
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)

    if 'distance' in command:
        check_distance()

    if 'weather' in command:
        check_temperature()

    if 'light' in command:
        check_LightingMode()

    if 'motor' in command:
        rotate_servo()





run_alexa()