from GPIO import GPIO
from time import sleep

rows = [26, 19,13,6]
cols = [5,27,17,4]

GPIO.setmode(GPIO.BCM)

for i in range(4):
  GPIO.setup(rows[i], GPIO.OUT)
  GPIO.setup(cols[i], GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters):
	GPIO.output(line, GPIO.HIGH)
	if(GPIO.input(cols[0]) == 1):
    	    print(characters[0])
	if(GPIO.input(cols[1]) == 1):
        	    print(characters[1])
	if(GPIO.input(cols[2]) == 1):
    	    print(characters[2])
	if(GPIO.input(cols[3]) == 1):
    	    print(characters[3])
	GPIO.output(line, GPIO.LOW)

while True:
  try:
    readLine(rows[0], ["1","2","3","A"])
    readLine(rows[1], ["4","5","6","B"])
    readLine(rows[2], ["7","8","9","C"])
    readLine(rows[3], ["*","0","#","D"])
    sleep(0.1)
  except Exception as e:
    print(e)