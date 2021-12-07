#!/usr/bin/python3

''' components: 
- 2 motors (1 for rotating base, 1 for distributing card)
- LED to show who's turn it is (user input of buttons)
- photores to show if cards in holder or if empty
- buttons (show if new round or if next turn)
'''
import RPi.GPIO as GPIO
import time
import json
from stepper import Stepper

GPIO.setmode(GPIO.BCM)
# declare variables 
myStepper = Stepper()
DCpin = 20  #use 3.3V?
button = 12
GPIO.setup(DCpin, GPIO.OUT)
GPIO.setup(button, GPIO.IN)
GPIO.setup(button, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
pwm = GPIO.PWM(DCpin,100)
pwm.start(0)
while True:
  try:
    if GPIO.input(button) == 1:
      pwm.ChangeDutyCycle(35)
      time.sleep(10)
      pwm.ChangeDutyCycle(0)
      myStepper.goAngle(90,1)
    else:
      continue
  except Exception as e:
    print(e)
    GPIO.cleanup()
# functions
# handing out cards for this game
# load data
'''
with open("/usr/lib/cgi-bin...") as f:
  data = json.load(f) 

# read from text doc
game = data["game"]
'''
'''
photoPin = 3
GPIO.setup(photoPin, GPIO.IN) 
# read photores pin
photores = GPIO.input(photoPin)
# if photores not covered
  # tell user to put cards in card holder
# if photores is covered & game called from website

if photores > 20:
  # start handing out cards
  # for number of cards to each player for this game
  for cards in range(13):
    # for number of players
    for players in range(4):
      # rotate base certain number degrees
      myStepper.goAngle(90,1)
      # distribute 1 card
'''      
# if button pressed refering to next round
  # hand out cards in same manner
# if button pressed refering to new turn
  # change LED color according to order of player colors


# thread to check for end of game button being pressed
'''
if game == goFish:
  noWinner = True
  while (noWinner):
    if buttonTurn == 1:
      #deal another card to current player
      # change LED color
      # move motor to next player in order
      # maybe for degrees have those set in an array or a tuple so that the degrees and direction are always the same
    if keypadPress==1:
      noWinner = False
      # Winner is corresponding to number pressed on keypad
      # display html screen with option of starting a new game 
if game == prez
  noWinner = True
  while (noWinner):
    if buttonTurn == 1:
      # change LED
    if keypadPress ==1:
      noWinner = False
      # Winner displayed on html screen
'''