
"""
    yCrash Profiler: Logger
    A logger to log yCash profiler activities
"""

import logging

def configure_ycrash_logger():
    y_logger = logging.getLogger('ycrash-logger')
    y_logger.setLevel('DEBUG')
    formatter = logging.Formatter('yCrash: %(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('ycrash-profiler.log')
    file_handler.setFormatter(formatter)
    #console_handler = logging.StreamHandler()
    #console_handler.setFormatter(formatter)
    #logging.getLogger().addHandler(console_handler)
    y_logger.addHandler(file_handler)
    return y_logger


ycrash_logger = configure_ycrash_logger()
