from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import time

from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from classpicker import ClassPicker

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
        self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.text_size = instance.size
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class BackgroundBoxLayout(BoxLayout):
    def __init__(self, background=None, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.rect.source = background
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MyColoredLabel(MyLabel):
    def __init__(self, color=None, **kwargs):
        super(MyColoredLabel, self).__init__(**kwargs)
        with self.canvas.before:
            if color:
                Color(color[0], color[1], color[2], color[3])
            else:
                Color(0, 0, 0, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)


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
    class_rows = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.root = root = RootLayout()

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
        self.text_input = text_input = TextInput(multiline=False, size_hint=(.8, None), height=50)
        text_input.bind(on_text_validate=self.add_class_row)

        grid.add_widget(text_input)
        add_class_button = Button(text='Enter', size_hint=(.2, None), height=50)
        add_class_button.bind(on_press=self.add_class_row)
        grid.add_widget(add_class_button)

        self.results_box = results_box = BackgroundBoxLayout(background='Logo.jpg', orientation='vertical', padding=(10, 0), size_hint=(1, 8))

        third_layer_1.add_widget(grid)
        third_layer_1.add_widget(results_box)
        third_layer_1.add_widget(Button(text='Clean'))
        third_layer_1.add_widget(Button(text='Parse'))

        # The second half of the third layer
        third_layer_2 = BoxLayout(size_hint=(.5, 1), orientation='vertical')

        # Grid with all the classes
        self.classes_grid = classes_grid = GridLayout(cols=2, size_hint=(1, 1), padding=(10, 0), spacing=3)

        third_layer_2.add_widget(classes_grid)
        third_layer_2.add_widget(Label(size_hint=(1, .2)))

        # Create a new grid so it will go like [     Begin] instead of [Begin      ]
        begin_grid = GridLayout(cols=2, size_hint=(1, .3))
        begin_grid.add_widget(Label())
        begin_button = Button(text='Begin', size_hint=(1, 1), on_press=self.begin)
        begin_grid.add_widget(begin_button)
        third_layer_2.add_widget(begin_grid)

        third_layer.add_widget(third_layer_1)
        third_layer.add_widget(third_layer_2)
        root.add_widget(third_layer)

        return root

    def add_class_row(self, value):
        if len(self.text_input.text) == 0:
            return
        self.class_rows.append(ClassRow(widget=self.classes_grid, class_name=self.text_input.text))
        print([row.class_name for row in self.class_rows])
        self.text_input.text = ''

    def begin(self, value):
        self.results_box.clear_widgets()
        class_picker = ClassPicker()
        classes = [row.class_name for row in self.class_rows]
        best_classes = class_picker.pick(classes)
        for best_class in best_classes:
            sub_class_str = ''
            for sub_class in best_class.subclasses.values():
                sub_class_str += str(sub_class) + '\n'
            self.results_box.add_widget(MyLabel(text=sub_class_str, font_size='10sp', size_hint=(1, 1)))


class ClassRow():
    def __init__(self, **kwargs):
        if 'class_name' in kwargs:
            self.class_name = kwargs['class_name']
        else:
            self.class_name = ''
        if 'widget' in kwargs:
            self.widget = kwargs['widget']
            self.label = MyColoredLabel(text=self.class_name, padding=(50, 20), halign='center', valign='center',
                                        size_hint=(.6, None), color=(.6, .6, .6, 1),
                                        height=50)
            self.button = Button(text='Remove', size_hint=(.4, None), height=50)
            self.button.bind(on_press=self.destroy)
            kwargs['widget'].add_widget(self.label)
            kwargs['widget'].add_widget(self.button)

    def destroy(self, value):
        self.widget.remove_widget(self.label)
        self.widget.remove_widget(self.button)
        MainApp.class_rows.remove(self)


if __name__ == '__main__':
    MainApp().run()
