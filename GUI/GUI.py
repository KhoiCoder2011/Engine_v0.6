import imgui
import glm
from imgui.integrations.glfw import GlfwRenderer
from PIL import Image
import os


def setup_imgui_style():
    style = imgui.get_style()
    colors = style.colors

    colors[imgui.COLOR_WINDOW_BACKGROUND] = [0.13, 0.14, 0.17, 1.00]
    colors[imgui.COLOR_TITLE_BACKGROUND] = [0.09, 0.10, 0.12, 1.00]
    colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = [0.13, 0.14, 0.17, 1.00]
    colors[imgui.COLOR_TITLE_BACKGROUND_COLLAPSED] = [0.09, 0.10, 0.12, 0.75]
    colors[imgui.COLOR_HEADER] = [0.20, 0.22, 0.27, 1.00]
    colors[imgui.COLOR_HEADER_HOVERED] = [0.30, 0.33, 0.40, 1.00]
    colors[imgui.COLOR_HEADER_ACTIVE] = [0.25, 0.28, 0.35, 1.00]
    colors[imgui.COLOR_BUTTON] = [0.20, 0.22, 0.27, 1.00]
    colors[imgui.COLOR_BUTTON_HOVERED] = [0.30, 0.33, 0.40, 1.00]
    colors[imgui.COLOR_BUTTON_ACTIVE] = [0.25, 0.28, 0.35, 1.00]
    colors[imgui.COLOR_FRAME_BACKGROUND] = [0.16, 0.17, 0.20, 1.00]
    colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = [0.20, 0.22, 0.27, 1.00]
    colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = [0.25, 0.28, 0.35, 1.00]
    colors[imgui.COLOR_TAB] = [0.13, 0.14, 0.17, 1.00]
    colors[imgui.COLOR_TAB_HOVERED] = [0.30, 0.33, 0.40, 1.00]
    colors[imgui.COLOR_TAB_ACTIVE] = [0.20, 0.22, 0.27, 1.00]
    colors[imgui.COLOR_TAB_UNFOCUSED] = [0.13, 0.14, 0.17, 1.00]
    colors[imgui.COLOR_TAB_UNFOCUSED_ACTIVE] = [0.16, 0.17, 0.20, 1.00]
    colors[imgui.COLOR_SEPARATOR] = [0.20, 0.22, 0.27, 1.00]
    colors[imgui.COLOR_SEPARATOR_HOVERED] = [0.30, 0.33, 0.40, 1.00]
    colors[imgui.COLOR_SEPARATOR_ACTIVE] = [0.25, 0.28, 0.35, 1.00]
    colors[imgui.COLOR_RESIZE_GRIP] = [0.20, 0.22, 0.27, 1.00]
    colors[imgui.COLOR_RESIZE_GRIP_HOVERED] = [0.30, 0.33, 0.40, 1.00]
    colors[imgui.COLOR_RESIZE_GRIP_ACTIVE] = [0.25, 0.28, 0.35, 1.00]
    colors[imgui.COLOR_CHECK_MARK] = [0.30, 0.80, 0.40, 1.00]
    colors[imgui.COLOR_SLIDER_GRAB] = [0.30, 0.33, 0.40, 1.00]
    colors[imgui.COLOR_SLIDER_GRAB_ACTIVE] = [0.25, 0.28, 0.35, 1.00]
    colors[imgui.COLOR_TEXT] = [0.90, 0.92, 0.95, 1.00]
    colors[imgui.COLOR_TEXT_DISABLED] = [0.50, 0.55, 0.60, 1.00]
    colors[imgui.COLOR_POPUP_BACKGROUND] = [0.13, 0.14, 0.17, 0.95]
    colors[imgui.COLOR_SCROLLBAR_BACKGROUND] = [0.13, 0.14, 0.17, 1.00]
    colors[imgui.COLOR_SCROLLBAR_GRAB] = [0.20, 0.22, 0.27, 1.00]
    colors[imgui.COLOR_SCROLLBAR_GRAB_HOVERED] = [0.30, 0.33, 0.40, 1.00]
    colors[imgui.COLOR_SCROLLBAR_GRAB_ACTIVE] = [0.25, 0.28, 0.35, 1.00]
    colors[imgui.COLOR_DRAG_DROP_TARGET] = [0.30, 0.80, 0.40, 1.00]
    colors[imgui.COLOR_PLOT_LINES] = [0.61, 0.61, 0.61, 1.00]
    colors[imgui.COLOR_PLOT_LINES_HOVERED] = [1.00, 0.43, 0.35, 1.00]
    colors[imgui.COLOR_PLOT_HISTOGRAM] = [0.90, 0.70, 0.00, 1.00]
    colors[imgui.COLOR_PLOT_HISTOGRAM_HOVERED] = [1.00, 0.60, 0.00, 1.00]

    style.window_rounding = 8.0
    style.child_rounding = 6.0
    style.frame_rounding = 6.0
    style.grab_rounding = 6.0
    style.popup_rounding = 6.0
    style.scrollbar_rounding = 8.0
    style.tab_rounding = 6.0
    style.window_border_size = 1.0
    style.frame_border_size = 1.0
    style.popup_border_size = 1.0
    style.window_padding = (10, 10)
    style.frame_padding = (8, 4)
    style.item_spacing = (8, 6)
    style.item_inner_spacing = (6, 4)
    style.indent_spacing = 20
    style.alpha = 1.0


class GUI:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.window = app.window
        imgui.create_context()
        setup_imgui_style()
        self.impl = GlfwRenderer(self.window)

        self.components = [
            'Rigidbody',
            'Script',
            'Material'
        ]

        self.show_window = True
        self.scene = app.scene
        self.objects = self.scene.objects
        self.default_objects = self.scene.default_objects
        self.all_objects = self.objects + self.default_objects
        self.selected_object = None
        self.selected_resource = None
        self.max_fps = 0
        self.texture_map = {}
        self.load_textures()

    def load_texture(self, path):
        img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
        texture = self.ctx.texture(img.size, 4, img.tobytes())
        texture.build_mipmaps()
        return texture

    def load_textures(self):
        self.texture_map["grass_top"] = self.load_texture(
            "assets/grass_top.png")

    def quality_performance(self):
        imgui.set_next_window_position(0, 19)
        imgui.set_next_window_size(300, 135)
        imgui.begin("Performance", flags=imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_BACKGROUND |
                    imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_MOVE)
        fps = self.app.fps

        if fps < 30:
            color = (1.0, 0.0, 0.0, 1.0)
        elif 30 <= fps <= 120:
            color = (1.0, 0.87, 0.35, 1.0)
        else:
            color = (0.0, 1.0, 0.0, 1.0)

        imgui.text_colored(f'FPS: {fps:.3f}', *color)
        imgui.same_line()
        imgui.text("|")
        imgui.same_line()
        imgui.text(f"Max FPS: {self.max_fps :.3f}")

        imgui.separator()
        imgui.text(f'Delta Time : {1000 / fps :.3f} ms')
        imgui.text(f'Time : {self.app.time :.3f} s')
        imgui.text(f"Objects: {len(self.objects)}")
        self.max_fps = max(fps, self.max_fps)
        imgui.end()

    def object_manager(self):
        imgui.set_next_window_position(0, 130)
        imgui.set_next_window_size(300, 500)
        imgui.begin("Hierarchy", flags=imgui.WINDOW_NO_RESIZE |
                    imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_MOVE)

        imgui.text_colored("Game Objects", 0.7, 0.9, 1.0, 1.0)
        imgui.separator()

        if imgui.button("Add Object", width=imgui.get_content_region_available()[0]):
            imgui.open_popup("add_object_popup")

        if imgui.begin_popup("add_object_popup"):
            imgui.text("Feature coming soon...")
            imgui.end_popup()

        imgui.begin_child("object_list", width=0, height=0, border=False)
        for obj in self.all_objects:
            is_selected = (self.selected_object == obj)
            clicked, _ = imgui.selectable(obj.name, is_selected)
            if clicked:
                self.selected_object = obj
        imgui.end_child()
        imgui.end()

    def resource_window(self):
        imgui.set_next_window_position(0, 630)
        imgui.set_next_window_size(1350, 270)
        imgui.begin("Resources", flags=imgui.WINDOW_NO_RESIZE |
                    imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_MOVE)

        imgui.text_colored("Assets", 0.7, 0.9, 1.0, 1.0)
        imgui.separator()

        if not hasattr(self, 'assets'):
            self.assets = {
                "models": ['car.obj'],
                "texture": ['grass_top']
            }
        if not hasattr(self, 'model_path_input'):
            self.model_path_input = ""
        if not hasattr(self, 'texture_path_input'):
            self.texture_path_input = ""
        if not hasattr(self, 'resource_tab'):
            self.resource_tab = 0

        if imgui.begin_tab_bar("assets_tabs"):
            if imgui.begin_tab_item("Models")[0]:
                columns = 6
                imgui.columns(columns, "models_columns", border=False)
                for item in self.assets["models"]:
                    imgui.text(item)
                    if imgui.is_item_clicked():
                        self.selected_resource = ("models", item)
                    imgui.next_column()
                imgui.columns(1)
                imgui.separator()
                imgui.text_colored("Feature", 0.8, 1.0, 0.7, 1.0)
                imgui.spacing()
                if imgui.button("Add Model"):
                    imgui.open_popup("add_model_popup")
                if imgui.begin_popup("add_model_popup"):
                    imgui.text("Import Model")
                    imgui.spacing()
                    changed, self.model_path_input = imgui.input_text(
                        "Model Path (.obj)", self.model_path_input, 512)
                    if imgui.button("Import Model", width=imgui.get_content_region_available()[0]):
                        file_path = self.model_path_input.strip()
                        if file_path and file_path.lower().endswith(".obj"):
                            filename = os.path.basename(file_path)
                            if filename not in self.assets["models"]:
                                self.assets["models"].append(filename)
                        self.model_path_input = ""
                        imgui.close_current_popup()
                    imgui.end_popup()
                imgui.end_tab_item()

            if imgui.begin_tab_item("Textures")[0]:
                columns = 6
                imgui.columns(columns, "textures_columns", border=False)
                for item in self.assets["texture"]:
                    if item in self.texture_map:
                        texture = self.texture_map[item]
                        imgui.image(texture.glo if hasattr(
                            texture, 'glo') else texture.texture_id, 64, 64)
                        imgui.text(item)
                    else:
                        imgui.text(item)
                    if imgui.is_item_clicked():
                        self.selected_resource = ("texture", item)
                    imgui.next_column()
                imgui.columns(1)
                imgui.separator()
                imgui.text_colored("Feature", 0.8, 1.0, 0.7, 1.0)
                imgui.spacing()
                if imgui.button("Add Texture"):
                    imgui.open_popup("add_texture_popup")
                if imgui.begin_popup("add_texture_popup"):
                    imgui.text("Import Texture")
                    imgui.spacing()
                    _, self.texture_path_input = imgui.input_text("Texture Path (.png)", self.texture_path_input, 512)
                    if imgui.button("Import Texture", width=imgui.get_content_region_available()[0]):
                        file_path = self.texture_path_input.strip()
                        if file_path and file_path.lower().endswith(".png"):
                            filename = os.path.splitext(os.path.basename(file_path))[0]
                            if filename not in self.assets["texture"]:
                                self.assets["texture"].append(filename)
                                self.texture_map[filename] = self.load_texture(file_path)
                        self.texture_path_input = ""
                        imgui.close_current_popup()
                    imgui.end_popup()
                imgui.end_tab_item()
            imgui.end_tab_bar()

        imgui.spacing()
        if self.selected_resource:
            category, resource = self.selected_resource
            imgui.separator()
            imgui.text_colored("Asset Info", 0.9, 0.8, 0.5, 1.0)
            imgui.spacing()
            imgui.text(f"Type: {category.capitalize()}")
            imgui.text(f"Name: {resource}")
            if category == "texture" and resource in self.texture_map:
                texture = self.texture_map[resource]
                imgui.image(texture.glo if hasattr(texture, 'glo')
                            else texture.texture_id, 128, 128)
                img = texture
                imgui.text(f"Size: {img.size[0]} x {img.size[1]}")
            elif category == "models":
                imgui.text("Model preview not available.")
            imgui.spacing()
            if imgui.button("Delete Asset", width=imgui.get_content_region_available()[0]):
                if resource in self.assets[category]:
                    self.assets[category].remove(resource)
                    if category == "texture" and resource in self.texture_map:
                        del self.texture_map[resource]
                    self.selected_resource = None
        imgui.end()

    def _end(self):
        imgui.spacing()
        imgui.separator()
        imgui.dummy(0, 15)

    def inspector_window(self):
        imgui.set_next_window_position(1350, 0)
        imgui.set_next_window_size(300, 900)
        imgui.begin("Inspector", flags=imgui.WINDOW_NO_RESIZE |
                    imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_MOVE)

        if self.selected_object and self.selected_object in self.objects:
            obj = self.selected_object

            imgui.text_colored("General", 1.0, 1.0, 0.3, 1.0)
            imgui.separator()

            changed, new_name = imgui.input_text("Name", obj.name, 256)
            if changed:
                obj.name = new_name

            imgui.text(f"Type: {obj.type}")
            changed, set_active = imgui.checkbox("Set Active", obj.set_active)
            if changed:
                obj.set_active = set_active

            self._end()

            imgui.text_colored("Transform", 0.3, 1.0, 0.6, 1.0)
            imgui.separator()

            changed, position = imgui.input_float3("Position", *obj.position)
            if changed:
                obj.position = glm.vec3(*position)

            changed, new_rot = imgui.input_float3("Rotation", *obj.rotation)
            if changed:
                obj.rotation = glm.vec3(*new_rot)

            changed, new_scale = imgui.input_float3("Scale", *obj.scale)
            if changed:
                obj.scale = glm.vec3(*new_scale)

            self._end()

            imgui.text_colored("Physics", 0.6, 0.8, 1.0, 1.0)
            imgui.separator()

            imgui.text(f"Velocity: {tuple(obj.rigidbody.velocity)}")

            self._end()

            imgui.text_colored("Metadata", 0.8, 0.8, 1.0, 1.0)
            imgui.separator()

            changed, new_tag = imgui.input_text("Tag", obj.tag, 256)
            if changed:
                obj.tag = new_tag

            changed, new_id = imgui.input_text("ID", obj.id, 256)
            if changed:
                obj.id = new_id

            self._end()

            imgui.text_colored("Model Matrix", 1.0, 0.6, 0.6, 1.0)
            imgui.separator()

            imgui.begin_child("Matrix", width=0, height=100, border=True)
            imgui.text(self.matrix_to_string(obj.m_model))
            imgui.end_child()

            self._end()

            self.feature(obj)

        if self.selected_object and self.selected_object in self.default_objects:
            obj = self.selected_object

            if obj.type == "Camera":
                imgui.text_colored("Camera", 1.0, 0.6, 0.6, 1.0)
                imgui.separator()

                changed, position = imgui.input_float3(
                    "Position", *obj.position)
                if changed:
                    obj.position = glm.vec3(*position)

                changed, rotation = imgui.input_float3(
                    "Rotation", *obj.rotation)
                if changed:
                    obj.rotation = glm.vec3(*rotation)

                changed, fov = imgui.input_float("FOV", obj.fov)
                if changed:
                    obj.fov = fov

                changed, near = imgui.input_float("Near", obj.near)
                if changed:
                    obj.near = near

                changed, far = imgui.input_float("Far", obj.far)
                if changed:
                    obj.far = far

                self._end()

                imgui.text_colored("Projection Matrix", 1.0, 0.6, 0.6, 1.0)
                imgui.separator()

                imgui.begin_child("Projection Matrix",
                                  width=0, height=100, border=True)
                imgui.text(self.matrix_to_string(obj.m_proj))
                imgui.end_child()

                self._end()

                imgui.text_colored("View Matrix", 1.0, 0.6, 0.6, 1.0)
                imgui.separator()
                imgui.begin_child("View Matrix", width=0,
                                  height=100, border=True)
                imgui.text(self.matrix_to_string(obj.m_view))
                imgui.end_child()

            if obj.type == "Light":
                obj = self.app.light
                imgui.text_colored("Light", 1.0, 0.6, 0.6, 1.0)
                imgui.separator()

                changed, position = imgui.input_float3(
                    "Position", *obj.position)
                if changed:
                    obj.position = glm.vec3(*position)

                changed, color = imgui.color_edit3("Color", *obj.color)
                if changed:
                    obj.color = glm.vec3(*color)

                changed, ambient = imgui.input_float("Ambient", obj.ambient)
                if changed:
                    obj.ambient = ambient

                changed, shininess = imgui.input_float(
                    "Shininess", obj.shininess)
                if changed:
                    obj.shininess = shininess

                self._end()

        imgui.end()

    def feature(self, obj):
        imgui.spacing()
        if imgui.button("Add Component", width=imgui.get_content_region_available()[0]):
            imgui.open_popup("add_component_popup")

        if imgui.begin_popup("add_component_popup"):
            imgui.begin_child("component_list_child",
                              width=300, height=200, border=True)

            for name in self.components:
                clicked, _ = imgui.menu_item(name)
                if clicked:
                    print(f"Added component: {name}")

            imgui.end_child()
            imgui.end_popup()

        imgui.spacing()
        if imgui.button("Delete", width=imgui.get_content_region_available()[0]):
            self.objects.remove(obj)
            self.selected_object = None
            self.all_objects = self.objects + self.default_objects

    def menu_bar(self):
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                if imgui.menu_item("Save")[0]:
                    self.scene.save()
                if imgui.menu_item("Save As")[0]:
                    '''self.scene.save_as() Add path to save'''
                    pass
                if imgui.menu_item("Build and Run")[0]:
                    pass
                imgui.end_menu()

            if imgui.begin_menu("Setting", True):
                if imgui.menu_item("Config Engine")[0]:
                    pass
                imgui.end_menu()

            if imgui.begin_menu("Tool", True):
                if imgui.menu_item("Code Editor")[0]:
                    pass
                imgui.end_menu()

            if imgui.begin_menu("Help", True):
                if imgui.menu_item("About")[0]:
                    imgui.open_popup("AboutPopup")
                imgui.end_menu()
            imgui.end_main_menu_bar()

        if imgui.begin_popup("AboutPopup"):
            imgui.text("Game Engine v1.0")
            imgui.text("Powered by Python + Dear ImGui")
            imgui.separator()
            if imgui.button("Close"):
                imgui.close_current_popup()
            imgui.end_popup()

    def matrix_to_string(self, matrix):
        return "\n".join([f"{matrix[i][0]:.2f}\t{matrix[i][1]:.2f}\t{matrix[i][2]:.2f}\t{matrix[i][3]:.2f}" for i in range(4)])

    def render(self):
        self.impl.process_inputs()

        imgui.new_frame()

        self.menu_bar()
        self.quality_performance()
        self.object_manager()
        self.resource_window()
        self.inspector_window()

        imgui.render()
        self.impl.render(imgui.get_draw_data())
