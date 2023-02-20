import os
import time
for i in os.listdir("/root/site/logs/"):
    if float(time.time())-float(os.path.getctime("/root/site/logs/"+str(i)))>259200:
        os.remove("/root/site/logs/"+str(i))
        print("Файл "+str(i)+" удален")
    