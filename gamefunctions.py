'''
Header file containing methods for card game functionality
'''
import RPi.GPIO as GPIO
import time
from time import sleep
import re
from stepper import Stepper
import json
import multiprocessing

GPIO.setmode(GPIO.BCM)

# Motor setup
myStepper = Stepper()
DCpin = 20 
GPIO.setup(DCpin, GPIO.OUT)
pwm = GPIO.PWM(DCpin,100)
pwm.start(0)

# Keypad setup
rows = [26,19,13,6]
cols = [5,27,17,4]


#LED setup
pins = (16, 24, 25) # R = 13, G = 24, B = 25
GPIO.setup(16, GPIO.OUT, initial=1)
GPIO.setup(24, GPIO.OUT, initial=1)
GPIO.setup(25, GPIO.OUT, initial=1)

pwmR = GPIO.PWM(16, 2000)  # set each PWM pin to 2 KHz
pwmG = GPIO.PWM(24, 2000)
pwmB = GPIO.PWM(25, 2000)
pwmR.start(0)   # initially set to 0 duty cycle
pwmG.start(0)
pwmB.start(0)

for i in range(4):
  GPIO.setup(rows[i], GPIO.OUT)
  GPIO.setup(cols[i], GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

def get_game_info():
    # var to return
    myPlayers = {}
    ready = False
    varCheck = False
    
    # Need to read in files with game and player information
    # Check if files have already been read in
    with open("/usr/lib/cgi-bin/home-screen.txt", 'r') as f:
      data = json.load(f) 
    # read from text doc
    game = data["game_choice"]
    num = int(data["player_num"])
    
    if (game != "Going"):
        
        # Next, open up the player information file
        with open("/usr/lib/cgi-bin/player-screen.txt", 'r') as f:
            playerData = json.load(f)
        
        if (playerData["Player1"] != "Going"):
            
            varCheck = True

            for player in playerData.keys():
                playerPattern = '^Name:(.*),,,Color:\((\d{1,3}),(\d{1,3}),(\d{1,3})\)$'
                myMatch = re.search(playerPattern, playerData[player])
                if myMatch:
                    myColors = []
                    for i in range(0,3):
                        myColors.append(int(myMatch.group(i+2)))
                    
                    myPlayers[player] = [myMatch.group(1), myColors]
                    
            # Write to file that game is now going on
            data = {"game_choice":"Going", "player_num":num}
            with open("/usr/lib/cgi-bin/home-screen.txt", 'w') as f:
                json.dump(data, f)
            
            # Write to file that game is now going on
            data = {"Player1":"Going", "player_num":"Done"}
            with open("/usr/lib/cgi-bin/player-screen.txt", 'w') as f:
                json.dump(data, f)
                
            ready = True

    # Do we have to overwrite the files?
    return ready, game, num, myPlayers

# based on game, deal the correct cards
def deal_setup(numUsers, myGame):
    
    global myStepper
    
    playerAngle = 360/numUsers
    
    if (myGame == "Go Fish!"):
        # https://bicyclecards.com/how-to-play/go-fish/
        if (numUsers < 4):
            multiplier = 7
        else:
            multiplier = 5
    elif (myGame == "Prez"):
        multiplier = 52/numUsers
    
    
    myDir = 1
    multiplier = 2
    for i in range (0, multiplier):
    
        for j in range(0, numUsers):
            # need to adjust duty cycle for time for one card
            print(j)
            deal_card()
            if (j < numUsers - 1):
                myStepper.goAngle(playerAngle,myDir)
        
        myStepper.goAngle(360 - playerAngle,-1)

def setup_turn(colorList):
    # display the LED color of the specific player
    # Need to map from 0 - 255 to 0 - 100

    r = int(100 * (colorList[0] / 255))
    g = int(100 * (colorList[1] / 255))
    b = int(100 * (colorList[2] / 255))

    print(r,g,b)

    pwmR.ChangeDutyCycle(r)
    pwmG.ChangeDutyCycle(g)
    pwmB.ChangeDutyCycle(b)
    
def end_turn(numUsers, myDir):

    playerAngle = 360/numUsers
    myStepper.goAngle(playerAngle, myDir)

def reverseMotor(numUsers, myDir):
    playerAngle = 360/numUsers
    myStepper.goAngle(360 - playerAngle, myDir)

def deal_card():
    global pwm
    pwm.ChangeDutyCycle(70)
    sleep(5)
    pwm.ChangeDutyCycle(0)
 
def check_keypad(noWinner):
    
    while (noWinner.value == 1):
        try:
          winner = "noWinner"
          noWinner.value, winner = readLine(rows[0], ["1","2","3","A"],winner,noWinner)
          noWinner.value, winner = readLine(rows[1], ["4","5","6","B"],winner,noWinner)
          noWinner.value, winner = readLine(rows[2], ["7","8","9","C"],winner,noWinner)
          noWinner.value, winner = readLine(rows[3], ["*","0","#","D"],winner,noWinner)          
        except Exception as e:
          print(e)
    
    
def readLine(line, characters, winner, noWinner):
  GPIO.output(line, GPIO.HIGH)
  if(GPIO.input(cols[0]) == 1):
    winner = "Player" +(characters[0])
    noWinner.value = 0
  if(GPIO.input(cols[1]) == 1):
    winner = "Player" +(characters[1])
    noWinner.value = 0
  if(GPIO.input(cols[2]) == 1):
    winner = "Player" +(characters[2])
    noWinner.value = 0
  if(GPIO.input(cols[3]) == 1):
    winner = "Player" +(characters[3])
    noWinner.value = 0
      
  GPIO.output(line, GPIO.LOW)
  return noWinner.value, winner

def readLetter(line, characters, winner, noWinner):
  GPIO.output(line, GPIO.HIGH)
  if(GPIO.input(cols[0]) == 1):
    winner = "Player" +(characters[0])
    noWinner.value = 0
  if(GPIO.input(cols[1]) == 1):
    winner = "Player" +(characters[1])
    noWinner.value = 0
  if(GPIO.input(cols[2]) == 1):
    winner = "Player" +(characters[2])
    noWinner.value = 0
  if(GPIO.input(cols[3]) == 1):
    winner = "Player" +(characters[3])
    noWinner.value = 0
  if(GPIO.input(cols[4]) == 1):
    noWinner.value = 1  
  GPIO.output(line, GPIO.LOW)
  return noWinner.value, winner