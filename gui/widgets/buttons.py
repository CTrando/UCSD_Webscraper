from kivy.uix.button import Button


class MyButton(Button):
    """
    Simple wrapper for button that will change the background color.
    """
    def __init__(self, **kwargs):
        """
        Set the background color.
        :param kwargs: Arguments for Kivy.
        """
        super().__init__(**kwargs)
        self.background_color = (0, .5, 1, 1)