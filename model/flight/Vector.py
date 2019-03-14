class Vector(object):
    def __init__(self, **kwargs):
        self._roll = kwargs.get('roll', 0)
        self._pitch = kwargs.get('pitch', 0)
        self._yaw = kwargs.get('yaw', 0)
        self._vertical_movement = kwargs.get('vertical_movement', 0)

    def set_roll(self, roll):
        self._roll = roll

    def set_pitch(self, pitch):
        self._pitch = pitch

    def set_yaw(self, yaw):
        self._yaw = yaw

    def set_vertical_movement(self, vertical_movement):
        self._vertical_movement = vertical_movement

    @staticmethod
    def __round(val):
        return int(round(val, 0))

    def emit(self):
        return {
            'roll': self.__round(self._roll),
            'pitch': self.__round(self._pitch),
            'yaw': self.__round(self._yaw),
            'vertical_movement': self.__round(self._vertical_movement)
        }

    def is_null(self):
        for k, v in self.__dict__.items():
            if v != 0:
                return False
        return True
