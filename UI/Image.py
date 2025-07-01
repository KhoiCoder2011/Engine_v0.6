import moderngl
import numpy as np
from PIL import Image as PIL_Image
from Shader import ShaderProgram


class Image:
    def __init__(self, app, image_path):
        self.ctx = app.ctx
        self.program = ShaderProgram(
            self.ctx, shader_name='ui_image').get_program()

        self.texture = self.load_texture(image_path)

        vertices = np.array([
            -1.0, -1.0, 0.0, 0.0,
            1.0, -1.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 1.0,
            -1.0,  1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 0.0,
            1.0,  1.0, 1.0, 1.0,
        ], dtype='f4')

        vbo = self.ctx.buffer(vertices.tobytes())
        self.vao = self.ctx.vertex_array(
            self.program, vbo, 'in_position', 'in_uv')
        self.texture.use(location=0)

    def load_texture(self, path):
        img = PIL_Image.open(path).transpose(PIL_Image.FLIP_TOP_BOTTOM).convert('RGBA')
        tex = self.ctx.texture(img.size, 4, img.tobytes())
        tex.build_mipmaps()
        tex.filter = (moderngl.LINEAR, moderngl.LINEAR)
        return tex

    def render(self):
        self.vao.render()
