import os
import time
import board
import digitalio
import subprocess
import json
import adafruit_ssd1306
import RPi.GPIO as GPIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


path = os.path.dirname(__file__) + '/'

oled_reset = digitalio.DigitalInOut(board.D4)
WIDTH = 128
HEIGHT = 64
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

icon_font = ImageFont.truetype(path + 'fonts/icomoon.ttf', 15)
roboto_bold = ImageFont.truetype(path + 'fonts/Roboto-Bold.ttf', 16)
roboto_regular = ImageFont.truetype(path + 'fonts/Roboto-Regular.ttf', 11)
roboto_light = ImageFont.truetype(path + 'fonts/Roboto-Light.ttf', 15)

def wait_screen( cmd2, cmd1 = "Want to"):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((4, 18), cmd1,  font=roboto_light, fill=255)
    draw.text((4, 38), str(cmd2 + " ?").upper(),  font=roboto_light, fill=255)
    draw.text((22, 43), "\ue918",  font=icon_font.font_variant(size=18), fill=255)
    draw.text((91, 43), "\ue913",  font=icon_font.font_variant(size=18), fill=255)

wait_screen("Shutdown")
oled.image(image)
oled.show()
time.sleep(LOOPTIME)