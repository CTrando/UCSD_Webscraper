import random
import threading

from kivy import Config
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

import startup
from ScheduleGraph import MyGraph
from classpicker import ClassPicker
from datautil import data_cleaner, data_parser
from gui.layouts.rootlayout import *
from gui.widgets.buttons import MyButton
from gui.widgets.labels import *
from scraper import scraper
from scraper.departmentscraper import DepartmentScraper
from settings import IMAGE_DIR, POPUP_TEXT_COLOR
from timeutil.timeutils import TimeIntervalCollection

Config.set('graphics', 'font-name', 'Times')
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('graphics', 'maxfps', 30)


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
        self.class_input = text_input = TextInput(multiline=False, size_hint=(.8, None), height=50)
        self.class_input.write_tab = False

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
        self.time_input = TextInput(hint_text='Ex: 8:00a-5:00p', size_hint=(.8, None), height=50, multiline=False)
        self.time_input.bind(on_text_validate=self.add_time_preference)
        self.time_input.write_tab = False

        # Adding the enter preference button
        add_preference_button = MyButton(text='Enter', size_hint=(.2, None), height=50,
                                         on_press=self.add_time_preference)

        time_box.add_widget(self.time_input)
        time_box.add_widget(add_preference_button)
        third_layer_1.add_widget(time_box)

        temp_box = BoxLayout(size_hint=(1, 5))
        self.time_preferences_box = StackLayout(padding=(0, 10), spacing=3, size_hint=(1, 1))
        temp_box.add_widget(self.time_preferences_box)

        third_layer_1.add_widget(temp_box)

        self.results_box = BoxLayout(orientation='vertical', padding=(10, 0), size_hint=(1, 8))

        # Box holding actions
        actions_box = BoxLayout(orientation='vertical', size_hint=(1, 1.5))
        scrape_box = BoxLayout()

        # Box holding the scraper buttons
        scrape_box.add_widget(MyButton(text='Scrape Classes', size_hint=(.5, 1), on_press=self.popup_webscrape))
        scrape_box.add_widget(MyButton(text='Scrape Departments', size_hint=(.5, 1), on_press=self.webscrape_dept))

        # Box holding parse and clean buttons
        data_base_box = BoxLayout()
        data_base_box.add_widget(MyButton(text='Parse', size_hint=(.5, 1), on_press=self.parse))
        data_base_box.add_widget(MyButton(text='Clean', size_hint=(.5, 1), on_press=self.clean))

        actions_box.add_widget(scrape_box)
        actions_box.add_widget(data_base_box)

        third_layer_1.add_widget(actions_box)

        # The second half of the third layer
        third_layer_2 = BoxLayout(size_hint=(.5, 1), orientation='vertical')
        third_layer_2.add_widget(MyLabel(text='', valign='center', size_hint=(1, 1)))

        # Grid with all the classes
        self.classes_box = classes_box = StackLayout(padding=(10, 0), spacing=3, size_hint=(1, 12))

        third_layer_2.add_widget(classes_box)

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
        if len(self.class_input.text) == 0:
            return
        self.class_input.text = self.class_input.text.rstrip().strip()

        self.class_rows.append(
            ClassRow(widget=self.classes_box, class_name=self.class_input.text))
        print([row.class_name for row in self.class_rows])
        Clock.schedule_once(self.focus_text)
        self.class_input.text = ''

    def focus_text(self, value):
        self.class_input.focus = True

    def focus_time_input(self, value):
        self.time_input.focus = True

    def add_time_preference(self, value):
        if len(self.time_input.text) == 0:
            return
        self.time_prfs.append(
            ClassRow(parent_list=MainApp.time_prfs, widget=self.time_preferences_box,
                     color=(.8, .8, .92, 1),
                     class_name=self.time_input.text))
        self.time_input.focus = True
        Clock.schedule_once(self.focus_time_input)
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

    def popup_webscrape(self, value):
        # Box layouts for positioning
        info_box = BoxLayout(orientation='vertical', size_hint=(1, 1))
        username_box = BoxLayout(orientation='vertical', size_hint=(.5, 1))
        password_box = BoxLayout(orientation='vertical', size_hint=(.5, 1))

        # Widgets which contain information about username and password
        self.username_input = TextInput(size_hint=(.5, None), height=50)
        self.password_input = TextInput(size_hint=(.5, None), height=50)
        login_button = MyButton(text='Login', size_hint=(.5, 1), on_press=self.webscrape)

        username_box.add_widget(MyLabel(text='Enter your username:', size_hint=(.5, None), height=50))
        self.username_input.multiline = False
        self.username_input.write_tab = False
        username_box.add_widget(self.username_input)

        password_box.add_widget(MyLabel(text='Enter your password:', size_hint=(.5, None), height=50))
        self.password_input.multiline = False
        # Setting it to password
        self.password_input.password = True
        self.password_input.write_tab = False
        # Binding it to make it login with enter press
        self.password_input.bind(on_text_validate=self.webscrape)
        password_box.add_widget(self.password_input)

        info_box.add_widget(username_box)
        info_box.add_widget(password_box)
        info_box.add_widget(Label(size_hint=(1, 1)))

        info_box.add_widget(login_button)
        info_box.add_widget(Label(size_hint=(1, 1)))

        popup = Popup(title='Login', title_size='24sp', title_color=(0, 0, 0, 1), size_hint=(.8, .8), content=info_box)
        popup.background = IMAGE_DIR + '/popup_background_logo.jpg'
        popup.open()

    def webscrape(self, value):
        username = self.username_input.text
        password = self.password_input.text
        scrape = scraper.Scraper(username=username, password=password)
        scrape.scrape()

    def webscrape_dept(self, value):
        dept_scraper = DepartmentScraper()
        dept_scraper.scrape()

    def graph_schedule(self, schedule):
        graph = MyGraph()
        for cl in schedule:
            color = (random.randint(150, 200) / 200,
                     random.randint(150, 200) / 200,
                     random.randint(150, 200) / 200)
            for subclass in cl.subclasses.values():
                # Using the pair in order to hit the PHYS classes with weird stuff
                day_time_pairs = subclass.interval.day_time_pairs
                # Make sure there are pairs
                if not day_time_pairs:
                    continue

                # Add the graph if the class and day exists
                for entry in day_time_pairs:
                    day = entry[0]
                    times = entry[1]

                    startTime = times[0].hour + times[0].minute / 60
                    endTime = times[1].hour + times[1].minute / 60
                    graph.add_class_time(day=day, time=[startTime, endTime], color=color, text=cl.data['COURSE_NUM'])

        graph.show()

    def begin(self, value):
        self.results_box.clear_widgets()

        # Creating popup and results content
        popup = Popup(title='Results', title_size='24sp', title_color=(0, 0, 0, 1), size_hint=(.8, .8))
        results_box = StackLayout(size_hint=(1, 1), padding=[10, 10])
        popup.background = IMAGE_DIR + '/popup_background_logo.jpg'
        popup.add_widget(results_box)

        self.best_classes = []

        # Using multi-threading to make UI responsive while loading
        # Thread will end upon finish, and will update best classes and the results box
        class_picker_thread = threading.Thread(target=self.pick_classes, args=(self, results_box, popup))
        class_picker_thread.start()
        popup.open()

    @staticmethod
    def pick_classes(val, results_box, popup):
        """
        Will pick classes through multi-threading and will add the class rows to the popup.
        Will open the popup once the thread has completed its actions.
        :param val: Passes in the MainApp instance
        :param results_box: Where the class results are placed
        :param popup: The popup that will be shown
        """

        # picking the class after making the widgets to allow for error handling
        try:
            class_picker = ClassPicker()
            classes = [row.class_name for row in val.class_rows]
            intervals = [TimeIntervalCollection(None, row.class_name) for row in val.time_prfs]
            val.best_classes = class_picker.pick(inputs=classes, intervals=intervals)
        except Exception as e:
            results_box.add_widget(MyLabel(text=str(e), size_hint=(1, 1), valign='top'))

        for best_class in val.best_classes:
            # Init the variables
            class_desc = ''
            sub_class_str = ''

            # A temp container for the class description and sub class
            temp_box = BoxLayout(orientation='vertical', size_hint=(.5, None))

            for sub_class in best_class.subclasses.values():
                class_desc = sub_class.data['DESCRIPTION']
                sub_class_str += val.format_class(sub_class) + '\n'

            temp_box.add_widget(
                # Putting the class description as the first label
                MyLabel(text=class_desc, text_color=POPUP_TEXT_COLOR, valign='top', halign='left', size_hint=(1, .2)))
            # Then the actual class data itself
            temp_box.add_widget(
                MyLabel(text=sub_class_str, text_color=POPUP_TEXT_COLOR, font_size='14sp', valign='top', halign='left',
                        size_hint=(1, .8)))
            # Add the container to the results box
            results_box.add_widget(temp_box)

        # If best classes actually has classes
        if val.best_classes:
            results_box.add_widget(
                MyButton(text='Click to see a visual', valign='bottom', size_hint=(1, .2), on_press=val.show_schedule))

    def show_schedule(self, value):
        self.graph_schedule(self.best_classes)


class ClassRow():
    def __init__(self, parent_list=MainApp.class_rows, color=(.97, .97, .97, 1), **kwargs):
        self.parent_list = parent_list
        if 'class_name' in kwargs:
            self.class_name = kwargs['class_name'].upper()
        else:
            self.class_name = ''
        if 'widget' in kwargs:
            self.layout = BoxLayout(size_hint=(1, None), height=50)
            self.widget = kwargs['widget']
            self.label = MyLabel(text=self.class_name, halign='center', valign='center',
                                 size_hint=(.6, None), background_color=color,
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
    startup.start()
    MainApp().run()
