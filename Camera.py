from Setting import *
import glfw


speed = SPEED
sensitivity = SENSITIVITY


class Camera:
    def __init__(self, position=(0, 0, 5), front=(0, 0, -1), up=(0, 1, 0), rotation=(0, 180, 0)):
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.forward = glm.vec3(front)
        self.up = glm.vec3(up)
        self.name = "Camera"
        self.type = "Camera"
        self.fov = H_FOV
        self.aspect_ratio = ASPECT_RATIO
        self.near = NEAR
        self.far = FAR

        self.update_projection_matrix()
        self.update_view_matrix()

    def update_view_matrix(self):
        # self.m_view = glm.rotate(glm.mat4(1.0), glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_projection_matrix(self):
        self.m_proj = glm.perspective(glm.radians(self.fov), self.aspect_ratio, self.near, self.far)

    def update(self):
        self.update_view_matrix()
        self.update_projection_matrix()

    def process_keyboard(self, direction, delta_time):
        velocity = speed * delta_time
        if direction == "FORWARD":
            self.position += self.forward * velocity
        elif direction == "BACKWARD":
            self.position -= self.forward * velocity
        elif direction == "UP":
            self.position += self.up * velocity
        elif direction == "DOWN":
            self.position -= self.up * velocity
        elif direction == "LEFT":
            self.position -= glm.normalize(glm.cross(self.forward, self.up)) * velocity
        elif direction == "RIGHT":
            self.position += glm.normalize(glm.cross(self.forward, self.up)) * velocity
    
    def movement(self, keyboard, delta_time):
        if keyboard.is_pressed(glfw.KEY_W):
            self.process_keyboard('FORWARD', delta_time)
        if keyboard.is_pressed(glfw.KEY_S):
            self.process_keyboard('BACKWARD', delta_time)
        if keyboard.is_pressed(glfw.KEY_A):
            self.process_keyboard('LEFT', delta_time)
        if keyboard.is_pressed(glfw.KEY_D):
            self.process_keyboard('RIGHT', delta_time)
        if keyboard.is_pressed(glfw.KEY_E):
            self.process_keyboard('UP', delta_time)
        if keyboard.is_pressed(glfw.KEY_Q):
            self.process_keyboard('DOWN', delta_time)

    def mouse_movement(self, x_offset, y_offset):
        x_offset *= sensitivity
        y_offset *= sensitivity

        self.rotation.y += x_offset
        self.rotation.x += y_offset
        self.rotation.x = glm.clamp(self.rotation.x, -89.9, 89.9)
        self.update_front()

    def update_front(self):
        self.forward = glm.normalize(
            glm.vec3(
                glm.cos(glm.radians(self.rotation.y)) * glm.cos(glm.radians(self.rotation.x)),
                glm.sin(glm.radians(self.rotation.x)),
                glm.sin(glm.radians(self.rotation.y)) * glm.cos(glm.radians(self.rotation.x))
            )
        )

    # def is_point_in_frustum(self, app, point):
    #     point_view = glm.vec4(*point, 1.0)
    #     point_camera = app.camera.m_view * point_view
    #     point_clip = app.camera.m_proj * point_camera

    #     if point_clip.w == 0:
    #         return False

    #     x = point_clip.x / point_clip.w
    #     y = point_clip.y / point_clip.w
    #     z = point_clip.z / point_clip.w

    #     if -1.5 <= x <= 1.5 and -1.5 <= y <= 1.5 and -1.5 <= z <= 1.5:
    #         return True

    #     if glm.length2(app.camera.position - point) <= 16:
    #         return True

    #     return False
