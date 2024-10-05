# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 09:07:19 2022
Updated on Fri Okt 04 12:21:20 2024

@author: Mohamed
"""

import os
import sys
import logging
import inspect

class Rocklogger():
    def __init__(self, level='info'):
        self.logger = self.__setup_logger(self.__get_level(level))
    
    def __setup_logger(self, log_lvl):
        caller_dirname, caller_filename = self.__get_caller()
        log_dir = os.path.join(caller_dirname, 'logs')
        log_file = os.path.join(log_dir, caller_filename + '.log')
        os.makedirs(log_dir, exist_ok=True)
        with open(log_file, 'a') as the_file:
            the_file.write('#'*100 + '\n')
                            
        logging.basicConfig(filename=log_file, filemode='a', 
                        format='%(asctime)s - %(filename)s - %(levelname)-8s:  %(message)s', # :%(name)s 
                        datefmt='%Y-%m-%d %H:%M:%S', 
                        level=log_lvl, 
                        force=True)
    
        # define a Handler which writes INFO messages or higher to the sys.stdout (stderr is also an option) 
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(log_lvl)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)-8s:  %(message)s', 
                                      datefmt='%Y-%m-%d %H:%M:%S') # :%(name)
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger().addHandler(console)
        
        logger = logging.getLogger(__name__)
        return logger
    
    def __get_level(self, log_level_str):
        levels = {
            'info': logging.INFO,
            'debug': logging.DEBUG,
            'warning': logging.WARNING,
            'error': logging.ERROR
        }
        return levels.get(log_level_str.lower(), logging.INFO)
    
    def __get_caller(self):
    for frame_info in inspect.stack():
        module = inspect.getmodule(frame_info.frame)
        if module and module.__name__ != __name__:
            if module.__file__:
                dir_name, file_name = os.path.split(module.__file__)
                file_name = file_name.split('.')[0]
                return dir_name, file_name
            else:
                return os.getcwd(), 'interactive_shell'
    return os.getcwd(), 'unknown'
    
    def get_logger(self):
        return self.logger
    
    def close(self):
        # Spyder does not release the log file. Could not break the link into
        # multiple lines.
        # https://stackoverflow.com/questions/15435652/python-does-not-release-filehandles-to-logfile#:~:text=I%20was%20using,the%20Spyder%20environment.
        handlers = self.logger.handlers[:]
        for handler in handlers:
            self.logger.removeHandler(handler)
            handler.close()
            
    def __del__(self):
        self.close()
        

if __name__ == "__main__":
    logger = Rocklogger().init(level='debug')
    logger.debug('Hello Rocklogger!')

