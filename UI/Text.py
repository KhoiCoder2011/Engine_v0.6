import glfw
import moderngl as mgl
import freetype
import glm
import numpy as np
from Shader import ShaderProgram


class CharacterSlot:
    def __init__(self, texture, glyph):
        self.texture = texture
        self.size = (glyph.bitmap.width, glyph.bitmap.rows)
        self.bearing = (glyph.bitmap_left, glyph.bitmap_top)
        self.advance = glyph.advance.x


class TextRenderer:
    def __init__(self, app):
        self.ctx = app.ctx
        self.font_path = app.font_path
        self.characters = {}
        self.width, self.height = glfw.get_window_size(app.window)
        self._init_resources()

    def _init_resources(self):

        self.shader = ShaderProgram(self.ctx, shader_name='ui_text')
        self.program = self.shader.get_program()

        projection = glm.ortho(0, self.width, self.height, 0, -1, 1)
        self.program['projection'].write(projection)

        self.vbo = self.ctx.buffer(reserve=6 * 4 * 4)

        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '4f', 'vertex')]
        )

        self._load_characters()

    def _load_characters(self):
        face = freetype.Face(self.font_path)
        face.set_char_size(48 * 64)

        for char_code in range(128):
            char = chr(char_code)
            face.load_char(char)
            glyph = face.glyph
            bitmap = glyph.bitmap

            texture = self.ctx.texture(
                (bitmap.width, bitmap.rows),
                components=1,
                data=bytes(bitmap.buffer)
            )
            texture.repeat_x = False
            texture.repeat_y = False
            texture.filter = (mgl.LINEAR, mgl.LINEAR)

            self.characters[char] = CharacterSlot(texture, glyph)

    def render(self, text, x, y, scale=1.0, color=(1.0, 1.0, 1.0)):
        self.program['textColor'].value = color

        for c in text:
            if c not in self.characters:
                continue

            ch = self.characters[c]
            xpos = x + ch.bearing[0] * scale
            ypos = y - (ch.size[1] - ch.bearing[1]) * scale
            w = ch.size[0] * scale
            h = ch.size[1] * scale

            vertices = np.array([
                xpos,     ypos - h, 0.0, 0.0,
                xpos,     ypos,     0.0, 1.0,
                xpos + w, ypos,     1.0, 1.0,

                xpos,     ypos - h, 0.0, 0.0,
                xpos + w, ypos,     1.0, 1.0,
                xpos + w, ypos - h, 1.0, 0.0,
            ], dtype='f4')

            self.vbo.write(vertices.tobytes())
            ch.texture.use(location=0)
            self.vao.render(mode=mgl.TRIANGLES)

            x += (ch.advance >> 6) * scale


class Text:
    def __init__(self, app, font_path='Font/Roboto.ttf'):
        self.app = app
        self.window = app.window
        self.font_path = font_path
        self.ctx = app.ctx
        self.renderer = TextRenderer(self)

    def render(self, content, x=10, y=0, scale=0.7, color=(1.0, 1.0, 1.0)):
        self.renderer.render(content, x, y + 70, scale, color)
