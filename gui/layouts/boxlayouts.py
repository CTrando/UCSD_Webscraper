from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.boxlayout import BoxLayout


class BackgroundBoxLayout(BoxLayout):
    """
    A wrapper class for Box Layout that will allow me to place
    a background for the layout.
    """

    def __init__(self, background_color=None, background=None, **kwargs):
        """
        Sets the background of the canvas to the image or color that is specified.
        :param background_color: The color of the background accepted as tuple
        :param background: The path to the background image
        :param kwargs: arguments passed into default Kivy Box Layout
        """
        super().__init__(**kwargs)

        assert background_color is not None and background is not None, \
            'Why are you using BackgroundBoxLayout without a background?'

        with self.canvas.before:
            # Initializing the rectangle to be written upon by the color or image
            self.rect = Rectangle(size=self.size, pos=self.pos)
            # Setting background color
            if background_color:
                Color(background_color[0], background_color[1], background_color[2], background_color[3])
            # Setting background
            if background:
                self.rect.source = background
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        """
        Updating the rectangle components after a resize change.
        :param instance: The size of the resized MyLabel widget
        :param value: Dummy value passed along with bind
        """
        self.rect.pos = instance.pos
        self.rect.size = instance.size
