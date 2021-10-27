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

class Scrapper:
    def __init__(self, logger):
        self.logger = logger
        self.driver = webdriver.Chrome()
        

    def __search_random(self, special_word=None):
        try:
            search = WebDriverWait(self.driver, c.TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, c.SEARCH_CSS_SELECTOR))
            )
        
            search_word = None
            
            search_word = RandomWords().get_random_word()
            if special_word is not None:
                search_word = special_word
            
            print(search_word)
            
            search.send_keys(search_word)
            search.send_keys(Keys.RETURN)
        except TimeoutException as te:
            self.logger.write('error', f'No element with CSS SELECTOR {c.SEARCH_CSS_SELECTOR} was found.')
        finally:
            if search_word is not None:
                return search_word
            else:
                return ''

    def quit(self):
        self.driver.quit()

    def browse_youtube(self, special_word=None):
        self.driver.get(c.URL)
        print('searching...')
        search_word = self.__search_random( special_word=special_word)
        try:
            no_results = WebDriverWait(self.driver, c.TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, c.NO_RESULTS_CSS_SELECTOR))
            )
            self.logger.write('warning', f'No results were found while searching for {search_word}, getting a random video from main page.')
        except TimeoutException as te:
            self.logger.write('info', f'{search_word} gave video results.')
        thumbnail = None
        try:
            thumbnail = WebDriverWait(self.driver, c.TIMEOUT).until(
                EC.presence_of_element_located((By.ID, c.THUMBNAIL_ID))
            )
            print('Thumbnail was found.')
        except TimeoutException as te:
            self.logger.write('error', f'No element with ID {c.THUMBNAIL_ID} was found.')
            self.driver.quit()
            return

        while True:
            webdriver.ActionChains(self.driver).move_to_element(thumbnail).click(thumbnail).perform()
            try:
                player = WebDriverWait(self.driver, c.TIMEOUT).until(
                    EC.presence_of_element_located((By.ID, c.PLAYER_ID))
                )
                break
            except:
                self.logger.write('warning', f'No player was found... clicking again.')
                
        return search_word
        