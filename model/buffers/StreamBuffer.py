from model.buffers import Buffer
from model.logging import log


class StreamBuffer(Buffer):
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
