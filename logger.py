import logging
import config as c

class NoTypeFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Logger:
    def __init__(self, filemode='w'):
        logging.basicConfig(filename=c.LOG_FILE_FILENAME,
                    format='%(asctime)s %(message)s',
                    filemode='w'
                    )

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
    
    def write(self, type:str, message:str):
        if type != 'info':
            print(f'\t{ type.upper()  }')
        print(message)
        if type == 'info':
            self.logger.info(message)
        elif type == 'debug':
            self.logger.debug(message)
        elif type == 'error':
            self.logger.error(message)
        elif type == 'warning':
            self.logger.warning(message)
        else:
            raise NoTypeFoundException(f'{type} is not a logger type.')