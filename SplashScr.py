import glm
import numpy as np
from PIL import Image
import time
from Shader import *
from Setting import *
from Texture import *
from UI.Text import *
import glfw
import moderngl as mgl


class SplashScreen:
    def __init__(self, icon_path="assets/icon.png", font_path="font/Roboto.ttf"):
        if not glfw.init():
            raise Exception("GLFW can't be initialized")

        self.width, self.height = 1300, 800
        self.window = glfw.create_window(
            self.width, self.height, ENGINE_NAME, None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can't be created")

        glfw.make_context_current(self.window)

        self.ctx = mgl.create_context()

        self.texture, self.image_size = self.load_texture(icon_path)

        self.text = Text(self, font_path=font_path)
        self.shader = ShaderProgram(self.ctx, shader_name='splashscr')
        self.program = self.shader.get_program()

        self.vertices = np.array([
            -1.0, -1.0, 0.0, 0.0,
            1.0, -1.0, 1.0, 0.0,
            -1.0, 1.0, 0.0, 1.0,
            -1.0, 1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 0.0,
            1.0, 1.0, 1.0, 1.0
        ], dtype=np.float32)

        self.vbo = self.ctx.buffer(self.vertices)
        self.vao = self.ctx.simple_vertex_array(
            self.program, self.vbo, 'in_position', 'in_texcoord')

        self.ctx.enable(mgl.BLEND)

        self.fov = 85.0
        self.aspect_ratio = self.width / self.height
        self.near = 0.01
        self.far = 10.0

        self.proj_matrix = glm.perspective(glm.radians(
            self.fov), self.aspect_ratio, self.near, self.far)
        self.model_matrix = glm.translate(
            glm.mat4(1.0), glm.vec3(0.0, 0.5, -2.0))

        self.alpha = 0.0
        self.fade_duration = 2.0
        self.start_time = time.time()

    def load_texture(self, image_path):
        image = Image.open(image_path).convert("RGBA")
        img_data = np.array(image, dtype=np.uint8)

        texture = self.ctx.texture(img_data.shape[:2], 4, img_data.tobytes())
        texture.use()

        return texture, image.size

    def render(self):
        while not glfw.window_should_close(self.window):
            self.ctx.clear(0.1, 0.16, 0.25, self.alpha)

            elapsed_time = time.time() - self.start_time
            if elapsed_time < self.fade_duration:
                self.alpha = elapsed_time / self.fade_duration

            self.program['alpha'] = self.alpha
            self.program['model'].write(self.model_matrix)
            self.program['projection'].write(self.proj_matrix)

            self.text.render(ENGINE_NAME.upper(), self.width / 2 - 72,
                             self.height / 2 + 165, scale=0.5)
            self.text.render(f'Version {ENGINE_VER}', self.width / 2 - 37.5,
                             self.height / 2 + 200, scale=0.4, color=(0.5, 0.5, 0.5))

            self.texture.use(location=0)
            self.vao.render()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

            if elapsed_time >= self.fade_duration:
                break

        glfw.terminate()
