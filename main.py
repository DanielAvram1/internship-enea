
from selenium.common.exceptions import WebDriverException, TimeoutException
from logger import Logger
from scrapper import Scrapper
from screen_record import record_video
from audio_record import record_audio, get_decibel_level
from threading import Thread
import subprocess
from datetime import datetime
import sys
import config as c


def main(myLogger, special_word=None, duration=10):
    try:
        
        scrapper = Scrapper(myLogger)
        search_word = scrapper.browse_youtube(special_word=special_word)

        output_file_name = 'output' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S_") + search_word + '.mov'

        video_recording = Thread(target=record_video, args=(duration, ))
        audio_recording = Thread(target=record_audio, args=(duration,  ))
        video_recording.start()
        audio_recording.start()

        video_recording.join()
        audio_recording.join()
        
        decibel_level = get_decibel_level(c.WAVE_OUTPUT_FILENAME)
        print('decibel level: ', decibel_level)
        output_file_name = 'output' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S_") + search_word + '.mov'
        
        with open('info.txt', 'a') as f:
            f.write(output_file_name[:-4] + ': ' + str(decibel_level) + '\n')
    
        print(output_file_name)
        try:
            subprocess.run(f'ffmpeg -hide_banner -loglevel error -i {c.MOV_OUTPUT_FILENAME } -i {c.WAVE_OUTPUT_FILENAME}  -c:v copy -c:a aac  {output_file_name}', shell=True)
        except subprocess.CalledProcessError as cpe:
            myLogger.write('error', f'{cpe}')
        
        myLogger.write('info', f'recording {output_file_name} was written with succes.')
    
    except TimeoutException as te:
        myLogger.write('error', str(te.msg))
    
    except WebDriverException as wde:
        error_message = str(wde.msg)
        print('error:   ', error_message)
        if 'ERR_INTERNET_DISCONNECTED' in error_message:
            myLogger.write('error', "Chrome Driver wasn't able to connect to the internet.")
        elif "ERR_NAME_NOT_RESOLVED" in str(error_message):
            myLogger.write('error', f"Unable to Navigate to URL:{c.URL}")
        print('More info: ', error_message)

    except IOError as ioe:
        myLogger.write('error', f'{ioe}')
    
    finally:
        scrapper.quit()


if __name__ == '__main__':
    duration = 10
    search_word = None
    myLogger = Logger()
    if len(sys.argv) >=2:
        try:
            duration = int(sys.argv[1])
        except:
            print('wrong first argument entered for duration. Going with 10 seconds.')
            myLogger.waring(f'The duration entered by the user {duration} is not valid')
    if len(sys.argv) >= 3:
        search_word = sys.argv[2]
    main( myLogger, special_word=search_word, duration=duration)