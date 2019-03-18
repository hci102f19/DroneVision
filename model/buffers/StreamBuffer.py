import os

from model.buffers import Buffer
from model.exceptions import MissingEnvironmentVariable
from model.logging import log


class StreamBuffer(Buffer):
    def __init__(self, stream, x, y):
        super().__init__(stream, x, y)

        if 'protocol_whitelist;file,rtp,udp' not in os.environ.get('OPENCV_FFMPEG_CAPTURE_OPTIONS', None):
            raise MissingEnvironmentVariable('Missing OPENCV_FFMPEG_CAPTURE_OPTIONS')

    def run(self):
        self._running = True

        while not self.stream.isOpened():
            log("Waiting for stream to open")

        success, image = self.stream.read()
        while success and self._running:
            try:
                self._latest_frame = self.pre_process_frame(image)
            except Exception as e:
                pass

            success, image = self.stream.read()

        self._running = False
        self._latest_frame = None
