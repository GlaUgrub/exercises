import autopy
import PIL
from PIL import ImageDraw
import pytesseract
import pyscreenshot
import os
from tkinter import *
import yaml
import wx
import time
from multiprocessing import Process, Queue

rows = { 'price': 0, 'time': 1, 'sign': 2, 'reload': 3}

coords = {
    'price': [],
    'time': [],
    'sign': [],
    'reload': []
}

#####################################################################
# functions to work with yaml file                                  #
#####################################################################

def load_from_yaml(file):
    with open(file, 'r') as stream:
        return yaml.load(stream)
        
def save_to_yaml(file, data):
    with open(file, 'w') as stream:
        yaml.dump(data, stream, default_flow_style=False)

#####################################################################
# functions to get coordinats from GUI                              #
#####################################################################
def get_from_entries(dst, src):
    for idx in range(len(src)):
        dst[idx] = int(src[idx].get())

def get_coords():
    for obj in coords:
        r = rows[obj] + 1
        get_from_entries(coords[obj], entries[r][1:])

def get_and_save_coords():
    get_coords()
    file_yaml = "coordinates.yaml"
    save_to_yaml(file_yaml, coords)

#####################################################################
# functions to draw rectangls cooresponding to coordinates          #
#####################################################################

def draw_rect(dc, rect, color):
    dc.StartDrawingOnTop()
    dc.Pen = wx.Pen(color)
    dc.SetBrush(wx.Brush((0,0,0), wx.BRUSHSTYLE_TRANSPARENT))
    dc.DrawRectangle(rect[0], rect[1], rect[2], rect[3])

def draw_coords():
    colors = {
        'red': '#FF0000',
        'green': "#00FF00",
        'blue': "#0000FF",
        'yellow': "#FFFF00"
    }

    app = wx.App(False)
    s = wx.ScreenDC()
    draw_rect(s, coords['price'], colors['red'])
    draw_rect(s, coords['time'], colors['green'])
    draw_rect(s, coords['sign'], colors['blue'])

#####################################################################
# functions to set coordinats to GUI                                #
#####################################################################

def set_to_entries(dst, src):
    for idx in range(len(src)):
        dst[idx].delete('0', 'end')
        dst[idx].insert('0', str(src[idx]))
    
def set_coords(data):
    for obj in coords:
        r = rows[obj] + 1
        set_to_entries(entries[r][1:], coords[obj])


#####################################################################
# function to form TKinter GUI                                      #
#####################################################################

def form_gui():
    layout = [
        [ ['l', '     '],   ['l', 'X'], ['l', 'Y'], ['l', 'W'], ['l', 'H']  ],
        [ ['l', 'price'],    'e',        'e',        'e',        'e'        ],
        [ ['l', 'time'],     'e',        'e',        'e',        'e'        ],
        [ ['l', 'sign'],     'e',        'e',        'e',        'e'        ],
        [ ['l', 'reload'],   'e',        'e',        'n',        'n'        ],
        [ ['b', 'Save', get_and_save_coords], ['b', 'Draw', draw_coords], ['b', 'Start', start_execution], ['b', 'Stop', finish_execution],        'n'        ]
    ]

    for r in range(len(layout)):
        entries.append([])
        for c in range(len(layout[0])):
            field_type = layout[r][c][0]
            if (field_type != 'n'):
                if (field_type == 'l'): # Layout
                    entries[r].append(Label(window, text=layout[r][c][1]))
                if (field_type == 'e'): # Entry
                    entries[r].append(Entry(window, width=8))
                if (field_type == 'b'): # Button
                    entries[r].append(Button(window, text=layout[r][c][1], width=6, command=layout[r][c][2]))
                entries[r][c].grid(row=r, column=c)

#####################################################################
# functions to work with screenshots                                #
#####################################################################

# form name of the screenshot: "screen_<date>_<time>_<w>x<h>.png"

def form_date(timestamp):
    return ".".join([str(timestamp.tm_mday), str(timestamp.tm_mon)])

def form_time(timestamp):
    return "-".join([str(timestamp.tm_hour), str(timestamp.tm_min), str(timestamp.tm_sec)])

def form_size(size):
    return "x".join([str(size[0]), str(size[1])])

def get_screenshot_filename(timestamp, size):
    filename = "_".join(['screen', form_date(timestamp), form_time(timestamp), form_size(size)])
    filename = ".".join([filename, 'png'])
    return filename

# make and save screenshot

def get_box(roi):
    return (roi[0], roi[1], roi[0] + roi[2], roi[1] + roi[3])

def save_screenshot(img, timestamp, folder):
    width, height = img.size
    filename = get_screenshot_filename(timestamp, [width, height])
    filename = os.path.join(folder, filename)
    print("[LOG] Save screenshot to file: " + filename)
    img.save(filename)
    return filename

def highlight_roi(img, roi):
    draw = ImageDraw.Draw(img)
    draw.rectangle(get_box(roi), outline='red')

def make_screenshot_roi(roi):
    timestamp = time.localtime()
    print("[LOG] Make screenshot: size " + str(roi[2]) + "x" + str(roi[3]) + ", time " + form_time(timestamp))
    img = pyscreenshot.grab(bbox = get_box(roi))
    return img, timestamp

def make_screenshot():
    roi = [0, 0, 1920, 1200]
    return make_screenshot_roi(roi)

def recognize_image(img):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    return pytesseract.image_to_string(img)

#####################################################################
# functions for logging                                             #
#####################################################################

def get_log_filename(timestamp):
    filename = "_".join(['log', form_date(timestamp), form_time(timestamp)])
    filename = ".".join([filename, 'txt'])
    return filename

def create_log_file():
    folder = 'log'
    filename = get_log_filename(time.localtime())
    filename = os.path.join(folder, filename)
    f = open(filename,'w')
    return f

#####################################################################
# main asynchronous loop                                            #
#####################################################################

def listen(q):
    while True:
        if (q.empty() == False):
            return q.get()
        time.sleep(0.1)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def move_and_click(place):
    x,y = place[0], place[1]
    autopy.mouse.smooth_move(x, y)
    autopy.mouse.click(autopy.mouse.Button.RIGHT)

def get_roi(img, roi):
    box = get_box(roi)
    return img.crop(box)

def process_price(img, timestamp, coordinates, log_file):
    roi = coordinates['price']
    price_roi = get_roi(img, roi)
    content = recognize_image(price_roi)
    if (is_number(content)):
        print("[LOG] Found number " + content + " at location " + str(roi))
        # if (float(content) > 1000):
            # move_and_click([1900, 1100])
        # else:
            # move_and_click([100, 100])
    else:
        print("[LOG]" + content + " at location " + str(roi))
        highlight_roi(img, roi)
        filename = save_screenshot(img, timestamp, 'log')
        log_file.write("No number in \"price\" rectangle - see screenshot " + filename + "\n")

def screenshot_loop(q, coordinates):
    log_file = create_log_file()
    while True:
        screenshot, timestamp = make_screenshot()
        process_price(screenshot, timestamp, coordinates, log_file)
        time.sleep(1)
        if (q.empty() == False):
            message = q.get()
            if (message != 'start'):
                log_file.close()
                return message

def main_loop(q):
    print("[LOG] Enter main_loop()")

    while True:
        signal = listen(q)

        if (signal == 'terminate'):
            print("[LOG] Exit main_loop()")
            return

        if (signal == 'start'):
            print("[LOG] Start making screenshots")
            coordinates = q.get()
            print("      coordinates are: " + str(coordinates))
            stop_signal = screenshot_loop(q, coordinates)
            if (stop_signal == 'terminate'):
                print("[LOG] Exit main_loop()")
                return
            print("[LOG] Stop making screenshots")


#####################################################################
# main TKinter loop                                                 #
#####################################################################

def start_execution():
    q.put('start')
    q.put(coords)
    return

def finish_execution():
    q.put('stop')
    return

if __name__ == '__main__':
    print("[LOG] Start")

    # start async process
    print("[LOG] Run async process ")
    q = Queue()
    p_main_loop = Process(target=main_loop, args=(q,))
    p_main_loop.start()

    # main TKinter loop -- START
    window = Tk()
    window.geometry("300x150")

    entries = []
    print("[LOG] Draw GUI")
    form_gui()

    print("[LOG] Load coordinates from file")
    file_yaml = "coordinates.yaml"
    coords = load_from_yaml(file_yaml)
    set_coords(coords)
    print("[LOG] Loaded coordinates: " + str(coords))

    window.mainloop()
    # main TKinter loop -- END

    print("[LOG] Terminate async process ")
    q.put('terminate')
    p_main_loop.join()
    print("[LOG] End")

#coords = [400,400]
#move_and_click(coords)
    