import os
import sys
import logging


# Configure logging
from kivy.logger import Logger

# Remove all existing handlers
for handler in Logger.handlers[:]:
    Logger.removeHandler(handler)

# # Create a console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)

# Add the console handler to Kivy's logger
Logger.addHandler(console_handler)
Logger.setLevel(logging.WARNING)


from kivy.config import Config
from kivy.core.window import Window as KivyWindow
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image as KivyImage
import platform

# DPI Awareness and Scaling Detection for Windows
scaling_factor = 1.0  # Default scaling factor is 1.0 (no scaling)

# if platform.system() == "Windows":
#     import ctypes
#     try:
#         ctypes.windll.user32.SetProcessDPIAware()
#         user32 = ctypes.windll.user32
#         dpi = user32.GetDpiForWindow(user32.GetForegroundWindow())
#         scaling_factor = dpi / 96.0
#     except Exception as e:
#         print(f"Unable to set DPI awareness or detect scaling factor: {e}")

# Calculate the adjusted window size based on scaling
base_width, base_height = 800, 600
adjusted_width = int(base_width / scaling_factor)
adjusted_height = int(base_height / scaling_factor)

# Ensure Kivy respects the exact size configuration
Config.set('graphics', 'width', str(adjusted_width))
Config.set('graphics', 'height', str(adjusted_height))
Config.set('graphics', 'borderless', '0')  # Enable border for accurate dimensions
Config.set('graphics', 'fullscreen', '0')  # Disable fullscreen to maintain window size
Config.write()

class Window:
    def __init__(self, title="PyVisual Window", size=(800, 600), background_color=(225, 225, 225, 1), borderless=False,
                 resizable=False, icon_path=None, background_image=None):
        # Set a default icon path if none is provided
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.default_icon_path = os.path.join(base_path, "assets", "icons", "window", "window.ico")

        # Adjust window size according to detected scaling factor
        self.title = title
        self.size = (int(size[0] / scaling_factor), int(size[1] / scaling_factor))
        self.background_color = background_color
        self.borderless = borderless
        self.resizable = resizable
        self.background_image = background_image
        self.icon_path = icon_path or self.default_icon_path

        # Set window properties using Kivy
        self._configure_window()

        # Root widget container
        self.root_widget = FloatLayout(size=self.size)

        if self.background_image:
            self.add_background_image()

        # Bind resize event if resizable is True
        if self.resizable:
            KivyWindow.bind(on_resize=self.on_window_resize)
        else:
            KivyWindow.unbind(on_resize=self.on_window_resize)

    def _configure_window(self):
        """Apply window configuration settings."""
        Config.set('graphics', 'width', str(self.size[0]))
        Config.set('graphics', 'height', str(self.size[1]))
        Config.set('graphics', 'borderless', str(int(self.borderless)))
        Config.set('graphics', 'resizable',
                   str(int(self.resizable)))  # Ensure the resizable setting is applied correctly
        Config.write()  # Write changes to the config

        # Apply settings directly to the Kivy window
        KivyWindow.size = self.size
        KivyWindow.clearcolor = self.background_color
        KivyWindow.borderless = self.borderless
        KivyWindow.fullscreen = False
        KivyWindow.resizable = self.resizable  # This should enforce the resizable property

        # Set the icon
        KivyWindow.set_icon(self.icon_path)

        # Debugging: Print out the window properties to confirm settings
        # print(f"Window Size: {KivyWindow.size}")
        # print(f"Resizable: {KivyWindow.resizable}")
        # print(f"Borderless: {KivyWindow.borderless}")
        # print(f"Window Icon: {self.icon_path}")

    def add_background_image(self):
        """Add a background image to the window and ensure it fills the window."""
        self.bg_image = KivyImage(source=self.background_image)

        # Force the texture to load to get the correct size
        self.bg_image.texture_update()

        # Manually set size to match the window size and handle aspect ratio manually
        texture_width, texture_height = self.bg_image.texture_size
        aspect_ratio = texture_width / texture_height

        if self.size[0] / aspect_ratio <= self.size[1]:
            self.bg_image.size = (self.size[0], self.size[0] / aspect_ratio)
        else:
            self.bg_image.size = (self.size[1] * aspect_ratio, self.size[1])

        self.bg_image.size_hint = (None, None)  # Disable size hint to manually set size
        self.bg_image.pos = (0, 0)
        self.root_widget.add_widget(self.bg_image, index=0)

    def on_window_resize(self, instance, width, height):
        """Adjust the background image on window resize."""
        self.size = (width, height)
        if hasattr(self, 'bg_image'):
            self.bg_image.size = (width, height)

    def add_widget(self, widget):
        """Add a widget to the window's main container."""
        self.root_widget.add_widget(widget)

    def show(self):
        """Show the window by running the Kivy app."""

        class PyVisualApplication(App):
            def build(self):
                return self.root_widget

            def on_start(self):
                KivyWindow.set_title(self.get_application_name())

            def get_application_name(self):
                return self.title

        app = PyVisualApplication()
        app.root_widget = self.root_widget
        app.title = self.title
        app.run()


if __name__ == "__main__":
    window = Window(
        title="PyVisual Window",
        size=(800, 600),
        background_color=(1, 1, 1, 1),
    )
    window.show()
