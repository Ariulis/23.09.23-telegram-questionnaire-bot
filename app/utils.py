from loguru import logger

logger.add('log/debug.log', level='DEBUG',
           format='{time} {level} {message}', rotation='10 KB', compression='zip')
