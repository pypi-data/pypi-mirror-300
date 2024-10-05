from kivy.uix.button import Button as KivyButton
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color
from kivy.core.window import Window as KivyWindow
from kivy.core.text import LabelBase


class BasicButton:
    def __init__(self, window, x, y, width=140, height=50, text="CLICK ME",
                 idle_color=(1, 1, 1, 1), hover_color=(0.7, 0.7, 0.7, 0.05), text_color=(0.6, 0.6, 0.6, 1),
                 border_color=(0, 0, 0, 1), border_thickness=1,
                 click_callback=None, release_callback=None, hover_callback=None,
                 font="Roboto", font_size=16, access_text = None):
        # Initialize button properties
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_thickness = border_thickness
        self.font_size = font_size
        self.click_callback = click_callback
        self.release_callback = release_callback
        self.hover_callback = hover_callback  # Store the hover callback function
        self.access_text = access_text
        # Register font if a file path is provided
        if font.endswith((".ttf", ".otf")):
            LabelBase.register(name="CustomFont", fn_regular=font)
            self.font_name = "CustomFont"
        else:
            self.font_name = font

        # Create a Kivy button widget
        self.button_widget = KivyButton(
            text=self.text,
            size=(self.width, self.height),
            pos=(self.x, self.y),  # Positioning will work with FloatLayout
            background_normal='',  # Disable default Kivy background
            background_color=self.idle_color,
            color=self.text_color,
            font_name=self.font_name,
            font_size=self.font_size,
            size_hint=(None, None)  # Disable size_hint to manually set size
        )

        # Draw the custom border
        self.draw_border()

        # Bind events for click, release, and hover callbacks
        if self.click_callback:
            self.button_widget.bind(on_press=self.click_callback)
        if self.release_callback:
            self.button_widget.bind(on_release=self.release_callback)

        # Monitor mouse position to simulate hover
        KivyWindow.bind(mouse_pos=self.on_mouse_pos)

        # Add the button to the window
        window.add_widget(self.button_widget)

    def draw_border(self):
        """Draw a custom border around the button."""
        with self.button_widget.canvas.before:
            Color(*self.border_color)  # Set the border color
            Line(
                rectangle=(self.button_widget.x, self.button_widget.y, self.button_widget.width, self.button_widget.height),
                width=self.border_thickness
            )

    def on_mouse_pos(self, window, pos):
        """Detect hover by checking if the mouse is within the button area."""
        if self.is_mouse_hovering(pos):
            self.button_widget.background_color = self.hover_color
            if self.hover_callback:
                self.hover_callback(self)  # Invoke the hover callback
        else:
            self.button_widget.background_color = self.idle_color

    def is_mouse_hovering(self, pos):
        """Check if the mouse is within the button's boundaries."""
        return (self.button_widget.x <= pos[0] <= self.button_widget.x + self.button_widget.width and
                self.button_widget.y <= pos[1] <= self.button_widget.y + self.button_widget.height)

    def set_border(self, border_thickness, border_color):
        """Set the border thickness and color, and redraw the border."""
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.button_widget.canvas.before.clear()  # Clear the previous canvas
        self.draw_border()  # Redraw the border with new settings

    def set_font(self, font_name, font_size):
        """Set the font name or file path and font size."""
        if font_name.endswith((".ttf", ".otf")):
            LabelBase.register(name="CustomFont", fn_regular=font_name)
            self.button_widget.font_name = "CustomFont"
        else:
            self.button_widget.font_name = font_name
        self.button_widget.font_size = font_size

if __name__ == "__main__":
    import pyvisual as pv
    window = pv.Window()
    # Create a button with hover, click, and release callbacks
    button = BasicButton(
        window=window,
        x=325, y=275,
        width=150, height=50,
        text="Click Me!",
        idle_color=(0.8, 0.8, 0.8, 1),  # Light Gray for idle state
        hover_color=(0.6, 0.6, 0.6, 0.3),  # Darker Gray for hover state
        text_color=(0.2, 0.2, 0.2, 1),  # Black Text Color
        border_color=(0.4, 0.4, 0.4, 1),  # Border Color
        border_thickness=2,  # Border thickness
        click_callback=lambda instance: print("Button clicked!"),
        release_callback=lambda instance: print("Button released!"),
        hover_callback=lambda instance: print("Button hovered!")
    )

    window.show()
