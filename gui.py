from tkinter import *
from tkinter import font

from classpicker import ClassPicker


class Program(Frame):
    widgets = {}

    def __init__(self, master=None):
        super(Program, self).__init__(master)
        master.title('UCSD Web Registration Scraper')
        self.grid(padx=(20, 20), pady=(20, 20))
        master.minsize(width=720, height=480)
        master.maxsize(width=1920, height=1280)
        self.classes = []
        self.class_num = 0
        self.row_class_num = 2
        self.make_widgets()

    def make_widgets(self):
        # self.quit = Button(self)
        # self.quit['text'] = 'QUIT'
        # self.quit['command'] = root.destroy
        # self.quit.grid(row=0, column=0)
        self.class_input = StringVar()
        title_font = font.Font(family='Arial', size=25)

        self.text_box = Entry(self, textvariable=self.class_input)
        self.text_box.grid(row=2, column=0, columnspan=10, sticky=W)
        Program.widgets['text_box'] = self.text_box

        self.title = Label(self)
        self.title['text'] = 'UCSD Web Registration Scraper'
        self.title['font'] = title_font
        self.title.grid(row=0, column=0, columnspan=10, sticky=W)
        Program.widgets['title'] = self.title

        self.enter_class_label = Label(self)
        self.enter_class_label['text'] = 'Enter in your classes here'
        self.enter_class_label.grid(row=1, column=0, columnspan=10, sticky=W)
        Program.widgets['enter_class_label'] = self.enter_class_label

        self.enter = Button(self)
        self.enter['text'] = 'Click to add your class'
        self.enter['command'] = self.add_class
        self.enter.grid(row=3, column=0, columnspan=10, sticky=W)
        Program.widgets['enter'] = self.enter

        self.start = Button(self)
        self.start['text'] = 'Start generating'
        self.start['command'] = self.run
        self.start.grid(row=4, column=0, columnspan=10, sticky=W)
        Program.widgets['start'] = self.start

        self.clear = Button(self)
        self.clear['text'] = 'Clear'
        self.clear['command'] = self.clear_classes
        self.clear.grid(row=5, column=0, columnspan=10, sticky=W)

    def add_class(self):
        text = self.text_box.get()
        if len(text) <= 0:
            return
        self.text_box.delete(0, END)

        class_label = Label(self)
        class_label['text'] = text
        class_label.grid(row=self.row_class_num, column=10, sticky=W)
        Program.widgets['class' + str(self.class_num)] = class_label

        self.class_num += 1
        self.row_class_num += 1
        self.classes.append(text)
        print(text)

    def clear_classes(self):
        for row in range(0, self.class_num):
            Program.widgets['class' + str(row)].destroy()
            del Program.widgets['class' + str(row)]
        self.class_num = 0

    def run(self):
        class_picker = ClassPicker()
        best_classes = class_picker.pick(self.classes)
        i = 5
        for best_class in best_classes:
            for sub_class in best_class.subclasses:
                row = ClassRow(self, sub_class)


class ClassRow:
    current_row = 15

    def __init__(self, Frame, class_template):
        self.data = class_template.data
        self.current_col = 0

        type_label = Label(Frame)
        type_label['text'] = self.data['TYPE'].strip()
        type_label.grid(row=ClassRow.current_row, column=self.current_col, sticky=W)
        self.current_col += 1

        course_num_label = Label(Frame)
        course_num_label['text'] = self.data['COURSE_NUM']
        course_num_label.grid(row=ClassRow.current_row, column=self.current_col, sticky=W)
        self.current_col += 1

        day_label = Label(Frame)
        day_label['text'] = self.data['DAYS']
        day_label.grid(row=ClassRow.current_row, column=self.current_col, sticky=W)
        self.current_col += 1

        time_label = Label(Frame)
        time_label['text'] = self.data['TIME']
        time_label.grid(row=ClassRow.current_row, column=self.current_col, sticky=W)
        self.current_col += 1

        ClassRow.current_row += 1


root = Tk()
app = Program(master=root)
app.mainloop()
