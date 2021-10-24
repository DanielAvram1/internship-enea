from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
from screen_record import record_video
from audio_record import record_audio
from threading import Thread
import os
from datetime import datetime
from random_word import RandomWords
import sys

def search_random(driver, special_word=None):
    search = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#search'))
    )
    search_word = None
    if special_word is not None:
        search_word = special_word
    while search_word is None:
        search_word = RandomWords().get_random_word()
    print(search_word)
    
    search.send_keys(search_word)
    search.send_keys(Keys.RETURN)
    return search_word

def browse_youtube(special_word=None, duration=10):
    try:
        driver = webdriver.Chrome()
        driver.get('https://youtube.com')
        
        thumbnail = None
        search_word = None
        while thumbnail is None:
            search_word = search_random(driver, special_word=special_word)
            thumbnail = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, 'thumbnail'))
            )
            special_word = None

        while driver.current_url != 'https://www.youtube.com/results?search_query='+search_word.replace(' ', '+'):
            pass
        time.sleep(0.5)
        thumbnail = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, 'thumbnail'))
        )

        webdriver.ActionChains(driver).move_to_element(thumbnail).click(thumbnail).perform()
        player = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, 'player'))
        )
        output_file_name = 'output' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S_") + search_word + '.mov'
        video_recording = Thread(target=record_video, args=(duration, ))
        audio_recording = Thread(target=record_audio, args=(duration, output_file_name[:-4] ))
        video_recording.start()
        audio_recording.start()

        video_recording.join()
        audio_recording.join()

        output_file_name = 'output' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S_") + search_word + '.mov'
        print(output_file_name)
        os.system('ffmpeg -hide_banner -loglevel error -i recording_video_only.mov -i audio_output.wav -c:v copy -c:a aac ' + output_file_name)
    except WebDriverException as wde:
        print('\tERROR')
        print('You may not be connected to the internet.')
        print('Chrome Driver or Chrome Browser is not installed or their versions do not match. ')
        print('More info: ', wde.msg)
        
        
    except Exception as e:
        print(e)
    finally:
        driver.quit()

if __name__ == '__main__':
    duration = 10
    search_word = None
    if len(sys.argv) >=2:
        try:
            duration = int(sys.argv[1])
        except:
            print('wrong first argument entered for duration. Going with 10 seconds')
    if len(sys.argv) >= 3:
        search_word = sys.argv[2]
    browse_youtube(special_word=search_word, duration=duration)