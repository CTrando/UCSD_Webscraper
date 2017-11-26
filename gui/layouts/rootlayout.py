import os

from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from settings import IMAGE_DIR


class RootLayout(BoxLayout):
    def __init__(self, **kwargs):
        """
        Constructor for background layout - this is the main layout.
        :param kwargs: arguments from kivy constructor
        """
        super(RootLayout, self).__init__(**kwargs)
        # Defining settings for the root layout
        self.orientation = 'vertical'
        # Kivy padding is like HTML padding so pads 50 for every side
        self.padding = (50, 50)
        # Using with to close canvas after initializing
        with self.canvas.before:
            # Defining texture for the background
            self.texture = Image(source=os.path.join(IMAGE_DIR, 'background_logo.jpg')).texture
            # Getting width and height of texture to prevent stretching
            self.width = self.texture.width
            self.height = self.texture.height

            # Setting the bounding box for the background and the background image
            self.bound_box = Rectangle(size=self.size, pos=self.pos)
            self.image_bound_box = Rectangle(size=self.size, pos=self.pos, texture=self.texture)

        # Binding size and position change to _update_rect method
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        """
        Private method that will update the bounding boxes and make sure the image
        remains centered and unstretched
        :param instance: The source object - in this case it would be the caller Root Layout
        :param value: Dummy value pased along with bind method
        """
        # Setting the bounding boxes to the instances
        self.bound_box.pos = instance.pos
        self.bound_box.size = instance.size

        # Making sure that the image remains in the middle
        # instance.size is a tuple with x being 0 and y being 1
        # Getting the x and y positions of the updated RootLayout and the texture
        middle = [instance.size[0] / 2, instance.size[1] / 2]
        mid_tex = [self.texture.width / 2, self.texture.height / 2]

        # Calculating the offset and representing it accordingly
        self.image_bound_box.pos = [middle[0] - mid_tex[0], middle[1] - mid_tex[1]]
