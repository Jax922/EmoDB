import logging
from logging.handlers import RotatingFileHandler
import os

# 确保日志目录存在
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# 创建一个 RotatingFileHandler，设置最大文件大小为1MB，保留5个日志文件
log_file_path = os.path.join(log_directory, 'app.log')  # 保证日志文件在 logs 目录下
handler = RotatingFileHandler(log_file_path, maxBytes=1e6, backupCount=5)

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 创建并设置logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def log_message(message, level='info'):
    """记录日志消息"""
    if level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)
    elif level == 'critical':
        logger.critical(message)
    elif level == 'debug':
        logger.debug(message)
    else:
        raise ValueError(f"Invalid log level: {level}")