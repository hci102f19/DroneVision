class Key(object):
    def __init__(self):
        self.value = False
        self.pressed = False

    def set(self, key, value):
        if key == value and not self.pressed:
            self.value = not self.value
            self.pressed = True
        else:
            self.pressed = False

    def __bool__(self):
        return self.value
