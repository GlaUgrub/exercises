from YaDiskClient.YaDiskClient import YaDisk
import psutil
import random
import time
from multiprocessing import Process, Queue
# import plotly
# import plotly.plotly as py
# import plotly.graph_objs as go
import datetime
import sys

LOGIN = "dummy"
PASSWORD = "dummy"

PLOTLY_USERNAME = "dummy"
PLOTLY_API_KEY = "dummy"

def download(q, src, dst):
    disk = YaDisk(LOGIN, PASSWORD)
    q.put("started")
    disk.download(src, dst)
    q.put("finished")

def calc_average(list_numbers, window):
    sublist = list_numbers[-window:]
    ave = float(sum(sublist)) / max(len(sublist), 1)
    return ave

def print_bandwidth(list_megabytes_per_sec):
    FULL_RANGE = 100
    MAX_VALUE_BYTES = 1e7
    MAX_VALUE_MB = int(MAX_VALUE_BYTES/1e6)
    PADDING = 90
    cur_value = list_megabytes_per_sec[len(list_megabytes_per_sec) - 1]
    num_chars = int(FULL_RANGE * cur_value / MAX_VALUE_BYTES)
    footer_first = "[0 MB/s    |1        |2        |3        |4        |5        |6        |7        |8        |9        ]10 MB/s"
    average = str(calc_average((list_megabytes_per_sec), len(list_megabytes_per_sec)) / 1e6)
    average = average[:3]
    max_bandwidth = str(max(list_megabytes_per_sec) / 1e6)
    max_bandwidth = max_bandwidth[:3]
    min_bandwidth = str(min(list_megabytes_per_sec) / 1e6)
    min_bandwidth = min_bandwidth[:3]
    downloaded = str(sum(list_megabytes_per_sec) / 1e6)
    downloaded = downloaded[:4]
    footer_last = " -- Average: " + average + " MB/s -- Min: "+ min_bandwidth + " MB/s -- Max: "+ max_bandwidth + " MB/s -- Downloaded: " + downloaded + " MBs\r"
    to_print = "[" + "*"*num_chars + " "*(FULL_RANGE - num_chars) + "]" + " "*PADDING + "\n"
    footer = footer_first + footer_last
    sys.stdout.write(to_print)
    sys.stdout.write(footer)
    sys.stdout.flush()

def calc_counters(sec):
    start = psutil.net_io_counters()
    time.sleep(sec)
    end = psutil.net_io_counters()
    diff = end[1] - start[1]
    return diff

def collect_bandwidth(q, is_print):
    bytes_per_second = []
    if q.get() != "started":
        return
    THRESHOLD = 20000
    while True:
        if (q.empty() == False) and (q.get() == "finished"):
            q.put(bytes_per_second)
            return
        bytes_received = calc_counters(1)
        if (len(bytes_per_second) != 0) or (bytes_received > THRESHOLD):
            bytes_per_second.append(bytes_received)
            if is_print:
                print_bandwidth(bytes_per_second)

def duration(start_time):
    cur_time = datetime.datetime.now()
    duration = cur_time - start_time
    return duration.total_seconds()

if __name__ == '__main__':
    q = Queue()
    p_collect = Process(target=collect_bandwidth, args=(q,True))
    p_collect.start()
    # start_time = datetime.datetime.now()
    # while duration(start_time) < 300:
    p_download = Process(target=download, args=(q,"test/file_rand", "C:/Users/sefremov/Desktop/file_rand(downloaded)"))
    p_download.start()
    p_download.join()
    p_collect.join()
    output = q.get()

    # dots = []
    # for dot in range(len(bytes_per_second)):
        # dots.append(dot)

    # plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)

    # trace = go.Scatter(
        # x = dots,
        # y = bytes_per_second
    # )
    # data = [trace]

    # py.plot(data, filename='network_bandwidth')