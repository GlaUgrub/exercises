from YaDiskClient.YaDiskClient import YaDisk
import psutil
import random
import time
from multiprocessing import Process, Queue
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import datetime
import sys

LOGIN = "dummy"
PASSWORD = "dummy"

PLOTLY_USERNAME = "dummy"
PLOTLY_API_KEY = "dummy"

def download(src, dst):
    disk = YaDisk(LOGIN, PASSWORD)
    disk.download(src, dst)

def print_counters(q):
    full_range = 100
    max_value = 1e7
    padding = 20
    bytes_per_second = []
    while True:
        if (q.empty() == False):
            q.get()
            q.put(bytes_per_second)
            return
        start = psutil.net_io_counters()
        time.sleep(1)
        end = psutil.net_io_counters()
        diff = end[1] - start[1]
        bytes_per_second.append(diff)
        num_chars = int(full_range * diff / max_value)
        zero_mbs = "0MB/s"
        half_mbs = str(int(max_value/2/1e6)) + "MB/s"
        full_mbs = str(int(max_value/1e6)) + "MB/s"
        footer_first = "[" + zero_mbs + " "*(full_range//2 - len(zero_mbs)) + "|" + half_mbs
        footer_second = " "*(full_range - len(footer_first) + 1) + "]" + full_mbs + "\r"
        to_print = "[" + "*"*num_chars + " "*(full_range - num_chars) + "]" + " "*padding + "\n"
        footer = footer_first + footer_second
        sys.stdout.write(to_print)
        sys.stdout.write(footer)
        sys.stdout.flush()
        # print("[" + "*"*num_chars + " "*num_chars_left + "]")
        # print("[" + "*"*num_chars + " "*num_chars_left + "]")

def duration(start_time):
    cur_time = datetime.datetime.now()
    duration = cur_time - start_time
    return duration.total_seconds()

if __name__ == '__main__':
    q = Queue()
    p = Process(target=print_counters, args=(q,))
    p.start()
    time.sleep(5)
    # start_time = datetime.datetime.now()
    # while duration(start_time) < 300:
    download("test/file_rand", "C:/Users/notmoor/Desktop/file_rand(downloaded)")
    time.sleep(5)
    q.put("finish")
    p.join()
    bytes_per_second = q.get()

    dots = []
    for dot in range(len(bytes_per_second)):
        dots.append(dot)

    plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)

    trace = go.Scatter(
        x = dots,
        y = bytes_per_second
    )
    data = [trace]

    py.plot(data, filename='network_bandwidth')