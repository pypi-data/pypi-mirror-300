import threading
import logging


def sampleLogging():
    buggy_app_logger.debug('This is log simulation')
    buggy_app_logger.info('This is log simulation')
    buggy_app_logger.warning('This is log simulation')
    buggy_app_logger.error('This is log simulation')
    buggy_app_logger.critical('This is log simulation')


def contineous_logs_simulation():
    logging_thread = threading.Thread(target=sampleLogging, name="buggyapp.logger.thread")
    logging_thread.start()


def configure_buggyapp_logger():
    b_logger = logging.getLogger('buggyapp-logger')
    b_logger.setLevel('INFO')
    formatter = logging.Formatter('buggyapp: %(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('buggyapp.log')
    file_handler.setFormatter(formatter)
    b_logger.addHandler(file_handler)
    return b_logger


buggy_app_logger = configure_buggyapp_logger()
