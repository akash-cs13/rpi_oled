import subprocess
import os

print(" 1: Shutdown\n 2: Reboot\n 3: Hotsopt")
cmd = int(input("Choose command:"))

if cmd == 1:
    print("Shutting down.....")
    os.system("sudo shutdown now")

elif cmd == 2:
    print("Rebootig.....")
    os.system("sudo", "reboot", "now")

elif cmd == 3:
    wlan = str(subprocess.check_output("ifconfig | grep -o \"wlan0\"",shell=True), 'utf-8')
    if wlan == "wlan0":
        print("Hotspot off.....")
        os.system("sudo nmcli con down Mark ifname wlan0")
        os.system("sudo nmcli radio wifi off")
        os.system("sudo ifconfig wlan0 down")
        
    else: 
        print("Hotsopt on........")
        os.system("sudo rfkill unblock wifi; sudo rfkill unblock all")
        os.system("sudo ifconfig wlan0 up")
        os.system("sudo nmcli radio wifi on")
        os.system("sudo nmcli con up Mark ifname wlan0")