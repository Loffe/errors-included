import logging

def getLogger(filename="log.txt"):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=filename,
                        filemode='w')

    return logging.getLogger('errors-included')
