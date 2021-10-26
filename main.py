from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
import time
from screen_record import record_video
from audio_record import record_audio
from threading import Thread
import os
import subprocess
from datetime import datetime
from random_word import RandomWords
import sys
import config as c
import logging

logging.basicConfig(filename='log_file.log',
                    format='%(asctime)s %(message)s',
                    filemode='w'
                    )

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def search_random(driver, special_word=None):
    try:
        search = WebDriverWait(driver, c.TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, c.SEARCH_CSS_SELECTOR))
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
    except TimeoutException as te:
        print('\tERROR')
        print(f'No element with CSS SELECTOR {c.SEARCH_CSS_SELECTOR} was found.')
        logger.error(f'No element with CSS SELECTOR {c.SEARCH_CSS_SELECTOR} was found.')
    finally:
        return ''
    

def browse_youtube(special_word=None, duration=10):
    try:
        driver = webdriver.Chrome()
        driver.get(c.URL)
        
        search_word = None
        print('searching...')
        search_word = search_random(driver, special_word=special_word)
        try:
            no_results = WebDriverWait(driver, c.TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, c.NO_RESULTS_CSS_SELECTOR))
            )
            print(f'No results were found while searching for {search_word}, getting a random video from main page.')
            logger.warning(f'No results were found while searching for {search_word}, getting a random video from main page.')
            driver.get(c.URL)
        except TimeoutException as te:
            print(f'{search_word} gave video results.')
            logger.info(f'{search_word} gave video results.')
        thumbnail = None
        try:
            thumbnail = WebDriverWait(driver, c.TIMEOUT).until(
                EC.presence_of_element_located((By.ID, c.THUMBNAIL_ID))
            )
            
        except TimeoutException as te:
            print('\tERROR')
            print(f'No element with ID {c.THUMBNAIL_ID} was found.')
            logger.error(f'No element with ID {c.THUMBNAIL_ID} was found.')
            driver.quit()
            return

        while True:
            webdriver.ActionChains(driver).move_to_element(thumbnail).click(thumbnail).perform()
            try:
                player = WebDriverWait(driver, c.TIMEOUT).until(
                    EC.presence_of_element_located((By.ID, c.PLAYER_ID))
                )
                break
            except:
                print('No player was found... clicking again.')
                logger.warning(f'No player was found... clicking again.')
                
        output_file_name = 'output' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S_") + search_word + '.mov'
        video_recording = Thread(target=record_video, args=(duration, logger))
        audio_recording = Thread(target=record_audio, args=(duration, output_file_name[:-4], logger ))
        video_recording.start()
        audio_recording.start()

        video_recording.join()
        audio_recording.join()
        
        output_file_name = 'output' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S_") + search_word + '.mov'
        
        print(output_file_name)
        try:
            subprocess.run(f'ffmpeg -hide_banner -loglevel error -i {c.MOV_OUTPUT_FILENAME } -i {c.WAVE_OUTPUT_FILENAME}  -c:v copy -c:a aac  {output_file_name}', shell=True)
        except subprocess.CalledProcessError as cpe:
            print('\tERROR')
            print(f'{cpe}')
            logger.error(f'{cpe}')
        
        logger.info(f'recording {output_file_name} was written with succes.')
    except TimeoutException as te:
        print('\tERROR')
        print(str(te.msg))
    
    except WebDriverException as wde:
        print('\tERROR')
        error_message = str(wde.msg)
        print('error:   ', error_message)
        if 'ERR_INTERNET_DISCONNECTED' in error_message:
            print("Chrome Driver wasn't able to connect to the internet.")
            logger.error("Chrome Driver wasn't able to connect to the internet.")
        elif "ERR_NAME_NOT_RESOLVED" in str(error_message):
            print(f"Unable to Navigate to URL:{c.URL}")
            logger.error(f"Unable to Navigate to URL:{c.URL}")
        print('More info: ', error_message)

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
            print('wrong first argument entered for duration. Going with 10 seconds.')
            logger.waring(f'The duration entered by the user {duration} is not valid')
    if len(sys.argv) >= 3:
        search_word = sys.argv[2]
    browse_youtube(special_word=search_word, duration=duration)