import os
import time
import board
import digitalio
import subprocess
import adafruit_ssd1306
import RPi.GPIO as GPIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

path = os.path.dirname(__file__) + '/'

oled_reset = digitalio.DigitalInOut(board.D4)
WIDTH = 128
HEIGHT = 64
BORDER = 5

LOOPTIME = 1.0

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(
    WIDTH, HEIGHT, i2c, addr=0x3c, reset=oled_reset)
oled.fill(0)
oled.show()

width = oled.width
height = oled.height

image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)
top = -2
x = 0

time_font = ImageFont.truetype(path + 'fonts/Roboto-Regular.ttf', 11)
icon_font = ImageFont.truetype(path + 'fonts/icomoon.ttf', 15)
font = ImageFont.truetype(path + 'fonts/Roboto-Light.ttf', 11)
fonts = ImageFont.truetype(path + 'fonts/Roboto-Regular.ttf', 40)
font1 = ImageFont.truetype(path + 'fonts/Roboto-Light.ttf', 12)
font2 = ImageFont.truetype(path + 'fonts/Roboto-Bold.ttf', 16)
font3 = ImageFont.truetype(path + 'fonts/Roboto-Light.ttf', 15)


def time_page(semi_colon):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    current_time = datetime.now()
    if semi_colon:
        disp = current_time.strftime("%I:%M")
    else:
        disp = current_time.strftime("%I %M")
    draw.text((x+2, top+16), disp,  font=fonts, fill=255)
    draw.text((x+105, top+40), current_time.strftime("%p"),
              font=font2, fill=255)
    dates = current_time.strftime("%d/%m %a")
    draw.text((x+35, top+54), dates,  font=font1, fill=255)


def stats():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    IP = str(subprocess.check_output("hostname -I | cut -d\' \' -f1 | head --bytes -1", shell=True), 'utf-8')
    CPU = str(subprocess.check_output("top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'", shell=True), 'utf-8')
    MemUsage = str(subprocess.check_output("free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'", shell=True), 'utf-8')
    Disk = str(subprocess.check_output("df -h | awk '$NF==\"/mnt/hdd\"{printf \"%sB/%sB ~ %s\", $3,$2,$5}'", shell=True), 'utf-8')
    Temperature = str(subprocess.check_output("vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1", shell=True), 'utf-8')
    draw.text((x, top+20),    "\ue917",  font=icon_font, fill=255)
    draw.text((x+16, top+20), IP,  font=font3, fill=255)
    draw.text((x, top+37),    "\ue92a",  font=icon_font, fill=255)
    draw.text((x+17, top+37), Temperature,  font=font, fill=255)
    draw.text((x+65, top+37), "\ue922",  font=icon_font, fill=255)
    draw.text((x+85, top+37), MemUsage,  font=font, fill=255)
    draw.text((x, top+49), "\ue924",  font=icon_font, fill=255)
    draw.text((x, top+53), "\ue924",  font=icon_font, fill=255)
    draw.text((x+17, top+53), Disk,  font=font, fill=255)


def clean():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)


def notification():
    Under_voltage = subprocess.check_output('vcgencmd get_throttled', shell=True)
    txt = str(Under_voltage, 'utf8').strip().split("=")
    if txt[1] == "0x0":
        pass
    else:
        draw.text((x+97, top+2), "\ue927",  font=icon_font, fill=255)

    Temp = subprocess.check_output("vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1", shell=True)
    txt = float(str(Temp, 'utf8')[:-2])
    if txt <= 50:
        draw.text((x+113, top+2), "\ue908",  font=icon_font, fill=255)
    elif txt <= 70:
        draw.text((x+113, top+2), "\ue923",  font=icon_font, fill=255)
    else:
        draw.text((x+113, top+2), "\ue91f",  font=icon_font, fill=255)

matrix = ("toggle", "hotspot",
          "shutdown", "reboot")
def press():
    for j in range(2):
        GPIO.output(COL[j], 1)
        for i in range(2):
            if GPIO.input(ROW[i]) == 1:
                m = ((i * 2) + j)
                return matrix[m]

        GPIO.output(COL[j], 0)

def button(cmd):
    if cmd == "shutdown":
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((4, 18), "Press once more to",  font=font3, fill=255)
        draw.text((4, 38), "SHUTDOWN",  font=font3, fill=255)
        time.sleep(0.2)
        com = press()
        if com == "shutdown":
            clean()
            for x in range(1, 51):
                image = Image.open(path + '/animation3/frame ('+str(x)+').pbm').convert('1')
                oled.image(image)
                oled.show()
            os.system("sudo shutdown now")
        else: clean()
            
    elif cmd == "reboot":
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((4, 18), "Press once more to",  font=font3, fill=255)
        draw.text((4, 38), "REBOOT",  font=font3, fill=255)
        time.sleep(0.2)
        com = press()
        if com == "reboot":
            clean()
            for x in range(1, 51):
                image = Image.open(path + '/animation3/frame ('+str(x)+').pbm').convert('1')
                oled.image(image)
                oled.show()
            os.system("sudo reboot now")
        else: clean()



COL = (25, 8) #coloumn gpio pins
ROW = (23, 24) #row gpio pins

for j in range(2):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 0)

for i in range(2):
    GPIO.setup(ROW[i], GPIO.IN)


page = 0

semi_colon = True

while True:
    if page == 0:
        time_page(semi_colon)
        notification()
    elif page == 1:    
        stats()
        notification()
    elif page == 2:
        clean()
    else:
        page = 0
    for j in range(2):
        GPIO.output(COL[j], 1)
        for i in range(2):
            if GPIO.input(ROW[i]) == 1:
                m = ((i * 2) + j)
                if matrix[m]  == "toggle":
                    page = page + 1
                    time.sleep(0.3)
                else: button(matrix[m])
   
        GPIO.output(COL[j], 0)
    semi_colon = not semi_colon
    oled.image(image)
    oled.show()
    time.sleep(LOOPTIME)
