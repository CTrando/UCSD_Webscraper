from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import time

from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

Config.set('graphics', 'font-name', 'Times')


class RootLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (50, 50)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        print(self.rect.size)


class MyLabel(Label):
    def __init__(self, **kwargs):
        super(MyLabel, self).__init__(**kwargs)
        self.bind(size=self.setter('text_size'))


class TimeLabel(MyLabel):
    def update(self, *args):
        self.text = str(time.asctime(time.localtime(time.time())))


class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(MyGridLayout, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 0, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MainApp(App):
    def build(self):
        self.root = root= RootLayout()

        # First layer holds the title and the time
        self.first_layer = first_layer = BoxLayout(size_hint=(1, 1))
        label = MyLabel(text='UCSD Web Scraper', font_size='32sp', halign='left', size_hint=(.7, 1), valign='top')
        credits_label = TimeLabel(text='Hi', font_size=14, halign='right',
                                  size_hint=(.3, 1), valign='top')
        first_layer.add_widget(label)
        first_layer.add_widget(credits_label)
        root.add_widget(first_layer)

        # Schedule updating the time
        Clock.schedule_interval(credits_label.update, 1)

        # The second layer, just holds the enter the following label
        self.second_layer = secondLayer = BoxLayout(size_hint=(1, 1))
        secondLayer.add_widget(MyLabel(text='Enter your classes below.', halign='left', valign='middle'))
        root.add_widget(secondLayer)

        # The third layer
        self.third_layer = third_layer = BoxLayout(size_hint=(1, 10))

        # The first half of the third layer
        third_layer_1 = BoxLayout(size_hint=(.5, 1), orientation='vertical')
        grid = GridLayout(cols=2, size_hint=(1, 1))
        text_input = TextInput(text='hi', multiline=False, size_hint=(.8,1))
        text_input.bind(on_text_validate=self.handle_input)
        grid.add_widget(text_input)
        grid.add_widget(Button(text='Enter', size_hint=(.2, 1)))
        third_layer_1.add_widget(grid)
        third_layer_1.add_widget(Label(size_hint=(1, 8)))
        third_layer_1.add_widget(Button(text='Clean'))
        third_layer_1.add_widget(Button(text='Parse'))

        # The second half of the third layer
        third_layer_2 = BoxLayout(size_hint=(.5, 1), orientation='vertical')

        # Grid with all the classes
        self.classes_grid = classes_grid = GridLayout(cols=2, size_hint=(1, 1))

        third_layer_2.add_widget(classes_grid)
        third_layer_2.add_widget(Label(size_hint=(1, .2)))

        # Create a new grid so it will go like [     Begin] instead of [Begin      ]
        begin_grid = GridLayout(cols=2, size_hint=(1, .3))
        begin_grid.add_widget(Label())
        begin_grid.add_widget(Button(text='Begin', size_hint=(1, 1)))
        third_layer_2.add_widget(begin_grid)

        third_layer.add_widget(third_layer_1)
        third_layer.add_widget(third_layer_2)
        root.add_widget(third_layer)

        return root

    def handle_input(self, value):
        ClassRow(widget=self.classes_grid, class_name=value.text)
        print(value.text)
        value.text=''




class ClassRow():
    def __init__(self, **kwargs):
        if 'class_name' in kwargs:
            self.class_name = kwargs['class_name']
        else:
            self.class_name = ''
        if 'widget' in kwargs:
            kwargs['widget'].add_widget(MyLabel(text=self.class_name, padding=(50,20), halign='left', valign='center', size_hint=(.6, None), height=50))
            kwargs['widget'].add_widget(Button(text='hi how are you', size_hint=(.4, None), height=50))


if __name__ == '__main__':
    MainApp().run()
