import time
import board
import busio
import digitalio
import gpiozero
import os


from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess
from gpiozero import CPUTemperature


path = os.path.dirname(__file__) + '/'
# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Display Refresh
LOOPTIME = 1.0

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(
    WIDTH, HEIGHT, i2c, addr=0x3c, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = oled.width
height = oled.height

# boot animation
# for x in range(1, 51):
#    image = Image.open('./mark_boot/frame ('+str(x)+').pbm').convert('1')
#    oled.image(image)
#    oled.show()


image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

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
    cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
    IP = subprocess.check_output(cmd, shell=True)
    cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/mnt/hdd\"{printf \"%sB/%sB ~ %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)
    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
    Temperature = subprocess.check_output(cmd, shell=True)
    draw.text((x, top+20),    "\ue917",  font=icon_font, fill=255)
    draw.text((x+16, top+20), str(IP, 'utf-8'),  font=font3, fill=255)
    draw.text((x, top+37),    "\ue92a",  font=icon_font, fill=255)
    draw.text((x+17, top+37), str(Temperature, 'utf-8'),  font=font, fill=255)
    draw.text((x+65, top+37), "\ue922",  font=icon_font, fill=255)
    draw.text((x+85, top+37), str(MemUsage, 'utf-8'),  font=font, fill=255)
    draw.text((x, top+49), "\ue924",  font=icon_font, fill=255)
    draw.text((x, top+53), "\ue924",  font=icon_font, fill=255)
    draw.text((x+17, top+53), str(Disk, 'utf-8'),  font=font, fill=255)


def clean():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)


def notification():

    cmd = 'vcgencmd get_throttled'
    Under_voltage = subprocess.check_output(cmd, shell=True)
    txt = str(Under_voltage, 'utf8').strip().split("=")
    if txt[1] == "0x0":
        pass
    else:
        draw.text((x+97, top+2), "\ue927",  font=icon_font, fill=255)

    cmd = cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
    Temperature = subprocess.check_output(cmd, shell=True)
    txt = float(str(Temperature, 'utf8')[:-2])
    if txt <= 45:
        draw.text((x+113, top+2), "\ue908",  font=icon_font, fill=255)
    elif txt <= 55:
        draw.text((x+113, top+2), "\ue923",  font=icon_font, fill=255)
    else:
        draw.text((x+113, top+2), "\ue91f",  font=icon_font, fill=255)


semi_colon = True
# while True:
time_page(semi_colon)
stats()
notification()
# clean()
semi_colon = not semi_colon
oled.image(image)
oled.show()
time.sleep(LOOPTIME)
