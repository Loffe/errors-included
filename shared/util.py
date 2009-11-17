import logging

def getLogger(filename="log.txt"):
    logger = logging.getLogger(filename)
    fh = logging.FileHandler(filename,'w')
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)

    return logger
