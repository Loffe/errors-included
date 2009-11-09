import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log.txt',
                    filemode='aw')

logger = logging.getLogger('errors-included')
logger.info("hej")
