import glfw

class Keyboard:
    def __init__(self, app):
        self.window = app.window

    def is_pressed(self, click_key):
        return glfw.get_key(self.window, click_key) == glfw.PRESS
