import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# GPIO.setup(24, GPIO.OUT)
matrix = [1, 2,
          3, 4]


COL = [25, 8]
ROW = [23, 24]

for j in range(2):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 0)

for i in range(2):
    GPIO.setup(ROW[i], GPIO.IN)

while True:
    for j in range(2):

        GPIO.output(COL[j], 1)
        for i in range(2):
            if GPIO.input(ROW[i]) == 1:

                #print("col = ", (j+1))
                #print("row = ", (i+1))

                m = ((i * 2) + j)
                #print("postion = ", (m))
                print(matrix[m])  # u get 1,2,3,4 output here
                print()
                time.sleep(0.1)

                while (GPIO.input(ROW[i]) == 1):
                    # GPIO.output(24,1)
                    time.sleep(0.2)

        # GPIO.output(24,0)
        GPIO.output(COL[j], 0)
