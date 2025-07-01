import glm
import glfw


class Mouse:
    def __init__(self, app):
        self.window = app.window
        self.position = glm.vec2(0)
        self.xoffset, self.yoffset = 0, 0
        self.last_x, self.last_y = 0, 0

    def set_cursor_mode(self, mode):
        glfw.set_input_mode(self.window, glfw.CURSOR, mode)

    def update(self):
        mouse_pos = glfw.get_cursor_pos(self.window)
        self.position = glm.vec2(*mouse_pos)
        mouse_x, mouse_y = self.position
        self.xoffset = mouse_x - self.last_x
        self.yoffset = self.last_y - mouse_y
        self.last_x, self.last_y = mouse_x, mouse_y


