from Model import Quad
from Material import Material


class Skybox:
    def __init__(self, scene):
        self.app = scene.app
        self.location = 'assets/skybox/'
        self.format = '.png'
        self.faces = ['top', 'bottom', 'front', 'back', 'left', 'right']

        textures = [self.location + face + self.format for face in self.faces]

        self.skybox = [
            Quad(self.app, position=(0, 1, 0), rotation=(0, 0, 0),
                 material=Material(texture_path=textures[0])),
            Quad(self.app, position=(0, -1, 0), rotation=(180, 0, 0),
                 material=Material(texture_path=textures[1])),
            Quad(self.app, position=(1, 0, 0), rotation=(0, 90, 0),
                 material=Material(texture_path=textures[2])),
            Quad(self.app, position=(-1, 0, 0), rotation=(0, -90, 0),
                 material=Material(texture_path=textures[3])),
            Quad(self.app, position=(0, 0, 1), rotation=(0, 0, 90),
                 material=Material(texture_path=textures[4])),
            Quad(self.app, position=(0, 0, -1), rotation=(0, 0, -90),
                 material=Material(texture_path=textures[5]))
        ]
