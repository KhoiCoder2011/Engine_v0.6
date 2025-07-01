import imgui
import glfw
from imgui.integrations.glfw import GlfwRenderer
import moderngl
import time


class CodeEditorApp:
    def __init__(self, width=1280, height=720, title="ImGui Code Editor with Menu Bar"):
        if not glfw.init():
            raise RuntimeError("Could not initialize GLFW")
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Could not create GLFW window")
        glfw.make_context_current(self.window)
        imgui.create_context()
        self.renderer = GlfwRenderer(self.window)
        self.code_text = """def hello_world():\n    print(\"Hello, World!\")"""
        self.show_about = False
        self.frame_time = 1.0 / 60.0
        self.running = True
        glfw.set_input_mode(self.window, glfw.STICKY_KEYS, glfw.TRUE)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)
        # Move ModernGL context creation after ImGui renderer
        self.ctx = moderngl.create_context()
        glfw.focus_window(self.window)
        glfw.swap_interval(1)

    def update(self):
        start_time = time.time()
        glfw.poll_events()
        self.ctx.clear(color=(0.1, 0.1, 0.1, 1.0))
        imgui.new_frame()
        self.draw_menu_bar()
        self.draw_code_editor()
        self.draw_about_popup()
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
        glfw.swap_buffers(self.window)
        elapsed = time.time() - start_time

    def draw_menu_bar(self):
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                if imgui.menu_item("New")[0]:
                    self.code_text = ""
                if imgui.menu_item("Open")[0]:
                    pass  # Implement file open dialog if needed
                if imgui.menu_item("Save")[0]:
                    pass  # Implement file save dialog if needed
                imgui.end_menu()
            if imgui.begin_menu("Edit", True):
                if imgui.menu_item("Undo")[0]:
                    pass  # Implement undo
                if imgui.menu_item("Redo")[0]:
                    pass  # Implement redo
                imgui.end_menu()
            if imgui.begin_menu("Help", True):
                if imgui.menu_item("About")[0]:
                    self.show_about = True
                imgui.end_menu()
            imgui.end_main_menu_bar()

    def draw_code_editor(self):
        imgui.begin("Code Editor")
        changed, self.code_text = imgui.input_text_multiline(
            "##CodeEditor", self.code_text, 4096, height=400)
        imgui.end()

    def draw_about_popup(self):
        if self.show_about:
            imgui.open_popup("AboutPopup")
            self.show_about = False
        if imgui.begin_popup("AboutPopup"):
            imgui.text("ImGui Code Editor Example")
            imgui.text("Powered by Python + Dear ImGui")
            imgui.separator()
            if imgui.button("Close"):
                imgui.close_current_popup()
            imgui.end_popup()

    def run(self):
        while not glfw.window_should_close(self.window) and self.running:
            self.update()
        self.shutdown()

    def shutdown(self):
        self.renderer.shutdown()
        glfw.terminate()


def main():
    app = CodeEditorApp()
    app.run()


if __name__ == "__main__":
    main()
