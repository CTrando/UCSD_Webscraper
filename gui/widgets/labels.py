import time
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.uix.label import Label


class MyLabel(Label):
    """
    Small wrapper class over the Label class from Kivy that allows
    the Label widget to be repositioned and aligned in different places
    by expanding the bounding box to take up the size of its container.
    """

    def __init__(self, background_src=None, text_color=(0, 0, .4, 1), background_color=None, **kwargs):
        """
        Will create a Label object with optional text_coloring or background_coloring or
        an image in the background. Allows for alignment.
        :param background_src: The path to the background image
        :param text_color: The color of the image accepted as a tuple
        :param background_color: The color of the background accepted as a tuple
        :param kwargs: Optional kwargs that will be passed to default Label class
        """
        super(MyLabel, self).__init__(**kwargs)
        self.color = text_color
        # Defining rectangle up here in order to set the default color to white
        self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        if background_color or background_src:
            with self.canvas.before:
                if background_color:
                    # If a color is present then set the color
                    # Make sure to reset the background rectangle to a new rectangle that will reflect
                    # the color change
                    Color(background_color[0], background_color[1], background_color[2], background_color[3])
                    self.rect = RoundedRectangle(size=self.size, pos=self.pos)
                if background_src:
                    # Same with the background, need to make a new rectangle if want to show
                    # a new background with the rectangle
                    self.rect.source = background_src
                    self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        # Bind the change in size and position to the update rect method defined below
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        """
        Updating the rectangle components after a resize change.
        :param instance: The size of the resized MyLabel widget
        :param value: Dummy value passed along with bind
        """
        self.text_size = instance.size
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class TimeLabel(MyLabel):
    """
    Wrapper class for time that will update itself with the current time.
    """
    def update(self, *args):
        """
        Update the time using the time.localtime method.
        :param args: Requires this from default kivy method
        """
        cur_time = time.localtime(time.time())
        cur_time = time.strftime('%a. %b %d, %Y %I:%M %p')
        self.text = cur_time
