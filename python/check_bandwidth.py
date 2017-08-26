from YaDiskClient.YaDiskClient import YaDisk
import psutil
import random
import time
from multiprocessing import Process, Queue
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

LOGIN = "dummy"
PASSWORD = "dummy"

PLOTLY_USERNAME = "dummy"
PLOTLY_API_KEY = "dummy"

def download(src, dst):
    disk = YaDisk(LOGIN, PASSWORD)
    disk.download(src, dst)

def print_counters(q):
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

if __name__ == '__main__':
    q = Queue()
    p = Process(target=print_counters, args=(q,))
    p.start()
    time.sleep(5)
    download("test/file_rand", "C:/Users/notmoor/Desktop/file_rand(downloaded)")
    time.sleep(5)
    q.put("finish")
    p.join()
    bytes_per_second = q.get()
    dots = []
    for dot in range(len(bytes_per_second)):
        dots.append(dot)

    plotly.tools.set_credentials_file(username='PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)

    trace = go.Scatter(
        x = dots,
        y = bytes_per_second
    )
    data = [trace]

    py.plot(data, filename='network_bandwidth')