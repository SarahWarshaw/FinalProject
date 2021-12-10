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
import gamefunctions as gf
import multiprocessing

GPIO.setmode(GPIO.BCM)

# Flags for game readiness
readyToBegin = False

#Button
button = 12
GPIO.setup(button, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#multiprocessing for keypad
noWinner = multiprocessing.Value('i')
noWinner = 1
p = multiprocessing.Process(target = gf.check_keypad,args=(noWinner,))
p.daemon = True
p.start()

while True:
  try:
      readyToBegin, game, num, playerInfo = gf.get_game_info()
      if (readyToBegin):
          print(playerInfo)
          
          gf.deal_setup(num, game)
          currPlayer = 1
          info_key = "Player"

          if (game == "Go Fish!"):
              print("Go Fish!")
              noWinner = 1
              info_key = info_key + str(currPlayer)
              
              gf.setup_turn(playerInfo[info_key][1])
              
              while (noWinner==1):
                if GPIO.input(button) == 1:
                  
                  print("42")
                  gf.deal_card()
                  if (currPlayer < num):
                      gf.end_turn(num, 1)
                  # Arrange how to iterate by the dictionary keys
                  # if we're already at last player, need to reverse motor
                  
                  oldPlayer = currPlayer
                  
                  if (currPlayer == num):
                      currPlayer = 0
                      gf.reverseMotor(num, -1)
                      
                  currPlayer += 1
                  info_key = info_key.replace(str(oldPlayer), str(currPlayer))
                  print(info_key)
                      
                  gf.setup_turn(playerInfo[info_key][1])
                  # maybe for degrees have those set in an array or a tuple so that the degrees and direction are always the same
                '''
                if keypadPress==1:
                  noWinner = False
                  # Winner is corresponding to number pressed on keypad
                  # display html screen with option of starting a new game
          
          elif (game == "Prez"):
          noWinner = True
          while (noWinner):
            if buttonTurn == 1:
              # change LED
            if keypadPress ==1:
              noWinner = False
              # Winner displayed on html screen
    ''' 
              print(noWinner)
  except Exception as e:
    print(e)
    #GPIO.cleanup()
    
