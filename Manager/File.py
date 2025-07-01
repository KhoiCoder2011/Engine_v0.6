import json
from Model import *
from Texture import *


class Save:
    def __init__(self, objects, path: str):
        self.objects = objects
        self.path = path

    def save(self):
        object_dicts = [obj.to_dict() for obj in self.objects]
        with open(self.path, 'w+') as file:
            json.dump(object_dicts, file, indent=4)


class Load:
    def __init__(self, app, path: str):
        self.app = app
        self.path = path
        self.class_map = {
            "Cube": Cube,
            "OBJModel": OBJModel,
            "Quad": Quad,
            "Sphere": Sphere
        }

    def load(self):
        with open(self.path, 'r') as file:
            file_content = file.read().strip()

        if file_content == '[]' or file_content == '':
            return []
        try:
            data = json.loads(file_content)
        except json.JSONDecodeError:
            print(f"Error: The file {self.path} is not a valid JSON.")
            return []

        return [self._load_model(line) for line in data]

    def _load_model(self, line):
        position = line['position']
        rotation = line['rotation']
        scale = line['scale']
        color = line['color']
        model_type = line['type']
        tag = line['tag']
        name = line['name']
        texture_path = line['texture_path']
        model_path = line['model_path']
        model_id = line['id']
        set_active = line['set_active']

        model = self.class_map[model_type](
            self.app, position, rotation, scale, color
        )

        if model_type == "OBJModel":
            model.path = model_path
        
        model.texture_path = texture_path
        model.tag = tag
        model.id = model_id
        model.set_active = set_active
        model.name = name

        return model
