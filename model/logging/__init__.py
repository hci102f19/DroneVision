import logging


def log(msg, level=logging.DEBUG):
    log = logging.getLogger('DroneVision')
    log.log(level, msg)
