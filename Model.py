from BaseMesh import *
from Material import *
from Setting import *
import glm
from Texture import Texture
from Manager.Model import *
from Physic.RigidBody import Rigidbody
from Script import Script, BlankScript


class BaseModel(BaseMesh):
    def __init__(self, o):
        self.app = getattr(o, 'app', None)
        self.position = getattr(o, 'position', None)
        self.rotation = getattr(o, 'rotation', None)
        self.scale = getattr(o, 'scale', None)
        self.color = getattr(o, 'color', None)
        self.name = getattr(o, 'name', None)
        self.id = getattr(o, 'id', None)
        self.tag = getattr(o, 'tag', None)
        self.type = getattr(o, 'type', None)
        self.vertices = getattr(o, 'vertices', None)
        self.indices = getattr(o, 'indices', None)
        self.normals = getattr(o, 'normals', None)
        self.uv = getattr(o, 'uv', None)
        self.set_active = getattr(o, 'set_active', None)
        self.texture_path = getattr(o, 'texture_path', None)
        self.model_path = getattr(o, 'model_path', None)
        self.rigidbody = getattr(o, 'rigidbody', None)
        self.render_type = getattr(o, 'render_type', mgl.TRIANGLES)
        self.update = getattr(o, 'update', None)
        super().__init__(self)

    def to_dict(self):
        return {
            "name": self.name,
            "position": self.position.to_tuple(),
            "rotation": self.rotation.to_tuple(),
            "scale": self.scale.to_tuple(),
            "color": self.color.to_tuple(),
            "texture_path": self.texture_path,
            "model_path": self.model_path,
            "type": self.type,
            "tag": self.tag,
            "id": self.id,
            "set_active": self.set_active
        }


default_material = Material()
default_script = BlankScript()


class Cube(BaseModel):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1),
                 material: Material = default_material, script: Script = default_script):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.material = material
        self.texture_path = material.texture_path
        self.texture = Texture(app, material.texture_path)
        self.set_active = True
        self.tag = ''
        self.name = f'Cube {self.position.to_tuple()}'
        self.type = 'Cube'
        self.id = ''
        cube = CubeModel()
        self.vertices = cube.vertices
        self.uv = cube.uv
        self.normals = cube.normals
        self.indices = cube.indices
        self.color = material.color
        self.alpha = material.alpha
        self.colors = np.tile(self.color, len(self.vertices) // 3)
        self.rigidbody = Rigidbody(self)
        self.script = script
        self.script.obj = self
        self.script.app = self.app
        self.script.start()
        self.update = self.script.update
        super().__init__(self)

    # def create_indices(self):
    #     face_indices = [
    #         [0, 1, 2, 0, 2, 3],
    #         [4, 5, 6, 4, 6, 7],
    #         [8, 9, 10, 8, 10, 11],
    #         [12, 13, 14, 12, 14, 15],
    #         [16, 17, 18, 16, 18, 19],
    #         [20, 21, 22, 20, 22, 23]
    #     ]

    #     indices = [idx for face, idx in zip(
    #         self.faces, face_indices) if face != False]
    #     return np.array([index for sublist in indices for index in sublist], dtype='u4')


class Quad(BaseModel):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1),
                 material: Material = default_material, script: Script = default_script):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.material = material
        self.texture_path = material.texture_path
        self.texture = Texture(app, self.texture_path)
        self.set_active = True
        self.tag = ''
        self.name = f'Quad {self.position.to_tuple()}'
        self.type = 'Quad'
        self.id = ''
        quad = QuadModel()
        self.vertices = quad.vertices
        self.uv = quad.uv
        self.normals = quad.normals
        self.indices = quad.indices
        self.color = material.color
        self.alpha = material.alpha
        self.colors = np.tile(self.color, len(self.vertices) // 3)
        self.rigidbody = Rigidbody(self)
        self.script = script
        self.script.obj = self
        self.script.app = self.app
        self.script.start()
        self.update = self.script.update
        super().__init__(self)


class OBJModel(BaseModel):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1),
                 path: str = 'assets/meshes/cube.obj', material: Material = default_material, script: Script = default_script):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.path = path
        self.material = material
        self.texture_path = material.texture_path
        self.texture = Texture(app, self.texture_path)
        self.set_active = True
        self.tag = ''
        self.name = f'OBJModel {self.position.to_tuple()}'
        self.type = 'OBJModel'
        self.id = ''
        self.model_path = path
        obj = OBJLoader(path)
        self.vertices = obj.vertices
        self.uv = obj.uv
        self.normals = obj.normals
        self.indices = obj.indices
        self.color = material.color
        self.alpha = material.alpha
        self.colors = np.tile(self.color, len(self.vertices) * 3)
        self.rigidbody = Rigidbody(self)
        self.script = script
        self.script.obj = self
        self.script.app = self.app
        self.script.start()
        self.update = self.script.update
        super().__init__(self)


class Grid(BaseModel):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1),
                 material: Material = default_material, script: Script = default_script):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.material = material
        self.texture_path = material.texture_path
        self.texture = Texture(app, self.texture_path)
        self.set_active = True
        self.tag = ''
        self.name = f'Grid {self.position.to_tuple()}'
        self.type = 'Grid'
        self.id = ''
        self.grid_size = 10
        self.grid_spacing = 1
        self.radius = 1
        grid = GridModel(self.grid_size, self.grid_spacing)
        self.vertices, self.indices = grid.vertices, grid.indices
        self.normals = grid.normals
        self.uv = grid.uv
        self.color = material.color
        self.alpha = material.alpha
        self.colors = np.tile(self.color, len(self.vertices) // 3)
        self.rigidbody = Rigidbody(self)
        self.render_type = mgl.LINES
        self.script = script
        self.script.obj = self
        self.script.app = self.app
        self.script.start()
        self.update = self.script.update
        super().__init__(self)

class Sphere(BaseModel):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1),
                  material: Material = default_material, script: Script = default_script):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.material = material
        self.texture_path = material.texture_path
        self.texture = Texture(app, self.texture_path)
        self.set_active = True
        self.tag = ''
        self.name = f'Sphere {self.position.to_tuple()}'
        self.type = 'Sphere'
        self.id = ''
        self.radius = 1
        sphere = SphereModel(self.radius)
        self.vertices = sphere.vertices
        self.uv = sphere.uv
        self.normals = sphere.normals
        self.indices = sphere.indices
        self.color = material.color
        self.alpha = material.alpha
        self.colors = np.tile(self.color, len(self.vertices))
        self.rigidbody = Rigidbody(self)
        self.script = script
        self.script.obj = self
        self.script.app = self.app
        self.script.start()
        self.update = self.script.update
        super().__init__(self)

class Cylinder(BaseModel):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1),
                  material: Material = default_material, script: Script = default_script):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.material = material
        self.texture_path = material.texture_path
        self.texture = Texture(app, self.texture_path)
        self.set_active = True
        self.tag = ''
        self.name = f'Cylinder {self.position.to_tuple()}'
        self.type = 'Cylinder'
        self.id = ''
        self.radius = 1
        cylinder = CylinderModel(self.radius)
        self.vertices = cylinder.vertices
        self.uv = cylinder.uv
        self.normals = cylinder.normals
        self.indices = cylinder.indices
        self.color = material.color
        self.alpha = material.alpha
        self.colors = np.tile(self.color, len(self.vertices))
        self.rigidbody = Rigidbody(self)
        self.script = script
        self.script.obj = self
        self.script.app = self.app
        self.script.start()
        self.update = self.script.update
        super().__init__(self)
