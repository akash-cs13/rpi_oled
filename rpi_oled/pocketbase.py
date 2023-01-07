import time
import subprocess
import requests
import json
#from tqdm import tqdm

# 157GB/1.4TB ~ 12% 9.5GB/30GB ~ 34%
# print(str(Disk1, 'utf8'), str(Disk2, 'utf8'))
#print(float(str(Cpu, 'utf8')), float(str(Temperature, 'utf8')[:-2]), str(MemUsage, 'utf8'), str(Disk1, 'utf8'), str(Disk2, 'utf8'))



#for i in tqdm(range(1000)):
#    id = str(i)
#    cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
#    Cpu = subprocess.check_output(cmd, shell=True)
#    cmd = "free -m | awk 'NR==2{printf \"%s/%s ~ %.2f%%\", $3,$2,$3*100/$2 }'" 
#    MemUsage = subprocess.check_output(cmd, shell=True)
#    cmd = "df -h | awk '$NF==\"/mnt/hdd\"{printf \"%sB/%sB ~ %s\", $3,$2,$5}'" df -h | awk '$NF==\"/mnt/hdd\"{printf \"%sB/%sB ~ %s\", $3,$2,$5}'
#    Disk1 = subprocess.check_output(cmd, shell=True)
#    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
#    Temperature = subprocess.check_output(cmd, shell=True)
#    cmd = "df -h | awk '$NF==\"/\"{printf \"%sB/%sB ~ %s\", $3,$2,$5}'"
#    Disk2 = subprocess.check_output(cmd, shell=True)
#    data = {"id": id.zfill(15), "cpu_temperature": float(str(Temperature, 'utf8')[:-2]), "cpu_usage": float(str(
#        Cpu, 'utf8')), "disk1": str(Disk1, 'utf8'), "disk2": str(Disk2, 'utf8'), "ram_usage": str(MemUsage, 'utf8')}
#    r = requests.post(
#        "http://192.168.0.168:4900/api/collections/rpi_stats/records", json=data)
#    time.sleep(1.0)

http = "http://192.168.0.168:4900"
latest_id = 1
r = requests.patch(http + "/api/collections/settings/records/000000000000001", json={"latest_id": latest_id})

