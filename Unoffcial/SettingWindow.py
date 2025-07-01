import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import configparser
from Setting import *


class SettingsWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename='darkly')
        self.title("Engine Settings")
        self.geometry("550x550")
        self.resizable(False, False)

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=15, pady=15, fill="both", expand=True)

        self.window_label = ttk.Label(
            self.main_frame, text="Window Settings", font=("Arial", 12, "bold"))
        self.window_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        self.res_width_label = ttk.Label(self.main_frame, text="Width:")
        self.res_width_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.res_width_entry = ttk.Entry(self.main_frame, width=10)
        self.res_width_entry.insert(0, str(RESOLUTION[0]))
        self.res_width_entry.grid(row=1, column=1, padx=10, pady=5)

        self.res_height_label = ttk.Label(self.main_frame, text="Height:")
        self.res_height_label.grid(
            row=1, column=2, sticky="e", padx=10, pady=5)
        self.res_height_entry = ttk.Entry(self.main_frame, width=10)
        self.res_height_entry.insert(0, str(RESOLUTION[1]))
        self.res_height_entry.grid(row=1, column=3, padx=10, pady=5)

        self.display_x_label = ttk.Label(self.main_frame, text="Display X:")
        self.display_x_label.grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.display_x_entry = ttk.Entry(self.main_frame, width=10)
        self.display_x_entry.insert(0, str(DISPLAY_WIDTH))
        self.display_x_entry.grid(row=3, column=1, padx=10, pady=5)

        self.display_y_label = ttk.Label(self.main_frame, text="Display Y:")
        self.display_y_label.grid(row=3, column=2, sticky="e", padx=10, pady=5)
        self.display_y_entry = ttk.Entry(self.main_frame, width=10)
        self.display_y_entry.insert(0, str(DISPLAY_HEIGHT))
        self.display_y_entry.grid(row=3, column=3, padx=10, pady=5)

        self.bg_color_label = ttk.Label(
            self.main_frame, text="Background Color (R, G, B):", font=("Arial", 10, "bold"))
        self.bg_color_label.grid(row=5, column=0, columnspan=2, pady=(10, 5))

        self.bg_r_label = ttk.Label(self.main_frame, text="R:")
        self.bg_r_label.grid(row=6, column=0, sticky="e", padx=10, pady=5)
        self.bg_r_entry = ttk.Entry(self.main_frame, width=10)
        self.bg_r_entry.insert(0, str(BG_COLOR.x))
        self.bg_r_entry.grid(row=6, column=1, padx=10, pady=5)

        self.bg_g_label = ttk.Label(self.main_frame, text="G:")
        self.bg_g_label.grid(row=6, column=2, sticky="e", padx=10, pady=5)
        self.bg_g_entry = ttk.Entry(self.main_frame, width=10)
        self.bg_g_entry.insert(0, str(BG_COLOR.y))
        self.bg_g_entry.grid(row=6, column=3, padx=10, pady=5)

        self.bg_b_label = ttk.Label(self.main_frame, text="B:")
        self.bg_b_label.grid(row=6, column=4, sticky="e", padx=10, pady=5)
        self.bg_b_entry = ttk.Entry(self.main_frame, width=10)
        self.bg_b_entry.insert(0, str(BG_COLOR.z))
        self.bg_b_entry.grid(row=6, column=5, padx=10, pady=5)

        self.camera_label = ttk.Label(
            self.main_frame, text="Camera Settings", font=("Arial", 12, "bold"))
        self.camera_label.grid(row=9, column=0, columnspan=2, pady=(15, 5))

        self.sensitivity_label = ttk.Label(
            self.main_frame, text="Sensitivity:")
        self.sensitivity_label.grid(
            row=10, column=0, sticky="e", padx=10, pady=5)
        self.sensitivity_entry = ttk.Entry(self.main_frame, width=10)
        self.sensitivity_entry.insert(0, str(SENSITIVITY))
        self.sensitivity_entry.grid(row=10, column=1, padx=10, pady=5)

        self.speed_label = ttk.Label(self.main_frame, text="Speed:")
        self.speed_label.grid(row=10, column=2, sticky="e", padx=10, pady=5)
        self.speed_entry = ttk.Entry(self.main_frame, width=10)
        self.speed_entry.insert(0, str(SPEED))
        self.speed_entry.grid(row=10, column=3, padx=10, pady=5)

        self.fov_label = ttk.Label(self.main_frame, text="FOV:")
        self.fov_label.grid(row=10, column=4, sticky="e", padx=10, pady=5)
        self.fov_entry = ttk.Entry(self.main_frame, width=10)
        self.fov_entry.insert(0, str(H_FOV))
        self.fov_entry.grid(row=10, column=5, padx=10, pady=5)

        self.near_label = ttk.Label(
            self.main_frame, text="Near:")
        self.near_label.grid(row=12, column=0, sticky="e", padx=10, pady=5)
        self.near_entry = ttk.Entry(self.main_frame, width=10)
        self.near_entry.insert(0, str(NEAR))
        self.near_entry.grid(row=12, column=1, padx=10, pady=5)

        self.far_label = ttk.Label(self.main_frame, text="Far:")
        self.far_label.grid(row=12, column=2, sticky="e", padx=10, pady=5)
        self.far_entry = ttk.Entry(self.main_frame, width=10)
        self.far_entry.insert(0, str(FAR))
        self.far_entry.grid(row=12, column=3, padx=10, pady=5)

        self.graphics_label = ttk.Label(
            self.main_frame, text="Graphics Settings", font=("Arial", 12, "bold"))
        self.graphics_label.grid(row=13, column=0, columnspan=2, pady=(15, 5))

        self.gl_version_label = ttk.Label(
            self.main_frame, text="OpenGL Version:")
        self.gl_version_label.grid(
            row=16, column=1, sticky="e", padx=10, pady=5)

        self.gl_major_entry = ttk.Entry(self.main_frame, width=5)
        self.gl_major_entry.insert(0, str(GL_MAJOR))
        self.gl_major_entry.grid(row=16, column=2, padx=5, pady=5, sticky="w")

        self.gl_minor_entry = ttk.Entry(self.main_frame, width=5)
        self.gl_minor_entry.insert(0, str(GL_MINOR))
        self.gl_minor_entry.grid(row=16, column=3, padx=5, pady=5, sticky="w")

        self.apply_button = ttk.Button(
            self.main_frame, text="Apply", bootstyle=SUCCESS, command=self.apply_settings)
        self.apply_button.grid(row=18, column=0, pady=15, padx=10, sticky="ew")

        self.cancel_button = ttk.Button(
            self.main_frame, text="Cancel", bootstyle=DANGER, command=self.destroy)
        self.cancel_button.grid(
            row=18, column=1, pady=15, padx=10, sticky="ew")

    def apply_settings(self):
        try:

            width = int(self.res_width_entry.get())
            height = int(self.res_height_entry.get())
            display_x = int(self.display_x_entry.get())
            display_y = int(self.display_y_entry.get())
            r = float(self.bg_r_entry.get())
            g = float(self.bg_g_entry.get())
            b = float(self.bg_b_entry.get())
            sensitivity = float(self.sensitivity_entry.get())
            speed = float(self.speed_entry.get())
            h_fov = float(self.fov_entry.get())
            near = float(self.near_entry.get())
            far = float(self.far_entry.get())
            is_fps_text = self.fps_text_var.get()
            is_num_obj_text = self.num_obj_text_var.get()
            gl_major = int(self.gl_major_entry.get())
            gl_minor = int(self.gl_minor_entry.get())

            self.save_to_ini(width, height, display_x, display_y, r, g, b, sensitivity,
                             speed, h_fov, near, far, is_fps_text, is_num_obj_text, gl_major, gl_minor)
            messagebox.showinfo("Settings Applied",
                                "Settings have been applied and saved!")
            self.destroy()

        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter valid numerical values.")

    def save_to_ini(self, width, height, display_x, display_y, r, g, b, sensitivity, speed, h_fov, near, far, is_fps_text, is_num_obj_text, gl_major, gl_minor):
        config = configparser.ConfigParser()

        config.add_section('Window')
        config.add_section('Camera')
        config.add_section('Graphic')

        config.set('Window', 'res_x', str(width))
        config.set('Window', 'res_y', str(height))
        config.set('Window', 'display_x', str(display_x))
        config.set('Window', 'display_y', str(display_y))
        config.set('Window', 'r', str(r))
        config.set('Window', 'g', str(g))
        config.set('Window', 'b', str(b))

        config.set('Camera', 'sensitivity', str(sensitivity))
        config.set('Camera', 'speed', str(speed))
        config.set('Camera', 'h_fov', str(h_fov))
        config.set('Camera', 'near', str(near))
        config.set('Camera', 'far', str(far))

        config.set('Graphic', 'is_fps_text', str(is_fps_text))
        config.set('Graphic', 'is_num_obj_text', str(is_num_obj_text))
        config.set('Graphic', 'gl_major', str(gl_major))
        config.set('Graphic', 'gl_minor', str(gl_minor))

        with open('config/config.ini', 'w') as configfile:
            config.write(configfile)


if __name__ == "__main__":
    settings_window = SettingsWindow()
    settings_window.mainloop()
