import moderngl as mgl
import numpy as np
import pygame as pg
from pyrr import Matrix44, Vector3
import math
from opensimplex.internals import _noise2, _noise3, _init
import os


pg.init()
pg.display.set_mode((1600, 900), pg.OPENGL | pg.DOUBLEBUF)
ctx = mgl.create_context()
ctx.enable(mgl.DEPTH_TEST)
             

perm, _ = _init(seed=16)

prog = ctx.program(
    vertex_shader="""
    
    in vec3 in_position;
    in vec2 in_texcoord;  // Texture coordinates
    in vec3 in_offset;    // Per-instance position
    in vec3 in_color;     // Per-instance color

    uniform mat4 mvp;     // Model-view-projection matrix

    out vec2 fragTexCoord;  // Pass texture coordinates to fragment shader
    out vec3 objcolor;

    void main() {
        vec4 world_pos = vec4(in_position + in_offset, 1.0);
        gl_Position = mvp * world_pos;  // Apply camera transformations
        fragTexCoord = in_texcoord;     // Pass texture coordinates
        objcolor = in_color;
    }
    """,
    fragment_shader="""
    
    out vec4 fragcolor;
    in vec2 fragTexCoord;  // Texture coordinates
    in vec3 objcolor;

    uniform sampler2D texture1;  // The texture sampler

    void main() {
        fragcolor = vec4(objcolor, 1.0) * texture(texture1, fragTexCoord);  // Fetch the texture color
    }
    """,
)

vertices = np.array([
    -0.5, -0.5, -0.5,
    0.5, -0.5, -0.5,
    0.5,  0.5, -0.5,
    -0.5,  0.5, -0.5,

    -0.5, -0.5,  0.5,
    0.5, -0.5,  0.5,
    0.5,  0.5,  0.5,
    -0.5,  0.5,  0.5,

    -0.5, -0.5,  0.5,
    0.5, -0.5,  0.5,
    0.5, -0.5, -0.5,
    -0.5, -0.5, -0.5,

    -0.5,  0.5,  0.5,
    0.5,  0.5,  0.5,
    0.5,  0.5, -0.5,
    -0.5,  0.5, -0.5,

    -0.5, -0.5,  0.5,
    -0.5,  0.5,  0.5,
    -0.5,  0.5, -0.5,
    -0.5, -0.5, -0.5,

    0.5, -0.5,  0.5,
    0.5,  0.5,  0.5,
    0.5,  0.5, -0.5,
    0.5, -0.5, -0.5
], dtype='f4')

uv = np.array([
    0.005, 0.0, 0.5, 0.0,
    0.5, 1.0, 0.005, 1.0,
    0.005, 0.0, 0.5, 0.0,
    0.5, 1.0, 0.005, 1.0,

    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0,


    0.5, 0.0, 1.0, 0.0,
    1.0, 1.0, 0.5, 1.0,

    0.5, 0.0, 0.5, 1.0,
    0.0, 1.0, 0.005, 0.0,

    0.5, 0.0, 0.5, 1.0,
    0.005, 1.0, 0.005, 0.0,
], dtype='f4')

'''uv = np.array([
    0.005, 0.0, 0.5, 0.0,
    0.5, 1.0, 0.005, 1.0,
    0.005, 0.0, 0.5, 0.0,
    0.5, 1.0, 0.005, 1.0,
    0.5, 0.0, 1.0, 0.0,
    1.0, 1.0, 0.5, 1.0,
    0.5, 0.0, 1.0, 0.0,
    1.0, 1.0, 0.5, 1.0,

    0.5, 0.0, 0.5, 1.0,
    0.0, 1.0, 0.005, 0.0,

    0.5, 0.0, 0.5, 1.0,
    0.005, 1.0, 0.005, 0.0,
], dtype='f4')'''

'''
0.0, 0.0, 0.0, 0.0,
0.0, 0.0, 0.0, 0.0,

'''
'''
0.005, 0.0, 0.5, 0.0,
    0.5, 1.0, 0.005, 1.0,
    0.005, 0.0, 0.5, 0.0,
    0.5, 1.0, 0.005, 1.0,
    0.5, 0.0, 1.0, 0.0,
    1.0, 1.0, 0.5, 1.0,
    0.5, 0.0, 1.0, 0.0,
    1.0, 1.0, 0.5, 1.0,

    0.5, 0.0, 0.5, 1.0,
    0.0, 1.0, 0.005, 0.0,

    0.5, 0.0, 0.5, 1.0,
    0.005, 1.0, 0.005, 0.0,
    
'''
indices = np.array([
    0, 1, 2, 0, 2, 3,
    4, 5, 6, 4, 6, 7,
    8, 9, 10, 8, 10, 11,
    12, 13, 14, 12, 14, 15,
    16, 17, 18, 16, 18, 19,
    20, 21, 22, 20, 22, 23
], dtype='u4')

vbo = ctx.buffer(vertices)
tbo = ctx.buffer(uv)
ibo = ctx.buffer(indices)


terrain_size = 510
'''terrain = [[x, int((np.sin(x*0.2) + np.cos(z*0.2)) * 4.9), z]
           for x in range(terrain_size) for z in range(terrain_size)]'''

height = 12.5
width = 1 / height

terrain = [[x, int((np.sin(x * width) + np.cos(z * width)) * height), z]
           for x in range(terrain_size + 1) for z in range(terrain_size + 1)]


def noise2(x, z):
    return _noise2(x, z, perm)


def noise(x, z):
    global height

    island = 1 / (pow(0.0025 * math.hypot(x - terrain_size /
                  2, z - terrain_size/2), 20) + 0.0001)
    island = min(island, 1)

    a1 = height / 2
    a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125

    f1 = 0.005
    f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

    if noise2(0.1 * x, 0.1 * z) < 0:
        a1 /= 1.07

    height = 0
    height += noise2(x * f1, z * f1) * a1 + a1
    height += noise2(x * f2, z * f2) * a2 - a2
    height += noise2(x * f4, z * f4) * a4 + a4
    height += noise2(x * f8, z * f8) * a8 - a8

    height = max(height,  noise2(x * f8, z * f8) + 2)
    height *= island

    return int(height)


'''terrain = [[x, noise(x, z), z]
           for x in range(terrain_size + 1) for z in range(terrain_size + 1)]'''

colors = np.array([1.0, 1.0, 1.0] * len(terrain), dtype='f4')

terrain_positions = np.array(terrain, dtype='f4')
terrain_buffer = ctx.buffer(terrain_positions)
color_buffer = ctx.buffer(colors)


vao = ctx.vertex_array(prog, [
    (vbo, "3f", "in_position"),
    (tbo, "2f", "in_texcoord"),
    (terrain_buffer, "3f/i", "in_offset"),
    (color_buffer, "3f/i", "in_color"),
], index_buffer=ibo)


class Camera:
    def __init__(self, position=Vector3([10, 10, 10]), yaw=-90, pitch=0):
        self.position = position
        self.yaw = yaw
        self.pitch = pitch
        self.front = Vector3([0, 0, -1])
        self.right = Vector3([1, 0, 0])
        self.up = Vector3([0, 1, 0])
        self.update_vectors()

    def update_vectors(self):
        front = Vector3([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
        ])
        self.front = front.normalized
        self.right = Vector3([0, 1, 0]).cross(self.front).normalized
        self.up = self.front.cross(self.right).normalized

    def get_view_matrix(self):
        return Matrix44.look_at(self.position, self.position + self.front, self.up)


camera = Camera(position=[terrain_size / 2, 10, terrain_size / 2])
num_instance = terrain_size ** 2

clock = pg.time.Clock()
running = True
sensitivity = 0.1
speed = 0.1
pg.mouse.set_visible(False)
pg.event.set_grab(True)


def load(path, flip_x=False, flip_y=True, anisotropy=32.0):
    abs_path = os.path.join(os.path.dirname(__file__), path)

    if not os.path.exists(abs_path):
        raise FileNotFoundError(
            f"Lỗi: Không tìm thấy file texture tại {abs_path}")

    texture = pg.image.load(abs_path)
    texture = pg.transform.flip(texture, flip_x=flip_x, flip_y=flip_y)
    texture = ctx.texture(
        size=texture.get_size(),
        components=4,
        data=pg.image.tobytes(texture, 'RGBA', False)
    )
    texture.anisotropy = anisotropy
    texture.build_mipmaps()
    texture.filter = (mgl.NEAREST, mgl.NEAREST)
    return texture


texture = load("assets\img.png")
texture.use(location=0)

proj = Matrix44.perspective_projection(85, 1600 / 900, 0.01, 1000)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    if keys[pg.K_w]:
        camera.position += camera.front * speed
    if keys[pg.K_s]:
        camera.position -= camera.front * speed
    if keys[pg.K_d]:
        camera.position -= camera.right * speed
    if keys[pg.K_a]:
        camera.position += camera.right * speed
    if keys[pg.K_SPACE]:
        camera.position += camera.up * speed
    if keys[pg.K_LSHIFT]:
        camera.position -= camera.up * speed

    dx, dy = pg.mouse.get_rel()
    camera.yaw += dx * sensitivity
    camera.pitch -= dy * sensitivity
    camera.pitch = max(-89, min(89, camera.pitch))
    camera.update_vectors()

    view = camera.get_view_matrix()
    mvp = proj * view

    prog["mvp"].write(mvp.astype("f4"))

    texture.use(location=0)

    ctx.clear(0.1, 0.16, 0.25, 1.0)
    vao.render(mgl.TRIANGLES, instances=num_instance)
    fps = clock.get_fps()
    pg.display.set_caption(
        f'FPS: {fps :.4f} | Num_Voxels : {num_instance} | X, Y, Z: {camera.position}')

    pg.display.flip()
    clock.tick()

pg.quit()
