import configparser
import os
import moderngl as mgl
import glm
import platform

ENGINE_VER = '1.0'
save_path = f'{os.path.join(os.path.dirname(__file__))}/data.json'
config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.ini')
ENGINE_NAME = 'Meshcraft Engine'
PLATFORM = platform.platform()
config = configparser.ConfigParser()
config.read(config_path)

if not config.sections():
    raise FileNotFoundError(
        f"Error: Configuration file not found or could not be read: {config_path}")


def get_value(section, option, value_type, default=None):
    try:
        if value_type == int:
            return config.getint(section, option)
        elif value_type == float:
            return config.getfloat(section, option)
        elif value_type == bool:
            return config.getboolean(section, option)
        else:
            return config.get(section, option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        print(
            f"Warning: [{section}] {option} not found, using default value: {default}")
        return default


RES = glm.vec2(get_value('Window', 'res_x', int, 1650),
               get_value('Window', 'res_y', int, 900))

DISPLAY_RES = glm.vec2(get_value('Window', 'display_x', int, 958),
                       get_value('Window', 'display_y', int, 501))

render_mode = mgl.TRIANGLES  # mgl.LINE_STRIP

WIDTH, HEIGHT = int(RES.x), int(RES.y)
DISPLAY_WIDTH, DISPLAY_HEIGHT = int(DISPLAY_RES.x), int(DISPLAY_RES.y)

ASPECT_RATIO = DISPLAY_RES.x / DISPLAY_RES.y

RESOLUTION = (WIDTH, HEIGHT)
DISPLAY_RESOLUTION = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

SENSITIVITY = get_value('Camera', 'sensitivity', float, 0.08)
SPEED = get_value('Camera', 'speed', float, 4.0)

H_FOV = get_value('Camera', 'h_fov', float, 85.0)
V_FOV = glm.degrees(2 * glm.atan(glm.tan(glm.radians(H_FOV / 2)) * 1 / ASPECT_RATIO))

NEAR = get_value('Camera', 'near', float, 0.01)
FAR = get_value('Camera', 'far', float, 1000.0)

BG_COLOR = glm.vec3(
    get_value('Window', 'r', float, 0.1),
    get_value('Window', 'g', float, 0.16),
    get_value('Window', 'b', float, 0.25)
)

GL_MAJOR = get_value('Graphics', 'gl_major', int, 4)
GL_MINOR = get_value('Graphics', 'gl_minor', int, 6)
