import os
from time import sleep

from model.buffers import Buffer
from model.exceptions import MissingEnvironmentVariable
from model.logging import log


class StreamBuffer(Buffer):
    def __init__(self, stream, x, y):
        super().__init__(stream, x, y)

        # Thanks:
        # http://answers.opencv.org/question/192178/how-to-set-ffmpeg-option-protocol_whitelist-fileudprtp-in-videocapture/
        # os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'protocol_whitelist;file,rtp,udp'
        env = os.environ.get('OPENCV_FFMPEG_CAPTURE_OPTIONS', None)
        if env is None or 'protocol_whitelist;file,rtp,udp' not in env:
            raise MissingEnvironmentVariable('Missing OPENCV_FFMPEG_CAPTURE_OPTIONS')

    def run(self):
        self._running = True

        while not self.stream.isOpened():
            log("Waiting for stream to open")
            sleep(0.1)

        success, image = self.stream.read()
        while success and self._running:
            self._latest_frame = self.pre_process_frame(image)

            success, image = self.stream.read()

        self._running = False
        self._latest_frame = None
