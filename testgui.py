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
        root = RootLayout()

        one = BoxLayout(size_hint=(1, 1))

        label = MyLabel(text='UCSD Web Scraper', font_size='32sp', halign='left', size_hint_x=.7, valign='top')
        credits_label = TimeLabel(text='Hi', font_size=14, halign='right',
                                  size_hint_x=.3, valign='top')

        Clock.schedule_interval(credits_label.update, 1)
        one.add_widget(label)
        one.add_widget(credits_label)

        root.add_widget(one)

        extra = BoxLayout(size_hint=(1, 1))
        extra.add_widget(MyLabel(text='Enter your classes below.', halign='left', valign='middle'))
        root.add_widget(extra)

        yes = BoxLayout(size_hint=(1, 13))
        yes.add_widget(Label(text='hi'))

        other_grid = GridLayout(cols=2, size_hint=(1, 13))
        grid = GridLayout(cols=2, size_hint=(1, 1))
        grid.add_widget(TextInput(text='hi', multiline=False, size_hint=(.8, 1)))
        grid.add_widget(Button(text='Enter', size_hint=(.2, 1)))

        clean_grid = GridLayout(cols=1, size_hint=(1,10))
        clean_grid.add_widget(Label(text='', size_hint=(1, 5)))
        clean_grid.add_widget(Button(text='Clean', size_hint=(1, 1)))
        clean_grid.add_widget(Button(text='Parse', size_hint=(1, 1)))
        clean_grid.add_widget(Label(text='', size_hint=(1, 5)))

        grid.add_widget(clean_grid)
        other_grid.add_widget(grid)

        classes_grid = GridLayout(cols=2, size_hint=(1, 1))
        classes_grid.add_widget(Label(text='Class here', size_hint=(.6, 1)))
        classes_grid.add_widget(Button(text='hi how are you', size_hint=(.4, 1)))

        classes_grid.add_widget(Label(text='Class here', size_hint=(.6, 1)))
        classes_grid.add_widget(Button(text='hi how are you', size_hint=(.4, 1)))

        classes_grid.add_widget(Label(text='Class here', size_hint=(.6, 1)))
        classes_grid.add_widget(Button(text='hi how are you', size_hint=(.4, 1)))

        classes_grid.add_widget(Label(text='Class here', size_hint=(.6, 1)))
        classes_grid.add_widget(Button(text='hi how are you', size_hint=(.4, 1)))

        begin_grid = GridLayout(cols=1, size_hint=(1,4))
        begin_grid.add_widget(Button(text='Begin', size_hint=(1,1)))

        other_grid.add_widget(classes_grid)


        root.add_widget(other_grid)
        root.add_widget(begin_grid)

        return root


if __name__ == '__main__':
    MainApp().run()
