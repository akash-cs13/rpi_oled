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


def boot_animation():
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
        WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

    # Clear display.
    oled.fill(0)
    oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
    width = oled.width
    height = oled.height

    for x in range(1, 51):
        image = Image.open(
            path + '/mark_boot/frame ('+str(x)+').pbm').convert('1')
        oled.image(image)
        oled.show()

if __name__ == "__main__":
    boot_animation()
