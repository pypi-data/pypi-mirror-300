"""
HS tools
"""
import logging


def logger(file_name:str):
    """init logger

    Args:
        file_name (str): file name

    Returns:
        any:  logger
    """
    log = logging.getLogger(file_name)
    log.setLevel(level=logging.DEBUG)
    fh = logging.FileHandler(file_name)
    _format = '%(asctime)s %(levelname)s ln:%(lineno)d %(funcName)s - %(message)s'
    fh_formatter = logging.Formatter(_format)
    fh.setFormatter(fh_formatter)
    log.addHandler(fh)
    return log
