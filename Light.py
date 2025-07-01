import glm

class DirectionalLight:
    def __init__(self, position=(10, 10, 10), color=(0.8, 0.8, 0.8)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.name = 'Directional Light'
        self.type = 'Light'
        self.ambient = 0.3
        self.shininess = 32.0
        self.gamma = 1.1
