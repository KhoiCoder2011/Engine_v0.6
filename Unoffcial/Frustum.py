import glm
import math
from Setting import *


class Furstum:
    def __init__(self, camera):
        self.position = camera.position
        self.front = camera.forward
        self.up = camera.up
        self.h_fov = H_FOV
        self.v_fov = V_FOV
        self.near_plane = NEAR
        self.far_plane = FAR
        self.aspect_ratio = ASPECT_RATIO

    def world_to_camera_space(self, camera, object_pos):
        view_matrix = camera.m_view
        object_in_camera_space = glm.vec4(object_pos, 1.0)
        return view_matrix * object_in_camera_space

    def is_object_in_fov(self, camera, object_pos):

        object_in_camera_space = self.world_to_camera_space(camera, object_pos)

        z = object_in_camera_space.z

        if z < self.near_plane or z > self.far_plane:
            return False

        max_x = math.tan(glm.radians(self.h_fov) / 2) * z
        max_y = math.tan(glm.radians(self.v_fov) / 2) * z

        if abs(object_in_camera_space.x) > max_x or abs(object_in_camera_space.y) > max_y:
            return False

        return True

