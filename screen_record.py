import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import time

def get_size():
    img = pyautogui.screenshot()
    frame = np.array(img)
    return (frame.shape[1], frame.shape[0])

SCREEN_SIZE = get_size()




def get_screenshots(duration):
    img_list = []
    t_end = time.time() + duration
    while time.time() < t_end:
        #img = pyautogui.screenshot(region=(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
        img = ImageGrab.grab(bbox=(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
        img_list.append(img)
    return img_list
# display screen resolution, get it from your OS settings

def record_video(duration):
    SCREEN_SIZE = get_size()
    img_list = get_screenshots(duration)
    FPS = len(img_list)/duration
    out = cv2.VideoWriter('recording_video_only.mov',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, SCREEN_SIZE)
    print('Screenshot taken: ', len(img_list))
    print('fps of the video: ', FPS)
    for img in img_list:
        frame = np.array(img)
        # convert colors from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # write the frame
        out.write(frame)
    
    out.release()

if __name__ == '__main__':
    record_video(10)