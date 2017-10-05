from tkinter import *
from tkinter import font

from classpicker import ClassPicker
import scraper
from timeutils import TimeInterval


class Program(Frame):
    widgets = {}

    def __init__(self, master=None):
        super(Program, self).__init__(master)
        master.title('UCSD Web Registration Scraper')
        self.grid(padx=(20, 20), pady=(20, 20))
        master.minsize(width=720, height=480)
        master.maxsize(width=1920, height=1280)
        self.classes = []
        self.class_rows = []
        self.time_preferences = []
        self.results = []
        Program.widgets['classes'] = self.class_rows
        self.class_num = 0
        self.row_class_num = 2
        self.make_widgets()

    def make_widgets(self):
        self.preference_input = StringVar()
        self.class_input = StringVar()
        self.dept_input = StringVar()
        title_font = font.Font(family='Arial', size=25)

        self.text_box = Entry(self, textvariable=self.class_input)
        self.text_box.grid(row=2, column=0, columnspan=6, sticky=E+W)
        Program.widgets['text_box'] = self.text_box

        self.title = Label(self)
        self.title['text'] = 'UCSD Web Registration Scraper'
        self.title['font'] = title_font
        self.title.grid(row=0, column=0, columnspan=10, sticky=W)
        Program.widgets['title'] = self.title

        self.class_label = Label(self)
        self.class_label['text'] = 'Selected Classes'
        self.class_label.grid(row=1, column=10, sticky=W)
        Program.widgets['class_label'] = self.class_label

        self.enter_class_label = Label(self)
        self.enter_class_label['text'] = 'Enter in your classes here'
        self.enter_class_label.grid(row=1, column=0, columnspan=10, sticky=W)
        Program.widgets['enter_class_label'] = self.enter_class_label

        self.enter = Button(self)
        self.enter['text'] = 'Click to add your class'
        self.enter['command'] = self.add_class
        self.enter.grid(row=3, column=0, columnspan=6, sticky=E+W)
        Program.widgets['enter'] = self.enter

        self.start = Button(self)
        self.start['text'] = 'Start generating'
        self.start['command'] = self.run
        self.start.grid(row=4, column=0, columnspan=6, sticky=E+W)
        Program.widgets['start'] = self.start

        self.clear_selected_classes = Button(self)
        self.clear_selected_classes['text'] = 'Clear selected classes'
        self.clear_selected_classes['command'] = self.clear_classes
        self.clear_selected_classes.grid(row=5, column=0, columnspan=6, sticky=E+W)
        Program.widgets['clear_selected_class'] = self.clear_selected_classes

        self.clear_result = Button(self)
        self.clear_result['text'] = 'Clear results'
        self.clear_result['command'] = self.clear_results
        self.clear_result.grid(row=6,column=0, columnspan=6, sticky=E+W)
        Program.widgets['clear_result'] = self.clear_result

        self.quit = Button(self)
        self.quit['text'] = 'QUIT'
        self.quit['command'] = root.destroy
        self.quit.grid(row=7, column=0, columnspan=6, sticky=E+W)

        self.rowconfigure(8, minsize=100)

        self.enter_department_label = Label(self)
        self.enter_department_label['text'] = 'Enter a department to scrape'
        self.enter_department_label.grid(row=10, column=0, columnspan=6, sticky=W)

        self.enter_department = Entry(self, textvariable=self.dept_input)
        self.enter_department.grid(row=11, column=0, columnspan=6, sticky=E+W)

        self.enter_department_btn = Button(self)
        self.enter_department_btn['text'] = 'Click to webscrape department'
        self.enter_department_btn['command'] = self.scrape_department
        self.enter_department_btn.grid(row=12, column=0, columnspan=6, sticky=E+W)

        self.preferences = Label(self)
        self.preferences['text'] = 'Enter your time preferences'
        self.preferences.grid(row=10, column=10, sticky=W)

        self.preferences_entry = Entry(self, textvariable=self.preference_input)
        self.preferences_entry.grid(row=11, column=10, sticky=W)

        self.preferences_entry_btn = Button(self)
        self.preferences_entry_btn['text'] = 'Click to add a time preference'
        self.preferences_entry_btn['command'] = self.add_preference
        self.preferences_entry_btn.grid(row=12, column=10,sticky=W)

    def add_class(self):
        text = self.text_box.get()
        if len(text) <= 0:
            return
        self.text_box.delete(0, END)

        new_row = ClassButtonRow(self, text)
        self.class_rows.append(new_row)

        self.class_num += 1
        self.row_class_num += 1
        self.classes.append(text)
        print(text)

    def clear_classes(self):
        for row in self.class_rows:
            row.destroy()
        for row in self.class_rows:
            self.class_rows.remove(row)
        self.class_num = 0

    def run(self):
        self.clear_results()
        class_picker = ClassPicker()
        best_classes = class_picker.pick(self.classes, intervals=self.time_preferences)
        i = 5
        for best_class in best_classes:
            for sub_class in best_class.subclasses.values():
                self.results.append(ClassRow(self, sub_class))

    def clear_results(self):
        for result in self.results:
            result.destroy()

    def add_preference(self):
        self.time_preferences.append(TimeInterval(None, self.preference_input.get()))
        self.preferences_entry.delete(0, END)
        [print(str(i)) for i in self.time_preferences]

    def scrape_department(self):
        web_scraper = scraper.Scraper()
        web_scraper.login()
        web_scraper.pick_quarter()
        web_scraper.search_department(self.dept_input.get())
        web_scraper.iter_pages()


class ClassButtonRow:
    current_row = 2

    def __init__(self, Frame, text):
        self.Frame = Frame
        self.class_label = Label(Frame)
        self.class_label['text'] = text
        self.class_label.grid(row=ClassButtonRow.current_row, column=10, sticky=W)

        self.rm_button = Button(Frame)
        self.rm_button['text'] = 'Remove'
        self.rm_button['command'] = self.destroy
        self.rm_button.grid(row=ClassButtonRow.current_row, column=11, sticky=W)
        ClassButtonRow.current_row += 1

    def destroy(self):
        ClassButtonRow.current_row -= 1
        self.Frame.classes.remove(self.class_label['text'])
        self.class_label.destroy()
        self.rm_button.destroy()


class ClassRow:
    current_row = 15

    def __init__(self, Frame, class_template):
        self.data = class_template.data
        self.current_col = 0

        self.type_label = Label(Frame)
        self.type_label['text'] = self.data['TYPE'].strip()
        self.type_label.grid(row=ClassRow.current_row, column=self.current_col, sticky=W)
        self.current_col += 1

        self.course_num_label = Label(Frame)
        self.course_num_label['text'] = self.data['COURSE_NUM']
        self.course_num_label.grid(row=ClassRow.current_row, column=self.current_col, sticky=W)
        self.current_col += 1

        self.day_label = Label(Frame)
        self.day_label['text'] = self.data['DAYS']
        self.day_label.grid(row=ClassRow.current_row, column=self.current_col, sticky=W)
        self.current_col += 1

        self.time_label = Label(Frame)
        self.time_label['text'] = self.data['TIME']
        self.time_label.grid(row=ClassRow.current_row, column=self.current_col, sticky=W)
        self.current_col += 1

        ClassRow.current_row += 1

    def destroy(self):
        self.type_label.destroy()
        self.course_num_label.destroy()
        self.day_label.destroy()
        self.time_label.destroy()


root = Tk()
app = Program(master=root)
app.mainloop()
