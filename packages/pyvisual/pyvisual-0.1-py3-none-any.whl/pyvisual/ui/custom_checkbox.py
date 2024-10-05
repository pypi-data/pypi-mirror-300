import os
from pyvisual.ui.image import Image  # Ensure this is the correct import path
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.core.window import Window

class CustomCheckbox(Image):
    def __init__(self, window, x, y, checked_image=None, unchecked_image=None, scale=1.0,
                 checked_callback=None, unchecked_callback=None,
                 text=None, text_position='none', text_padding=5,
                 font_name='Roboto', font_color=(0, 0, 0, 1), font_size=14):
        """
        Initialize the CustomCheckbox.

        :param window: The window to which the checkbox will be added.
        :param x: The x-coordinate position of the checkbox.
        :param y: The y-coordinate position of the checkbox.
        :param checked_image: Path to the image representing the "Checked" state.
        :param unchecked_image: Path to the image representing the "Unchecked" state.
        :param scale: Scale factor for the checkbox images.
        :param checked_callback: Function to call when toggled to "Checked".
        :param unchecked_callback: Function to call when toggled to "Unchecked".
        :param text: Text to display alongside the checkbox.
        :param text_position: Position of the text relative to the checkbox ('none', 'left', 'right', 'top', 'bottom').
        :param text_padding: Padding between the checkbox and the text.
        :param font_name: Font name or path for the text.
        :param font_color: Color of the text in RGBA format.
        :param font_size: Size of the text font.
        """
        # Get the base path to the assets folder by moving up two directory levels
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        default_image_folder = os.path.join(base_path, "assets", "checkboxes", "sample")

        # Use default images if not provided
        self.checked_image_path = checked_image or os.path.join(default_image_folder, "checked.png")
        self.unchecked_image_path = unchecked_image or os.path.join(default_image_folder, "unchecked.png")

        # Store callback functions
        self.checked_callback = checked_callback
        self.unchecked_callback = unchecked_callback

        # Initial checkbox state
        self.is_checked = False  # Default state is unchecked

        # Initialize the checkbox image with the unchecked image path
        super().__init__(window, x, y, image_path=self.unchecked_image_path, scale=scale)

        # Text properties
        self.text = text
        self.text_position = text_position.lower()
        self.text_padding = text_padding
        self.font_name = font_name
        self.font_color = font_color
        self.font_size = font_size

        # Initialize the label if text is provided
        self.label = None
        if self.text and self.text_position != 'none':
            self.create_label(window)

    def create_label(self, window):
        """
        Create and add a Label widget based on the text properties.

        :param window: The window to which the label will be added.
        """
        # Register the font if it's a custom font file
        if os.path.isfile(self.font_name):
            font_name_without_ext = os.path.splitext(os.path.basename(self.font_name))[0]
            LabelBase.register(name=font_name_without_ext, fn_regular=self.font_name)
            font_name_to_use = font_name_without_ext
        else:
            font_name_to_use = self.font_name  # Use default Kivy font

        self.label = Label(text=self.text,
                           font_name=font_name_to_use,
                           color=self.font_color,
                           font_size=self.font_size,
                           size_hint=(None, None),
                           size=(Window.width, Window.height))  # Temporary size; will be updated
        window.add_widget(self.label)
        self.update_label_position()

    def on_touch_down(self, touch):
        """Handle mouse click to toggle checkbox state and update image."""
        if self.collide_point(*touch.pos):
            # Toggle the checked state
            self.is_checked = not self.is_checked

            # Update the checkbox image
            self.source = self.checked_image_path if self.is_checked else self.unchecked_image_path

            # Trigger the appropriate callback
            if self.is_checked and self.checked_callback:
                self.checked_callback(self)
            elif not self.is_checked and self.unchecked_callback:
                self.unchecked_callback(self)

            # Update label appearance if needed (optional: e.g., change text color)
            # self.update_label_appearance()

            return True  # Indicate that the touch was handled
        return super().on_touch_down(touch)  # Ensure the event is correctly passed to other widgets

    def set_images(self, checked_image, unchecked_image):
        """Set new images for checked and unchecked states."""
        self.checked_image_path = checked_image
        self.unchecked_image_path = unchecked_image
        self.source = self.checked_image_path if self.is_checked else self.unchecked_image_path

    def set_checked(self, state=True):
        """Set the checked state manually."""
        self.is_checked = state
        self.source = self.checked_image_path if self.is_checked else self.unchecked_image_path

        # Trigger the appropriate callback
        if self.is_checked and self.checked_callback:
            self.checked_callback(self)
        elif not self.is_checked and self.unchecked_callback:
            self.unchecked_callback(self)

    def update_label_position(self):
        """Position the label based on the text_position and padding."""
        if not self.label:
            return

        # Update label's size to fit the text
        self.label.texture_update()
        self.label.size = self.label.texture_size

        # Get checkbox position and size
        checkbox_x, checkbox_y = self.pos
        checkbox_width, checkbox_height = self.size
        label_width, label_height = self.label.size

        if self.text_position == 'left':
            label_x = checkbox_x - self.text_padding - label_width
            label_y = checkbox_y + (checkbox_height - label_height) / 2
        elif self.text_position == 'right':
            label_x = checkbox_x + checkbox_width + self.text_padding
            label_y = checkbox_y + (checkbox_height - label_height) / 2
        elif self.text_position == 'top':
            label_x = checkbox_x + (checkbox_width - label_width) / 2
            label_y = checkbox_y + checkbox_height + self.text_padding
        elif self.text_position == 'bottom':
            label_x = checkbox_x + (checkbox_width - label_width) / 2
            label_y = checkbox_y - self.text_padding - label_height
        else:
            label_x, label_y = self.label.pos  # Default to current position if invalid

        self.label.pos = (label_x, label_y)

    def set_text(self, text, position='none', padding=5,
                font_name='Roboto', font_color=(0, 0, 0, 1), font_size=14):
        """
        Set or update the text and its properties.

        :param text: The text to display.
        :param position: Position of the text relative to the checkbox ('none', 'left', 'right', 'top', 'bottom').
        :param padding: Padding between the checkbox and the text.
        :param font_name: Font name or path for the text.
        :param font_color: Color of the text.
        :param font_size: Size of the text font.
        """
        self.text = text
        self.text_position = position.lower()
        self.text_padding = padding
        self.font_name = font_name
        self.font_color = font_color
        self.font_size = font_size

        if self.text and self.text_position != 'none':
            if not self.label:
                # Create the label if it doesn't exist
                self.create_label(Window)
            else:
                # Update existing label properties
                if os.path.isfile(self.font_name):
                    font_name_without_ext = os.path.splitext(os.path.basename(self.font_name))[0]
                    LabelBase.register(name=font_name_without_ext, fn_regular=self.font_name)
                    self.label.font_name = font_name_without_ext
                else:
                    self.label.font_name = self.font_name
                self.label.text = self.text
                self.label.color = self.font_color
                self.label.font_size = self.font_size
                self.label.texture_update()
                self.label.size = self.label.texture_size
            self.update_label_position()
        else:
            # Remove the label if text is set to 'none' or empty
            if self.label:
                Window.remove_widget(self.label)
                self.label = None

    def set_text_properties(self, font_name=None, font_color=None, font_size=None):
        """
        Update the text properties.

        :param font_name: New font name or path.
        :param font_color: New font color.
        :param font_size: New font size.
        """
        if not self.label:
            return

        if font_name:
            if os.path.isfile(font_name):
                font_name_without_ext = os.path.splitext(os.path.basename(font_name))[0]
                LabelBase.register(name=font_name_without_ext, fn_regular=font_name)
                self.label.font_name = font_name_without_ext
            else:
                self.label.font_name = font_name

        if font_color:
            self.label.color = font_color

        if font_size:
            self.label.font_size = font_size

        self.label.texture_update()
        self.label.size = self.label.texture_size
        self.update_label_position()


# Example usage of the Enhanced CustomCheckbox class
if __name__ == "__main__":
    import pyvisual as pv

    window = pv.Window()

    # Toggle callback functions
    def on_checkbox_checked(cb):
        print("Checkbox is checked!")

    def on_checkbox_unchecked(cb):
        print("Checkbox is unchecked!")

    # Add a custom checkbox with text on the right
    custom_checkbox1 = CustomCheckbox(
        window=window,
        x=200, y=250,  # Position on the screen
        scale=1,  # Scale down the checkbox size
        checked_callback=on_checkbox_checked,
        unchecked_callback=on_checkbox_unchecked,
        text="Accept Terms",  # Text to display
        text_position='right',  # Position of the text relative to the checkbox
        text_padding=10,  # Padding between checkbox and text
        font_name='Roboto',  # Font name or path
        font_color=(0, 0, 0, 1),  # Black color
        font_size=16  # Font size
    )

    # Add another checkbox with text at the bottom
    custom_checkbox2 = CustomCheckbox(
        window=window,
        x=200, y=200,
        scale=1,
        checked_callback=lambda cb: print("Checkbox2 is checked!"),
        unchecked_callback=lambda cb: print("Checkbox2 is unchecked!"),
        text="Subscribe to Newsletter",
        text_position='bottom',  # Text below the checkbox
        text_padding=8,
        font_name='Roboto',
        font_color=(0, 0, 1, 1),  # Blue color
        font_size=14
    )

    # Create a checkbox without text
    custom_checkbox3 = CustomCheckbox(
        window=window,
        x=200, y=150,
        scale=1,
        checked_callback=lambda cb: print("Checkbox3 is checked!"),
        unchecked_callback=lambda cb: print("Checkbox3 is unchecked!"),
        text=None,  # No text
        text_position='none'
    )

    # Create a checkbox with text on the left
    custom_checkbox4 = CustomCheckbox(
        window=window,
        x=200, y=100,
        scale=1,
        checked_callback=lambda cb: print("Checkbox4 is checked!"),
        unchecked_callback=lambda cb: print("Checkbox4 is unchecked!"),
        text="Enable Notifications",
        text_position='left',  # Text to the left of the checkbox
        text_padding=10,
        font_name='Roboto',
        font_color=(1, 0, 0, 1),  # Red color
        font_size=16
    )

    # Optionally, dynamically update the text of a checkbox after creation
    # custom_checkbox1.set_text("New Text", position='top', padding=12, font_color=(0, 1, 0, 1), font_size=18)

    window.show()
