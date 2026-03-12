import logging
def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(message)s")
    return logger