import keyboard

last = None
while True:
    if keyboard.get_hotkey_name():
        key = keyboard.get_hotkey_name()

        if (last is None or last != key) and key:
            last = key
            print(f'"{key}"')
