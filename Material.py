import glm


class Material:
    def __init__(self, color = (1.0, 1.0, 1.0, 1.0), texture_path: str = 'assets/blank.png'):
        self.texture_path = texture_path
        self.color = glm.vec3(color[0], color[1], color[2])
        self.alpha = color[3] if len(color) == 4 else 1.0