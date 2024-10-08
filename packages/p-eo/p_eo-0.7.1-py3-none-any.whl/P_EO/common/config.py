import logging
import os


class Default:
    IMPLICITLY_WAIT = 5
    TIMEOUT = 5
    INTERVAL = 0.25
    ACTION_WAIT = 0.25
    REFRESH_WAIT = 2
    SCREENSHOTS = True
    SCREENSHOTS_PATH = os.path.join(os.getcwd(), 'screenshots')


class LogConfig:
    # STREAM输出相关配置
    STREAM = False
    STREAM_LEVEL = logging.INFO
    STREAM_FORMAT = ''

    # Log文件相关配置
    LOG_FILE = ''
    LOG_FILE_LEVEL = logging.INFO
    LOG_FILE_FORMAT = ''

    SAVE_ERROR = True
