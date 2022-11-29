import subprocess
print(" 1: Shutdown\n 2: Reboot\n 3: Hotsopt")
cmd = int(input("Choose command:"))

if cmd == 1:
    print("Shutting down.....")
    subprocess.run(["sudo", "shutdown", "now"], shell=True)

elif cmd == 2:
    print("Rebootig.....")
    subprocess.run(["sudo", "reboot", "now"], shell=True)

elif cmd == 3:
    wlan = str(subprocess.check_output("ifconfig | grep -o \"wlan0\"", shell=True), 'utf-8')
    if wlan == "wlan0":
        print("Hotspot off.....")
        subprocess.run(["sudo","nmcli","con","down","Mark","ifname","wlan0"], shell=True)
        subprocess.run(["sudo","nmcli","radio","wifi","off"], shell=True)
        subprocess.run(["sudo","ifconfig","wlan0","down"], shell=True)
        
    else: 
        print("Hotsopt on........")
        subprocess.run(["sudo","rfkill","unblock","wifi;","sudo","rfkill","unblock","all"], shell=True)
        subprocess.run(["sudo","ifconfig","wlan0","up"], shell=True)
        subprocess.run(["sudo","nmcli","radio","wifi","on"], shell=True)
        subprocess.run(["sudo","nmcli","con","up","Mark","ifname","wlan0"], shell=True)