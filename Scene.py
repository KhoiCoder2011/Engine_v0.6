from Model import *
from Setting import *
from Light import *
from Manager import File

class Scene:
    def __init__(self, app):
        self.app = app
        # self.light = self.app.light
        # self.road = OBJModel(self.app, path = 'assets/meshes/road.obj', material = Material(texture_path='assets/meshes/road.jpg'))
        # self.car = OBJModel(self.app, position = (0, 0.9, 0), rotation = (0, 180, 0), path = 'assets/meshes/tesla.obj')
        self.cube = Cube(self.app, position=(0.0, 2.0, 0.0), script=Script(path = 'Script/Cylinder.py'), material=Material(texture_path='assets/img.png'))
        self.cylinder_1 = Cylinder(self.app, position = (3.0, 0.0, 0.0), material = Material(texture_path='assets/img.png'), script=Script(path='Script/Cylinder.py'))
        self.cylinder_2 = Cylinder(self.app, position = (-3.0, 0.0, 0.0), material = Material(texture_path='assets/img.png'), script=Script(path='Script/Cylinder.py'))
        self.obj = OBJModel(self.app, path='assets/meshes/gun.obj', script=Script(path='Script/Gun.py'))
        self.light_obj = Sphere(self.app, position = (0.0, 1.0, 0.0), script = Script(path = 'Script/Light.py'), material = Material(color = (1.0, 1.0, 0.5)))
        self.light_obj.type = 'Light Object'
        self.light_obj.name = 'Light Object'
        self.objects = [self.cube, self.cylinder_1, self.cylinder_2]
        self.default_objects = [self.light_obj, self.app.light, self.app.camera]
        #Fix self.add_models(File.Load(self.app, save_path).load())
        self.num_obj = len(self.objects)

    def clear(self):
        self.objects.clear()

    def add_model(self, model):
        self.objects.append(model)

    def add_models(self, models):
        self.objects.extend(models)

    def remove(self, model):
        self.objects.remove(model)

    def remove(self, models: list):
        self.objects = [obj for obj in self.objects if obj not in models]

    def render(self):
        for obj in self.objects:
            self.light_obj.render()
            if obj.set_active:
                obj.render()

    def save(self):
        File.Save(self.objects, save_path).save()

    def update(self):
        pass
