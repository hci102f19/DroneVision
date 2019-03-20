import json
import threading

from pyparrot.Bebop import Bebop

from model.flight.Vector import Vector


class BebopWrapper(threading.Thread):
    def __init__(self, bebop: Bebop):
        super().__init__()

        self.bebop = bebop
        self.bebop.set_indoor(True)
        self.bebop.start_video_stream()

        self.battery_level = None

        self._running = True
        self.next_command = None

    def smart_sleep(self, timer):
        self.bebop.smart_sleep(timer)

    def stop_video_stream(self):
        self.bebop.stop_video_stream()

    def disconnect(self):
        self._running = False

    def enqueue_vector(self, vector: Vector):
        self.next_command = vector

    def run(self):
        self.bebop.flat_trim(0)
        self.bebop.ask_for_state_update()
        self.bebop.safe_takeoff(5)
        self.bebop.fly_direct(0, 0, 0, -100, 0.5)

        while self._running:
            self.sensor_callback()
            if self.next_command is None:
                self.bebop.smart_sleep(0.1)
                continue

            if self.next_command is None:
                cmd = Vector()
            else:
                cmd, self.next_command = self.next_command, None

            with open('flight.log', 'a') as f:
                f.write(json.dumps(cmd.emit()) + '\n')
            self.bebop.fly_direct(**cmd.emit(), duration=0.25)

        self.bebop.safe_land(5)
        self.bebop.stop_video_stream()
        self.bebop.disconnect()

    def sensor_callback(self):
        if self.battery_level is None or self.bebop.sensors.battery != self.battery_level:
            self.battery_level = self.bebop.sensors.battery
            print(f'battery_level: {self.battery_level}')
