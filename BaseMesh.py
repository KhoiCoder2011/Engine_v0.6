import numpy as np
from Setting import *

class BaseMesh:
    def __init__(self, object):
        self.object = object
        self.app = object.app
        self.light = self.app.light
        self.ctx = self.app.ctx
        self.program = self.app.prog
        self.camera = self.app.camera
        self.texture = object.texture
        self.rigidbody = object.rigidbody
        self.update = object.update
        self.render_type = object.render_type
        
        self.vbo = self.ctx.buffer(np.array(object.vertices, dtype='f4'))
        self.ibo = self.ctx.buffer(np.array(object.indices, dtype='u4'))
        self.color_buffer = self.ctx.buffer(np.array(object.colors, dtype='f4'))
        self.uv_buffer = self.ctx.buffer(np.array(object.uv, dtype='f4'))
        self.normals_buffer = self.ctx.buffer(np.array(object.normals, dtype='f4'))

        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (self.vbo, '3f', 'in_vert'),
                (self.color_buffer, '3f', 'in_color'),
                (self.uv_buffer, '2f', 'in_uv'),
                (self.normals_buffer, '3f', 'in_normal'),
            ],
            index_buffer=self.ibo,
        )

    def get_model_matrix(self):
        self.m_model = glm.translate(glm.mat4(), self.object.position)
        self.m_model = glm.rotate(self.m_model, glm.radians(self.object.rotation.x), glm.vec3(1, 0, 0))
        self.m_model = glm.rotate(self.m_model, glm.radians(self.object.rotation.y), glm.vec3(0, 1, 0))
        self.m_model = glm.rotate(self.m_model, glm.radians(self.object.rotation.z), glm.vec3(0, 0, 1))
        self.m_model = glm.scale(self.m_model, self.object.scale)

    def render(self):
        self.get_model_matrix()
        #self.rigidbody.update(self.app.time)
        self.program['m_model'].write(self.m_model)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['light_position'].write(self.light.position)
        self.program['light_color'].write(self.light.color)
        self.program['camera_position'].write(self.camera.position)
        self.program['ambient'] = self.light.ambient
        self.program['shininess'] = self.light.shininess
        self.program['gamma'] = self.light.gamma
        self.program['u_texture'] = 0
        self.texture.use(location = 0)
        self.vao.render(self.render_type)
        self.update()
