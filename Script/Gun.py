from Manager.Audio import Audio
import glfw

audio = Audio('assets/gun_sound.wav')
def start(app, obj): ...

def update(app, obj):
    if app.keyboard.is_pressed(glfw.KEY_SPACE):
        audio.play()