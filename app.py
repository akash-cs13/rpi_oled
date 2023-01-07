import os
import time
import board
import digitalio
import subprocess
import requests
import json
import adafruit_ssd1306
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

path = os.path.dirname(__file__) + '/'
http = "http://127.0.0.1:4900"
#f = open(path + "configure.json")
#data = json.load(f)
#f.close()


oled_reset = digitalio.DigitalInOut(board.D4)
WIDTH = 128
HEIGHT = 64
LOOPTIME = 15.0


i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c, reset=oled_reset)
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

def time_page():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    current_time = datetime.now()
    draw.text((2, 14), current_time.strftime("%I:%M"),  font=roboto_regular.font_variant(size=40), fill=255)
    draw.text((105, 38), current_time.strftime("%p"), font=roboto_bold, fill=255)
    dates = current_time.strftime("%d/%m %a")
    draw.text((35, 52), dates,  font=roboto_light.font_variant(size=12), fill=255)

def stats(CPU, MemUsage, Disk1, Temperature):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    IP = str(subprocess.check_output("hostname -I | cut -d\' \' -f1 | head --bytes -1", shell=True), 'utf-8')
    draw.text((0, 18),    "\ue917",  font=icon_font, fill=255)
    draw.text((16, 18), IP,  font=roboto_light, fill=255)
    draw.text((0, 35),    "\ue92a",  font=icon_font, fill=255)
    draw.text((17, 35), Temperature,  font=roboto_light.font_variant(size=11), fill=255)
    draw.text((65, 35), "\ue922",  font=icon_font, fill=255)
    draw.text((85, 35), MemUsage,  font=roboto_light.font_variant(size=11), fill=255)
    draw.text((0, 47), "\ue924",  font=icon_font, fill=255)
    draw.text((0, 51), "\ue924",  font=icon_font, fill=255)
    draw.text((17, 51), Disk1,  font=roboto_light.font_variant(size=11), fill=255)

def clean():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

def notification1(Temperature):
    Under_voltage = str(subprocess.check_output('vcgencmd get_throttled', shell=True), 'utf8').strip().split("=")
    if Under_voltage[1] == "0x0":
        pass
    else:
        draw.text((97, 0), "\ue927",  font=icon_font, fill=255)

    txt = float(Temperature[:-2])
    if txt <= 50:
        draw.text((113, 0), "\ue908",  font=icon_font, fill=255)
    elif txt <= 70:
        draw.text((113, 0), "\ue923",  font=icon_font, fill=255)
    else:
        draw.text((113, 0), "\ue91f",  font=icon_font, fill=255)

def notification():
    Under_voltage = subprocess.check_output('vcgencmd get_throttled', shell=True)
    txt = str(Under_voltage, 'utf8').strip().split("=")
    if txt[1] == "0x0":
        pass
    else:
        draw.text((113, 0), "\ue927",  font=icon_font, fill=255)



def pocketbase(i, CPU, MemUsage, Disk1, Disk2, Temperature):
    r = requests.patch(http + "/api/collections/settings/records/000000000000001", json={"latest_id": i})
    id = str(i)
    data = {"id": id.zfill(15), "cpu_temperature": Temperature, "cpu_usage": 
        CPU, "disk1": Disk1, "disk2": Disk2, "ram_usage": MemUsage}
    r = requests.post(http + "/api/collections/rpi_stats/records", json=data)
    

def pbinit():
    r = requests.get(http + "/api/collections/settings/records")
    settings = json.loads(r.text)
    page = settings["items"][0]["page"]
    latest_id = settings["items"][0]["latest_id"]
    return (page,latest_id)



page , latest_id = pbinit()   
while True:
    latest_id = latest_id + 1 
    CPU = str(subprocess.check_output("top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'", shell=True), 'utf-8')
    MemUsage = str(subprocess.check_output("free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'", shell=True), 'utf-8')
    Disk1 = str(subprocess.check_output("df -h | awk '$NF==\"/mnt/hdd\"{printf \"%sB/%sB ~ %s\", $3,$2,$5}'", shell=True), 'utf-8')
    Disk2 = str(subprocess.check_output("df -h | awk '$NF==\"/\"{printf \"%sB/%sB ~ %s\", $3,$2,$5}'", shell=True), 'utf-8')
    Temperature = str(subprocess.check_output("vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1", shell=True), 'utf-8')

    if page == 1:
        stats(CPU, MemUsage, Disk1, Temperature)
        notification()
    elif page == 2:
        time_page()
        notification1(Temperature)
    else: 
        clean()

    pocketbase(latest_id, CPU, MemUsage, Disk1, Disk2, Temperature) 
    page , latest_id = pbinit()
    
    oled.image(image)
    oled.show()
    time.sleep(LOOPTIME)

