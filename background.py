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
noWinner.value = 1
p = multiprocessing.Process(target = gf.check_keypad,args=(noWinner,))
p.daemon = True
p.start()
#t.join()

while True:
  try:
      #readyToBegin, game, num, playerInfo = gf.get_game_info()
      readyToBegin = True
      game = "Go Fish!"
      num = 2
      playerInfo = {}
      playerInfo['Player1'] = ['test',[255,0,0]]
      playerInfo['Player2'] = ['test2', [0,255,0]]
      if (readyToBegin):
          readyToBegin = False
          #print(playerInfo)
          
          #gf.deal_setup(num, game)
          currPlayer = 1
          game = "Go Fish!"
          num = 2
          info_key = "Player"

          if (game == "Go Fish!"):
              print("Go Fish!")
              print(noWinner.value)
              noWinner.value = 1
              info_key = info_key + str(currPlayer)
              
              #gf.setup_turn(playerInfo[info_key][1])
              
              while (noWinner.value == 1):
                letter = 'E'
                letter = gf.getCard()
                if letter == 'A':
                  gf.deal_card()
                  print(letter)  
                if GPIO.input(button) == 1:
                  
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
              print("end")
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
    
  except Exception as e:
    print(e)
    #GPIO.cleanup()