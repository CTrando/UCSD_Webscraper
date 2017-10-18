from kivy import Config
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import time

from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from classpicker import ClassPicker
from data_util import data_cleaner, data_parser
from timeutils import TimeInterval

Config.set('graphics', 'font-name', 'Times')
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')


class RootLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (50, 50)
        with self.canvas.before:
            Color(.95, .95, .95, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.rect.source = 'background_logo.jpg'
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        print(self.rect.size)


class MyLabel(Label):
    def __init__(self, background=None, color=(0, 0, .4, 1), **kwargs):
        super(MyLabel, self).__init__(**kwargs)
        self.color = color

        self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        if background:
            with self.canvas.before:
                self.rect = RoundedRectangle(size=self.size, pos=self.pos)
                self.rect.source = background
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.text_size = instance.size
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class BackgroundBoxLayout(BoxLayout):
    def __init__(self, color=None, background=None, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos)
            if color:
                Color(color[0], color[1], color[2], color[3])
            if background:
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


class MyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, .5, 1, 1)


class MainApp(App):
    class_rows = []
    time_prfs = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        # initialize the root
        self.root = root = RootLayout()

        # First layer holds the title and the time
        self.first_layer = first_layer = BoxLayout(size_hint=(1, 1))
        title_label = MyLabel(text='UCSD Web Scraper', font_size='32sp', halign='left', size_hint=(.8, 1), valign='top')
        title_label.y = 800

        time_label = TimeLabel(font_size=14, halign='right',
                               size_hint=(.3, 1), valign='top')
        time_label.update()
        time_label.opacity = 0

        Animation(y=500, duration=1).start(title_label)
        Animation(opacity=1, duration=1.5).start(time_label)

        first_layer.add_widget(title_label)
        first_layer.add_widget(time_label)
        root.add_widget(first_layer)

        # Schedule updating the time
        Clock.schedule_interval(time_label.update, 1)

        # The third layer
        self.third_layer = third_layer = BoxLayout(size_hint=(1, 10))

        # The first half of the third layer
        third_layer_1 = BoxLayout(size_hint=(.5, 1), orientation='vertical')
        third_layer_1.add_widget(
            MyLabel(text='Enter your classes below.', size_hint=(1, 1), halign='left', valign='center'))

        # Doing the text addition
        text_box = BoxLayout(size_hint=(1, 1))
        self.text_input = text_input = TextInput(multiline=False, size_hint=(.8, None), height=50)

        text_input.bind(on_text_validate=self.add_class_row)
        text_box.add_widget(text_input)

        # Adding the add_class_button
        add_class_button = MyButton(text='Enter', size_hint=(.2, None), height=50)
        add_class_button.bind(on_press=self.add_class_row)
        text_box.add_widget(add_class_button)

        third_layer_1.add_widget(text_box)

        third_layer_1.add_widget(MyLabel(text='Enter your time preferences here.', valign='center'))

        time_box = BoxLayout(size_hint=(1, 1))

        # Doing the second time input
        self.time_input = TextInput(size_hint=(.8, None), height=50, multiline=False)
        self.time_input.bind(on_text_validate=self.add_time_preference)

        # Adding the enter preference button
        add_preference_button = MyButton(text='Enter', size_hint=(.2, None), height=50,
                                         on_press=self.add_time_preference)

        time_box.add_widget(self.time_input)
        time_box.add_widget(add_preference_button)
        third_layer_1.add_widget(time_box)

        temp_box = BoxLayout(size_hint=(1, 5))
        self.time_preferences_box = time_preference_box = StackLayout(padding=(0, 10), spacing=3, size_hint=(1, 1))
        temp_box.add_widget(self.time_preferences_box)

        third_layer_1.add_widget(temp_box)

        self.results_box = results_box = BoxLayout(orientation='vertical', padding=(10, 0), size_hint=(1, 8))

        third_layer_1.add_widget(MyButton(text='Parse', size_hint=(1, 1), on_press=self.parse))
        third_layer_1.add_widget(MyButton(text='Clean', size_hint=(1, 1), on_press=self.clean))

        # The second half of the third layer
        third_layer_2 = BoxLayout(size_hint=(.5, 1), orientation='vertical')

        third_layer_2.add_widget(MyLabel(text='', valign='center', size_hint=(1, 1)))

        # Grid with all the classes
        self.classes_box = classes_box = StackLayout(padding=(10, 0), spacing=3, size_hint=(1, 12))

        third_layer_2.add_widget(classes_box)

        # Create time entry

        # Create a new grid so it will go like [     Begin] instead of [Begin      ]
        begin_box = BoxLayout(size_hint=(1, 1), spacing=10)
        begin_box.add_widget(Label())
        begin_button = MyButton(text='Begin', size_hint=(1, None), height=100, on_press=self.begin)
        begin_box.add_widget(begin_button)
        third_layer_2.add_widget(begin_box)

        third_layer.add_widget(third_layer_1)
        third_layer.add_widget(third_layer_2)
        root.add_widget(third_layer)

        return root

    def add_class_row(self, value):
        if len(self.text_input.text) == 0:
            return
        self.class_rows.append(
            ClassRow(widget=self.classes_box, color=(.97, .97, .97, 1), class_name=self.text_input.text))
        print([row.class_name for row in self.class_rows])
        self.text_input.text = ''

    def add_time_preference(self, value):
        if len(self.time_input.text) == 0:
            return
        self.time_prfs.append(
            ClassRow(parent_list=MainApp.time_prfs, widget=self.time_preferences_box,
                     color=(.8, .8, .92, 1),
                     class_name=self.time_input.text))
        self.time_input.text = ''

    def parse(self, value):
        parser = data_parser.Parser()
        parser.parse()

    def clean(self, value):
        cleaner = data_cleaner.Cleaner()
        cleaner.clean()

    def format_class(self, cl):
        ret = []
        data = cl.data
        if 'COURSE_NUM' in data:
            ret.append(data['COURSE_NUM'])
        if 'TYPE' in data:
            ret.append(data['TYPE'])
        if 'DAYS' in data:
            ret.append(data['DAYS'])
        if 'TIME' in data:
            ret.append(data['TIME'])
        return ' '.join(ret)

    def begin(self, value):
        self.results_box.clear_widgets()
        class_picker = ClassPicker()
        classes = [row.class_name for row in self.class_rows]
        intervals = [TimeInterval(None, row.class_name) for row in self.time_prfs]

        # Creating popup and results content
        popup = Popup(title='Results', title_size='24sp', title_color=(0, 0, 0, 1), size_hint=(.8, .8))
        results_box = StackLayout(size_hint=(1, 1), padding=[10, 10])
        popup.background = 'popup_background_logo.jpg'
        popup.add_widget(results_box)

        best_classes = []
        # picking the class after making the widgets to allow for error handling
        try:
            best_classes = class_picker.pick(inputs=classes, intervals=intervals)
        except IOError as e:
            results_box.add_widget(MyLabel(text=str(e), size_hint=(1,1), valign='top'))
        except RuntimeError as e:
            results_box.add_widget(MyLabel(text=str(e), size_hint=(1,1), valign='top'))

        for best_class in best_classes:
            title = ''
            sub_class_str = ''
            temp_box = BoxLayout(orientation='vertical', size_hint=(.5, None))
            for sub_class in best_class.subclasses.values():
                title = sub_class.data['DESCRIPTION']
                sub_class_str += self.format_class(sub_class) + '\n'
            temp_box.add_widget(
                MyLabel(text=title, color=(.4, .4, .4, 1), valign='top', halign='left', size_hint=(1, .2)))
            temp_box.add_widget(
                MyLabel(text=sub_class_str, color=(.4, .4, .4, 1), font_size='14sp', valign='top', halign='left',
                        size_hint=(1, .8)))
            results_box.add_widget(temp_box)

        # Making the popup
        popup.open()


class ClassRow():
    def __init__(self, parent_list=MainApp.class_rows, color=(.6, .6, .6, 1), **kwargs):
        self.parent_list = parent_list
        if 'class_name' in kwargs:
            self.class_name = kwargs['class_name'].upper()
        else:
            self.class_name = ''
        if 'widget' in kwargs:
            self.layout = BoxLayout(size_hint=(1, None), height=50)
            self.widget = kwargs['widget']
            self.label = MyColoredLabel(text=self.class_name, halign='center', valign='center',
                                        size_hint=(.6, None), color=color,
                                        height=50)
            self.button = MyButton(text='Remove', size_hint=(.4, None), height=50)
            self.button.bind(on_press=self.destroy)
            self.layout.add_widget(self.label)
            self.layout.add_widget(self.button)
            kwargs['widget'].add_widget(self.layout)

    def destroy(self, value):
        self.widget.remove_widget(self.layout)
        self.parent_list.remove(self)


if __name__ == '__main__':
    MainApp().run()
