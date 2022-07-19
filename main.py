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
digital_for_led = 4
board.set_pin_mode_digital_output(4)
board.set_pin_mode_digital_output(6)
board.set_pin_mode_servo(8)



def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        command = input("Hello, what would you like me to do? : ")
        # will take commands by input
        if 'Alexa' in command:
            command = command.lower()
            command = command.replace('alexa', '')
            print(command)

    except:
        pass
    return command


def check_distance():  # working

    talk("Checking distance.")
    board.set_pin_mode_sonar(triggerPin, echoPin, the_callback)
    engine.say("checking distance now")
    engine.runAndWait()
    try:
      board.sonar_read(triggerPin)
      time.sleep(2)



    except Exception:
        print("error")


def the_callback(data):
    print("Distance ", data[2])


def check_temperature():  # LM-35 TEMPERATURE - working!! works for A1 too
    talk("Checking temperature now.")
    board.set_pin_mode_analog_input(0)
    for x in range(6):
        voltage, time_stamp = board.analog_read(0)
        temperature_c = (voltage * 5000) / 1024
        print("The temperture is : ", temperature_c / 10)
        time.sleep(2)


def check_LightingMode():
    #Make sure that you use the 10 k resistor so that the values will be correct
    # LDR -work!! (somethimes will skip the first text and show 0 due to speed
    # thus the few repeated tests
    talk("Checking light conditions now.")
    board.set_pin_mode_analog_input(1)
    for x in range(6):
        voltage, time_stamp = board.analog_read(1)
        # light_level = (voltage * 5000) / 1024
        print("The light level is : ", voltage)
        time.sleep(2)

    if (voltage < 600 ):
        turn_on_light()

    else:
     print("there is enought light - green lit")
     board.digital_write(6, 1)
     time.sleep(5)
     board.digital_write(6, 0)
     talk("it's so bright you are good to go!! Green Light")




def  turn_on_light():
    talk( "It's a little dark, turn on the light! Red Light")
    board.digital_write(digital_for_led, 1)
    time.sleep(5)
    board.digital_write(digital_for_led, 0)

def rotate_servo():  # would open the door at my command
    talk("Opening the door.")
    pin = 8
    board.servo_write(pin, 280)
    time.sleep(3)


def closeDoorServo():
    talk("Closing the door.")
    time.sleep(2)
    board.servo_write(8, 0)


def run_alexa():
    talk("hello! please write what you would like me to do!")
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

    if 'door' in command:
        rotate_servo()

    if 'close' in command:
        closeDoorServo()



while True :
    run_alexa()
