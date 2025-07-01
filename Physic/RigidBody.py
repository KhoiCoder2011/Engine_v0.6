import glm

SCALE = 10 ** 5
GRAVITY = -9.81 / SCALE


class Rigidbody:
    def __init__(self, object):
        self.object = object
        self.position = object.position
        self.velocity = glm.vec3(0)
        self.acceleration = glm.vec3(0)
        self.is_gravity = True

    def update(self, time):
        if self.is_gravity:
            self.acceleration.y = GRAVITY
            self.velocity += self.acceleration * time
            self.position += self.velocity * time
            if self.position.y <= 0:
                self.position.y = 0
                self.velocity.y = 0