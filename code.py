import subprocess
import threading
import time
from mss import mss
import cv2
from PIL import Image
import numpy as np
import pydirectinput
import pyautogui
import pygetwindow as gw
# mon = {'top': 0, 'left':0, 'width':1920, 'height':1080}
cnt = [0]
try:
    my_window = gw.getWindowsWithTitle("3D Pinball for Windows - Space Cadet")[0]
except:
    try:
        print("starting pinball")
        subprocess.Popen(fr'"C:\Program Files (x86)\Pinball\pinball.exe"')
        print("pinball started")
        time.sleep(1)
        my_window = gw.getWindowsWithTitle("3D Pinball for Windows - Space Cadet")[0]
    except:
        print("please install Pinball on C drive\nthe installation file is in https://github.com/TRTR5TRTR/python-Pinball-bot")
        quit()

sct = mss()
l_contours = []
r_contours = []
def screen_left():
    while 1:
        mon = {'top': my_window.topleft[1]+365, 'left': my_window.topleft[0]+130, 'width': my_window.size[0]-560,'height': my_window.size[1]-365}
        # mon = {'top': my_window.topleft[1], 'left': my_window.topleft[0], 'width': my_window.size[0],'height': my_window.size[1]}
        sct_img = sct.grab(mon)
        frame = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        sct_img1 = sct.grab(mon)
        frame1 = Image.frombytes('RGB', (sct_img1.size.width, sct_img1.size.height), sct_img1.rgb)
        frame1 = cv2.cvtColor(np.array(frame1), cv2.COLOR_RGB2BGR)
        diff = cv2.absdiff(frame1, frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
        cv2.imshow("screen_left", frame1)
        global l_contours
        l_contours = contours
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def screen_right():
    while 1:
        mon = {'top': my_window.topleft[1]+365, 'left': my_window.topleft[0]+195, 'width': my_window.size[0]-560,'height': my_window.size[1]-365}
        # mon = {'top': my_window.topleft[1], 'left': my_window.topleft[0], 'width': my_window.size[0],'height': my_window.size[1]}
        sct_img = sct.grab(mon)
        frame = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        sct_img1 = sct.grab(mon)
        frame1 = Image.frombytes('RGB', (sct_img1.size.width, sct_img1.size.height), sct_img1.rgb)
        frame1 = cv2.cvtColor(np.array(frame1), cv2.COLOR_RGB2BGR)
        diff = cv2.absdiff(frame1, frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
        cv2.imshow("screen_right", frame1)
        global r_contours
        r_contours = contours
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
def click():
    while 1:
        start = time.time()
        flag = False
        if gw.getActiveWindowTitle() == "3D Pinball for Windows - Space Cadet":
            for c in l_contours:
            # if cv2.contourArea(c)%2==0:
                pydirectinput.keyDown("z")
                pyautogui.sleep(0.02)
                pydirectinput.keyUp("z")
            # else:
            for c in r_contours:
                pydirectinput.keyDown("/")
                pyautogui.sleep(0.02)
                pydirectinput.keyUp("/")
            if l_contours or r_contours:
                flag = True
                current = time.time()
        if flag and current - start < 0.28:
            time.sleep(0.5)
def l_click():
    while 1:
        start = time.time()
        flag = False
        if gw.getActiveWindowTitle() == "3D Pinball for Windows - Space Cadet":
            for c in l_contours:
                pydirectinput.keyDown("z")
                pyautogui.sleep(0.02)
                pydirectinput.keyUp("z")
            if l_contours:
                flag = True
                current = time.time()
        if flag and current - start < 0.28:
            time.sleep(0.5)
def r_click():
    while 1:
        start = time.time()
        flag = False
        if gw.getActiveWindowTitle() == "3D Pinball for Windows - Space Cadet":
            for c in r_contours:
                pydirectinput.keyDown("/")
                pyautogui.sleep(0.02)
                pydirectinput.keyUp("/")
            if r_contours:
                flag = True
                current = time.time()
        if flag and current - start < 0.255:
            print(current-start)
            time.sleep(0.5)
def check_start():
    while 1:
        mon = {'top': my_window.topleft[1], 'left': my_window.topleft[0], 'width': my_window.size[0],'height': my_window.size[1]}
        sct_img = sct.grab(mon)
        if sct_img.pixel(328, 420)==(56, 56, 56):
            print("starting")
            pydirectinput.keyDown(" ")
            pyautogui.sleep(1)
            pydirectinput.keyUp(" ")

t1 = threading.Thread(target=screen_left)
t2 = threading.Thread(target=screen_right)
# t3 = threading.Thread(target=click)
t4 = threading.Thread(target=check_start)
t5 = threading.Thread(target=r_click)
t6 = threading.Thread(target=l_click)

t1.start()
t2.start()
# t3.start()
t4.start()
t5.start()
t6.start()
time.sleep(0.2)
my_window.activate()
t1.join()
t2.join()
# t3.join()
t4.join()
t5.join()
t6.join()
