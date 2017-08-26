import requests
import time
import datetime

def internet_on():
    try:
        r = requests.get('http://77.88.55.50')
        return True
    except requests.exceptions.ConnectionError as err: 
        return False

f = open("network_interrupts.log",'a')
for attempt in range(72000):
    if (internet_on() == False):
        start_time = datetime.datetime.now()
        print("Interruption start: " + str(start_time))
        f.write("Interruption start: " + str(start_time) + "\n")
        while (internet_on() == False):
            time.sleep(0.2)
        end_time = datetime.datetime.now()
        print("Interruption end: " + str(end_time))
        f.write("Interruption end: " + str(end_time) + "\n")
        duration = end_time - start_time
        print("Duration: " + str(duration.total_seconds()))
        f.write("Duration: " + str(duration.total_seconds()) + "\n")
    time.sleep(1)
