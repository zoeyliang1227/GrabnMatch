import logging

from datetime import datetime

time_string = datetime.now().strftime('%Y-%m-%d')

def get_logger(name):
    dev_logger: logging.Logger = logging.getLogger(name)
    if not dev_logger.handlers:
        dev_logger.setLevel(logging.DEBUG)

        formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y%m%d %H:%M:%S')

        # print on console
        handler: logging.StreamHandler = logging.StreamHandler()    #StreamHandler 用來控制輸出終端機的相關設定
        handler.setFormatter(formatter)
        dev_logger.addHandler(handler)

        #save on log    
        file_handler = logging.StreamHandler(open(f'{time_string}.log', 'w'))
        file_handler.setLevel(logging.CRITICAL)
        file_handler.setFormatter(formatter)
        dev_logger.addHandler(file_handler)

    return dev_logger