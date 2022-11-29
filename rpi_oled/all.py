import os
import time
import board
import digitalio
import subprocess
from threading import Thread
import json
import adafruit_ssd1306
import RPi.GPIO as GPIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

path = os.path.dirname(__file__) + '/'
f = open(path + "configure.json")
data = json.load(f)
f.close()


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

oled_reset = digitalio.DigitalInOut(board.D4)
WIDTH = 128
HEIGHT = 64
LOOPTIME = 1.0

matrix = ("hotspot", "toggle", "shutdown", "reboot")

COL = (25, 8) #coloumn gpio pins
ROW = (23, 24) #row gpio pins

for j in range(2):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 0)

for i in range(2):
    GPIO.setup(ROW[i], GPIO.IN)

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

icon_font = ImageFont.truetype(path + 'fonts/icomoon.ttf', 15)
roboto_bold = ImageFont.truetype(path + 'fonts/Roboto-Bold.ttf', 16)
roboto_regular = ImageFont.truetype(path + 'fonts/Roboto-Regular.ttf', 11)
roboto_light = ImageFont.truetype(path + 'fonts/Roboto-Light.ttf', 15)

def animation(name):
    for x in range(1, 51):
        image = Image.open(path + f'/{name}/frame ('+str(x)+').pbm').convert('1')
        oled.image(image)
        oled.show()

def time_page(semi_colon):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    current_time = datetime.now()
    if semi_colon:
        disp = current_time.strftime("%I:%M")
    else:
        disp = current_time.strftime("%I %M")
    draw.text((2, 14), disp,  font=roboto_regular.font_variant(size=40), fill=255)
    draw.text((105, 38), current_time.strftime("%p"), font=roboto_bold, fill=255)
    dates = current_time.strftime("%d/%m %a")
    draw.text((35, 52), dates,  font=roboto_light.font_variant(size=12), fill=255)

def stats():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    IP = str(subprocess.check_output("hostname -I | cut -d\' \' -f1 | head --bytes -1", shell=True), 'utf-8')
    CPU = str(subprocess.check_output("top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'", shell=True), 'utf-8')
    MemUsage = str(subprocess.check_output("free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'", shell=True), 'utf-8')
    Disk = str(subprocess.check_output("df -h | awk '$NF==\"/mnt/hdd\"{printf \"%sB/%sB ~ %s\", $3,$2,$5}'", shell=True), 'utf-8')
    Temperature = str(subprocess.check_output("vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1", shell=True), 'utf-8')
    draw.text((0, 18),    "\ue917",  font=icon_font, fill=255)
    draw.text((16, 18), IP,  font=roboto_light, fill=255)
    draw.text((0, 35),    "\ue92a",  font=icon_font, fill=255)
    draw.text((17, 35), Temperature,  font=roboto_light.font_variant(size=11), fill=255)
    draw.text((65, 35), "\ue922",  font=icon_font, fill=255)
    draw.text((85, 35), MemUsage,  font=roboto_light.font_variant(size=11), fill=255)
    draw.text((0, 47), "\ue924",  font=icon_font, fill=255)
    draw.text((0, 51), "\ue924",  font=icon_font, fill=255)
    draw.text((17, 51), Disk,  font=roboto_light.font_variant(size=11), fill=255)

def clean():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

def notification():
    Under_voltage = subprocess.check_output('vcgencmd get_throttled', shell=True)
    txt = str(Under_voltage, 'utf8').strip().split("=")
    if txt[1] == "0x0":
        pass
    else:
        draw.text((97, 0), "\ue927",  font=icon_font, fill=255)

    Temp = subprocess.check_output("vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1", shell=True)
    txt = float(str(Temp, 'utf8')[:-2])
    if txt <= 50:
        draw.text((113, 0), "\ue908",  font=icon_font, fill=255)
    elif txt <= 70:
        draw.text((113, 0), "\ue923",  font=icon_font, fill=255)
    else:
        draw.text((113, 0), "\ue91f",  font=icon_font, fill=255)


def wait_screen( cmd2, cmd1 = "Want to"):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((4, 18), cmd1,  font=roboto_light, fill=255)
    draw.text((4, 38), str(cmd2 + " ?").upper(),  font=roboto_light, fill=255)
    draw.text((22, 43), "\ue918",  font=icon_font.font_variant(size=18), fill=255)
    draw.text((91, 43), "\ue913",  font=icon_font.font_variant(size=18), fill=255)


page = 0
wait_shutdown = [False, False]
wait_reboot = [False, False]
wait_hotspot = [False, False, False]


def display():
    global page, wait_shutdown, wait_reboot, wait_hotspot
    semi_colon = True
    while True:
        if wait_shutdown[0]:
            wait_screen("shutdown")
            if wait_shutdown[1]:
                animation("animation1")
                time.sleep(0.3)
                wait_shutdown = [False, False]
                
        elif wait_reboot[0]:
            wait_screen("reboot")
            if wait_reboot[1]:
                animation("animation2")
                time.sleep(0.3)
                wait_reboot = [False, False]                
        
        elif wait_hotspot[0]:
            wait_screen("hotspot", "Need")
            if wait_hotspot[1]:
                animation("mark_boot")
                time.sleep(0.3)
                wait_hotsopt = [False, False, False]
            elif wait_hotspot[2]:
                #animation("animation2")
                time.sleep(0.3)
                wait_hotsopt = [False, False, False]

        elif page == 0:
            time_page(semi_colon)
            notification()
        elif page == 1:    
            stats()
            notification()
        elif page == 2:
            clean()
        else:
            page = 0

        semi_colon = not semi_colon
        oled.image(image)
        oled.show()
        time.sleep(LOOPTIME)

def button():
    global page, wait_shutdown, wait_reboot, wait_hotspot
    while True:
        for j in range(2):
            GPIO.output(COL[j], 1)
            for i in range(2):
                if GPIO.input(ROW[i]) == 1:
                    m = ((i * 2) + j)
                    if wait_shutdown[0]: #logic maybe wrong
                        if matrix[m] == "shutdown" or "reboot":
                            wait_shutdown[1] = True
                        elif matrix[m] == "hotspot" or "toggle":
                            wait_shutdown = [False, False]
                    
                    if wait_reboot[0]:#logic maybe wrong
                        if matrix[m] == "shutdown" or "reboot":
                            wait_reboot[1] = True
                        elif matrix[m] == "hotspot" or "toggle": 
                            wait_reboot = [False, False]
                    
                    if wait_hotspot[0]:#logic maybe wrong
                        if matrix[m] == "shutdown" or "reboot":
                            wait_hotspot[1] = True
                        elif matrix[m] == "hotspot" or "toggle": 
                            wait_hotspot[2] = True

                    if matrix[m]  == "toggle":
                        page = page + 1
                    elif matrix[m] == "shutdown":
                        wait_shutdown[0] = True
                    elif matrix[m] == "reboot":
                        wait_reboot[0] = True
                    elif matrix[m] == "hotsopt":
                        wait_hotspot[0] = True
                    else: pass
                      
                    time.sleep(0.1)

            GPIO.output(COL[j], 0)

t1 = Thread(target = button)
t2 = Thread(target = display)

t1.start()
t2.start()

t1.join
t2.join
