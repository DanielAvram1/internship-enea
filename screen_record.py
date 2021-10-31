import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import time
import config as c

class ScreenRecorder:

    def __init__(self, logger):
        self.logger = logger
        self.SCREEN_SIZE = self.__get_size()

    def __get_size(self):
        img = pyautogui.screenshot()
        frame = np.array(img)
        return (frame.shape[1], frame.shape[0])


    def __get_screenshots(self, duration):
        img_list = []
        t_end = time.time() + duration
        self.logger.write('info', 'starting recording video...')
        while time.time() < t_end:
            img = ImageGrab.grab(bbox=(0, 0, self.SCREEN_SIZE[0], self.SCREEN_SIZE[1]))
            img_list.append(img)
        self.logger.write('info', 'ended recording video...')
        return img_list

    def record_video(self, duration):
        img_list = self.__get_screenshots(duration)
        FPS = len(img_list)/duration
        
        self.logger.write('info',f'Screenshot taken: {len(img_list)}')
        self.logger.write('info', 'fps of the video: {FPS}')

        out = cv2.VideoWriter(c.MOV_OUTPUT_FILENAME,cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, self.SCREEN_SIZE)
        for img in img_list:
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)

        out.release()

    
if __name__ == '__main__':
    ScreenRecorder().record_video(10)