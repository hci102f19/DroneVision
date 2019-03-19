import logging


class Logger(object):
    def __init__(self):
        # FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
        logging.basicConfig(level=logging.DEBUG)

        self.log = logging.getLogger('DroneVision')

    def info(self, msg):
        self.log.info(msg)

    def error(self, msg):
        self.log.error(msg)

    def debug(self, msg):
        self.log.debug(msg)


log = Logger()
