from kivy.uix.label import Label
from kivy.core.text import LabelBase


class Text(Label):
    def __init__(self, window, x, y, text="Hello", scale=1.0, font_path=None, font_size=20, color=(0.3, 0.3, 0.3, 1),
                 shadow=False, shadow_color=(0, 0, 0, 0.5), shadow_offset=(2, -2), blur=False, blur_radius=5):
        # Register custom font if provided
        if font_path and font_path.endswith((".ttf", ".otf")):
            LabelBase.register(name="CustomFont", fn_regular=font_path)
            self.font_name = "CustomFont"
        else:
            self.font_name = "Roboto"  # Default font

        # Initialize the main text label with the specified properties
        super().__init__(
            text=text,
            font_name=self.font_name,
            font_size=font_size,  # Base font size
            color=color,
            size_hint=(None, None),  # Disable size hint
            halign='left',
            valign='top',
            text_size=(None, None),
        )

        # Store initial position
        self.anchor_x = x
        self.anchor_y = y

        # Initialize shadow and blur properties
        self.shadow = shadow
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset
        self.blur = blur
        self.blur_radius = blur_radius

        # If shadow is enabled, create a shadow label
        if self.shadow:
            self.create_shadow(window)

        # Apply scaling to text
        self.set_scale(scale)

        # Adjust position to keep top-left corner at (x, y)
        self.update_position()

        # Add the text widget to the window
        window.add_widget(self)

    def create_shadow(self, window):
        """Create a shadow label behind the main text label, optionally with a blur effect."""
        # Create the shadow label
        self.shadow_label = Label(
            text=self.text,
            font_name=self.font_name,
            font_size=self.font_size,
            color=self.shadow_color,
            size_hint=(None, None),
            halign='left',
            valign='top',
            text_size=(None, None),
        )

        # Apply scaling to shadow label
        self.shadow_label.texture_update()
        self.shadow_label.size = self.shadow_label.texture_size

        # Adjust position
        self.shadow_label.pos = (
            self.anchor_x + self.shadow_offset[0],
            self.anchor_y + self.shadow_offset[1] - self.shadow_label.texture_size[1]
        )

        # Add to window
        window.add_widget(self.shadow_label)

    def set_scale(self, scale):
        """Set the scale of the text based on the scale factor."""
        self.font_size = self.font_size * scale
        self.texture_update()
        self.size = self.texture_size
        if self.shadow and hasattr(self, 'shadow_label'):
            self.shadow_label.font_size = self.font_size
            self.shadow_label.texture_update()
            self.shadow_label.size = self.shadow_label.texture_size

        # Update positions after scaling
        self.update_position()

    def update_position(self):
        """Adjust the position of the text and its shadow to keep the anchor point fixed."""
        # For main label
        self.texture_update()
        self.size = self.texture_size
        self.pos = (
            self.anchor_x,
            self.anchor_y - self.texture_size[1]
        )

        # For shadow label
        if self.shadow and hasattr(self, 'shadow_label'):
            self.shadow_label.texture_update()
            self.shadow_label.size = self.shadow_label.texture_size
            self.shadow_label.pos = (
                self.anchor_x + self.shadow_offset[0],
                self.anchor_y + self.shadow_offset[1] - self.shadow_label.texture_size[1]
            )

    def set_position(self, x, y):
        """Update the anchor position of the text and its shadow."""
        self.anchor_x = x
        self.anchor_y = y
        self.update_position()

    def set_text(self, text):
        """Update the text content and apply to both main and shadow labels."""
        self.text = text
        self.texture_update()
        self.size = self.texture_size
        if self.shadow and hasattr(self, 'shadow_label'):
            self.shadow_label.text = text
            self.shadow_label.texture_update()
            self.shadow_label.size = self.shadow_label.texture_size

        # Update positions after text change
        self.update_position()

    def set_font(self, font_path):
        """Set a new font for both main and shadow labels."""
        if font_path and font_path.endswith((".ttf", ".otf")):
            LabelBase.register(name="CustomFont", fn_regular=font_path)
            self.font_name = "CustomFont"
        else:
            self.font_name = font_path
        self.font_name = font_path
        self.texture_update()
        self.size = self.texture_size

        if self.shadow and hasattr(self, 'shadow_label'):
            self.shadow_label.font_name = self.font_name
            self.shadow_label.texture_update()
            self.shadow_label.size = self.shadow_label.texture_size

        # Update positions after font change
        self.update_position()

    def set_color(self, color):
        """Set the color of the main text label."""
        self.color = color

    def set_shadow_color(self, shadow_color):
        """Set the color of the shadow text label."""
        self.shadow_color = shadow_color
        if self.shadow and hasattr(self, 'shadow_label'):
            self.shadow_label.color = shadow_color

    def set_shadow_offset(self, shadow_offset):
        """Set the offset of the shadow position."""
        self.shadow_offset = shadow_offset
        if self.shadow and hasattr(self, 'shadow_label'):
            self.shadow_label.pos = (
                self.anchor_x + self.shadow_offset[0],
                self.anchor_y + self.shadow_offset[1] - self.shadow_label.texture_size[1]
            )

if __name__ == "__main__":
    import pyvisual as pv
    window = pv.Window()


    # Add a text element with a shadow effect to the window
    text_label = Text(
        window=window,
        x=100, y=500,  # Position of the text
        text="Text",
        scale=2,  # Scale the text size
        font_size=30,  # Initial font size
        color=(0.3, 0.3, 0.3, 1),  # Text color
        shadow=True,  # Enable shadow
        shadow_color=(0, 0, 0, 0.2),  # Shadow color
        shadow_offset=(2, -2),  # Shadow offset
        blur=False,  # Disable blur effect
        blur_radius=0  # Set blur radius
    )

    # Show the window
    window.show()
