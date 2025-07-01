import glfw
import sys
import os
sys.path.append(os.path.dirname(__file__))
from Light import DirectionalLight
from Camera import Camera
from Delete_cache import *
from SplashScr import *
from Scene import Scene
from Shader import ShaderProgram
from Input.Mouse import Mouse
from Input.Keyboard import Keyboard
import moderngl as mgl
from GUI.GUI import *
from UI.Text import *
from Setting import *


class Engine:
    def __init__(self):
        # SplashScreen().render()

        if not glfw.init():
            raise Exception("GLFW can't be initialized!")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, GL_MAJOR)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, GL_MINOR)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)

        self.window = glfw.create_window(
            WIDTH, HEIGHT, f"{ENGINE_NAME} | {PLATFORM} | Version {ENGINE_VER} | OpenGL {GL_MAJOR}.{GL_MINOR}", None, None)
        # glfw.set_window_icon(self.window, 1, [Image_Loader(icon_path).load()])

        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can't be created!")

        glfw.set_window_pos(self.window, 15, 35)
        glfw.make_context_current(self.window)

        self.ctx = mgl.create_context(screenshots=True, samples=4)
        self.ctx.viewport = (300, HEIGHT - DISPLAY_HEIGHT,
                             DISPLAY_WIDTH, DISPLAY_HEIGHT)

        self.ctx.multisample = True
        self.ctx.enable(mgl.DEPTH_TEST | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.time = 0
        self.delta_time = 0
        self.last_time = glfw.get_time()
        self.fps = 0
        self.is_mouse_disabled = True
        self.gl_init()

    def gl_init(self):
        self.camera = Camera()
        self.shader = ShaderProgram(self.ctx)
        self.prog = self.shader.get_program()
        self.light = DirectionalLight()
        self.scene = Scene(self)
        self.keyboard = Keyboard(self)
        self.mouse = Mouse(self)
        self.gui = GUI(self)
        self.mouse.set_cursor_mode(glfw.CURSOR_DISABLED)

    def render(self):
        self.ctx.clear(color=BG_COLOR)
        self.scene.render()
        self.gui.render()

    def update(self):
        self.camera.update()
        current_time = glfw.get_time()
        self.delta_time = current_time - self.last_time
        self.time += self.delta_time
        self.fps = 1 / self.delta_time
        self.last_time = current_time
        self.scene.update()
        self.mouse.update()

    def destroy(self):
        self.ctx.release()
        self.prog.release()
        self.scene.save()
        delete_cache()

    def handle_events(self):
        if self.keyboard.is_pressed(glfw.KEY_F1):
            self.mouse.set_cursor_mode(glfw.CURSOR_DISABLED)
            self.is_mouse_disabled = True
        if self.keyboard.is_pressed(glfw.KEY_F2):
            self.mouse.set_cursor_mode(glfw.CURSOR_NORMAL)
            self.is_mouse_disabled = False

        glfw.poll_events()

        if glfw.window_should_close(self.window) or self.keyboard.is_pressed(glfw.KEY_ESCAPE):
            self.destroy()
            self.scene.save()
            sys.exit()

        if self.is_mouse_disabled:
            self.camera.mouse_movement(self.mouse.xoffset, self.mouse.yoffset)
            self.camera.movement(self.keyboard, self.delta_time)

    def run(self):
        while not glfw.window_should_close(self.window):
            self.handle_events()
            self.update()
            self.render()
            glfw.swap_buffers(self.window)

        glfw.terminate()


if __name__ == '__main__':
    engine = Engine()
    engine.run()
