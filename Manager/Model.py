import numpy as np
import math
import mesh_loader
from dataclasses import dataclass, field
import numpy as np


@dataclass
class OBJLoader:
    path: str
    vertices: np.ndarray = field(init=False)
    normals: np.ndarray = field(init=False)
    indices: np.ndarray = field(init=False)
    uv: np.ndarray = field(init=False)

    def __post_init__(self):
        vertices, indices = mesh_loader.load_obj(self.path)
        self.vertices = np.array(
            [coord for v in vertices for coord in (v.x, v.y, v.z)], dtype='f4')
        self.normals = np.array(
            [coord for v in vertices for coord in (v.nx, v.ny, v.nz)], dtype='f4')
        self.indices = np.array(indices, dtype='i4')
        self.uv = np.array(
            [coord for v in vertices for coord in (v.u, v.v)], dtype='f4')


model = {
    'Cube': {
        "vertices": np.array([
            -0.5, -0.5, -0.5,  0.5, -0.5, -0.5,
            0.5,  0.5, -0.5, -0.5,  0.5, -0.5,
            -0.5, -0.5,  0.5,  0.5, -0.5,  0.5,
            0.5,  0.5,  0.5, -0.5,  0.5,  0.5,
            -0.5, -0.5,  0.5,  0.5, -0.5,  0.5,
            0.5, -0.5, -0.5, -0.5, -0.5, -0.5,
            -0.5,  0.5,  0.5,  0.5,  0.5,  0.5,
            0.5,  0.5, -0.5, -0.5,  0.5, -0.5,
            -0.5, -0.5,  0.5, -0.5,  0.5,  0.5,
            -0.5,  0.5, -0.5, -0.5, -0.5, -0.5,
            0.5, -0.5,  0.5,  0.5,  0.5,  0.5,
            0.5,  0.5, -0.5,  0.5, -0.5, -0.5
        ], dtype='f4'),

        "indices": np.array([
            0, 1, 2, 0, 2, 3,
            4, 5, 6, 4, 6, 7,
            8, 9, 10, 8, 10, 11,
            12, 13, 14, 12, 14, 15,
            16, 17, 18, 16, 18, 19,
            20, 21, 22, 20, 22, 23
        ], dtype='u4'),

        "normals": np.array([
            0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
            0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0,
            0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0,
            0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
            -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0,
            1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0
        ], dtype='f4'),

        "uv": np.array([
            0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0
        ], dtype='f4')
    },

    "Quad": {
        "vertices": np.array([
            -0.5, 0.0,  0.5,  0.5, 0.0,  0.5,
            0.5, 0.0, -0.5, -0.5, 0.0, -0.5
        ], dtype='f4'),

        "uv": np.array([
            0.0, 0.0, 1.0, 0.0,
            1.0, 1.0, 0.0, 1.0,
        ], dtype='f4'),

        "normals": np.array([
            0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
            0.0, 1.0, 0.0, 0.0, 1.0, 0.0
        ], dtype='f4'),

        "indices": np.array([
            0, 1, 2, 2, 3, 0
        ], dtype='u4')
    }
}


@dataclass
class CubeModel:
    vertices: np.ndarray = field(init=False)
    uv: np.ndarray = field(init=False)
    normals: np.ndarray = field(init=False)
    indices: np.ndarray = field(init=False)

    def __post_init__(self):
        self.vertices = model['Cube']['vertices']
        self.uv = model['Cube']['uv']
        self.normals = model['Cube']['normals']
        self.indices = model['Cube']['indices']


@dataclass
class QuadModel:
    vertices: np.ndarray = field(init=False)
    uv: np.ndarray = field(init=False)
    indices: np.ndarray = field(init=False)
    normals: np.ndarray = field(init=False)

    def __post_init__(self):
        self.vertices = model['Quad']['vertices']
        self.uv = model['Quad']['uv']
        self.indices = model['Quad']['indices']
        self.normals = model['Quad']['normals']


@dataclass
class SphereModel:
    radius: int = 1
    lat_count: int = 100
    lon_count: int = 100
    vertices: np.ndarray = field(init=False)
    uv: np.ndarray = field(init=False)
    normals: np.ndarray = field(init=False)
    indices: np.ndarray = field(init=False)

    def __post_init__(self):
        vertex_list = []
        normal_list = []
        uv_list = []
        index_list = []
        pi = math.pi

        for i in range(self.lat_count + 1):
            phi = pi * i / self.lat_count
            for j in range(self.lon_count + 1):
                theta = 2.0 * pi * j / self.lon_count
                x = self.radius * math.sin(phi) * math.cos(theta)
                y = self.radius * math.sin(phi) * math.sin(theta)
                z = self.radius * math.cos(phi)
                vertex_list.append((x, y, z))
                length = math.sqrt(x ** 2 + y ** 2 + z ** 2)
                normal_list.append((x / length, y / length, z / length))
                u = j / self.lon_count
                v = i / self.lat_count
                uv_list.append((u, v))

        for i in range(self.lat_count):
            for j in range(self.lon_count):
                first = i * (self.lon_count + 1) + j
                second = first + self.lon_count + 1
                if i != 0:
                    index_list.extend([first, second, first + 1])
                if i != self.lat_count - 1:
                    index_list.extend([first + 1, second, second + 1])

        self.vertices = np.array(vertex_list, dtype='f4')
        self.normals = np.array(normal_list, dtype='f4')
        self.uv = np.array(uv_list, dtype='f4')
        self.indices = np.array(index_list, dtype='u4')


@dataclass
class CylinderModel:
    radius: float = 1.0
    height: float = 2.0
    segments: int = 64
    vertices: np.ndarray = field(init=False)
    uv: np.ndarray = field(init=False)
    normals: np.ndarray = field(init=False)
    indices: np.ndarray = field(init=False)

    def __post_init__(self):
        vertex_list = []
        normal_list = []
        uv_list = []
        index_list = []

        half_height = self.height / 2.0
        angle_step = 2 * math.pi / self.segments

        for i in range(self.segments + 1):
            angle = i * angle_step
            x = self.radius * math.cos(angle)
            z = self.radius * math.sin(angle)

            vertex_list.append((x, -half_height, z))
            normal_list.append((x, 0.0, z) if self.radius !=
                               0 else (0.0, 0.0, 0.0))
            uv_list.append((i / self.segments, 0.0))

            vertex_list.append((x, half_height, z))
            normal_list.append((x, 0.0, z) if self.radius !=
                               0 else (0.0, 0.0, 0.0))
            uv_list.append((i / self.segments, 1.0))

        for i in range(self.segments):
            base = i * 2
            index_list.extend([base, base + 1, base + 2])
            index_list.extend([base + 1, base + 3, base + 2])

        bottom_center_index = len(vertex_list)
        vertex_list.append((0.0, -half_height, 0.0))
        normal_list.append((0.0, -1.0, 0.0))
        uv_list.append((0.5, 0.5))

        for i in range(self.segments):
            v0 = i * 2
            v1 = ((i + 1) % self.segments) * 2
            index_list.extend([bottom_center_index, v1, v0])

        top_center_index = len(vertex_list)
        vertex_list.append((0.0, half_height, 0.0))
        normal_list.append((0.0, 1.0, 0.0))
        uv_list.append((0.5, 0.5))

        for i in range(self.segments):
            v0 = i * 2 + 1
            v1 = ((i + 1) % self.segments) * 2 + 1
            index_list.extend([top_center_index, v0, v1])

        self.vertices = np.array(vertex_list, dtype='f4')
        self.normals = np.array(
            [tuple(np.array(n) / np.linalg.norm(n)) for n in normal_list], dtype='f4')
        self.uv = np.array(uv_list, dtype='f4')
        self.indices = np.array(index_list, dtype='u4')


@dataclass
class GridModel:
    grid_size: int = 100
    grid_spacing: float = 1.0
    vertices: np.ndarray = field(init=False)
    indices: np.ndarray = field(init=False)
    normals: np.ndarray = field(init=False)
    uv: np.ndarray = field(init=False)
    colors: np.ndarray = field(init=False)

    def __post_init__(self):
        self.generate_grid()

    def generate_grid(self):
        lines = []
        index_list = []
        color_list = []
        for i in range(-self.grid_size, self.grid_size + 1):

            lines.append([i * self.grid_spacing, 0, -
                         self.grid_size * self.grid_spacing])
            lines.append([i * self.grid_spacing, 0,
                         self.grid_size * self.grid_spacing])
            index_list.extend([len(lines) - 2, len(lines) - 1])

            if i == 0:
                color = [1.0, 0.0, 0.0, 1.0]
            else:
                color = [0.5, 0.5, 0.5, 1.0]
            color_list.extend([color, color])

            lines.append([-self.grid_size * self.grid_spacing,
                         0, i * self.grid_spacing])
            lines.append([self.grid_size * self.grid_spacing,
                         0, i * self.grid_spacing])
            index_list.extend([len(lines) - 2, len(lines) - 1])

            if i == 0:
                color = [0.0, 0.0, 1.0, 1.0]
            else:
                color = [0.5, 0.5, 0.5, 1.0]
            color_list.extend([color, color])

        self.vertices = np.array(lines, dtype='f4')
        self.indices = np.array(index_list, dtype='u4')
        num_vertices = len(lines)
        self.normals = np.tile(
            [0.0, 1.0, 0.0], (num_vertices, 1)).astype('f4').flatten()
        self.uv = np.tile([0.0, 0.0], (num_vertices, 1)).astype('f4').flatten()
        self.colors = np.array(color_list, dtype='f4').flatten()
