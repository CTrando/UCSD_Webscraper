import random

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.patches as patches

from matplotlib import ticker

days = {'M': 0,
        'Tu': 1,
        'W': 2,
        'Th': 3,
        'F': 4
        }

day_list = ['M', 'Tu', 'W', 'Th', 'F']
x_ticks = [.5, 1.5, 2.5, 3.5, 4.5]

loc = plticker.MultipleLocator(base=.5)  # this locator puts ticks at regular intervals


class MyGraph:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

        plt.title('Your Generated Schedule')

        plt.grid()
        plt.ylabel('Times')
        plt.xlabel('Days')
        plt.xlim([0, 5])

        plt.ylim([6, 19])

        self.ax.yaxis.set_major_locator(loc)

        self.ax.xaxis.set_major_formatter(ticker.NullFormatter())
        self.ax.xaxis.set_minor_locator(ticker.FixedLocator(x_ticks))

        self.ax.xaxis.set_minor_formatter(ticker.FixedFormatter(day_list))
        self.ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.time_format))

        # self.add_time(2, (8, 10))
        # self.add_time(2, (13, 14))
        #
        # self.add_time(1, (7, 14))
        # self.add_time(0, (7, 10))

    @staticmethod
    def time_format(x, y):
        modifier = 'am'
        time = x * 60
        hour = str(int(time // 60) % 12)
        if x // 12 > 0:
            modifier = 'pm'
        if hour == '0':
            hour = '12'
        minute = str(int(time % 60))
        if '3' not in minute:
            minute += '0'
        return hour + ':' + minute + modifier

    def add_time(self, day, time):
        day = days[day]
        dy = time[1] - time[0]
        y = time[0]
        self.ax.add_patch(
            patches.Rectangle(
                (day, y),
                1,
                dy,
                color=(random.randint(0, 200) / 200,
                       random.randint(0, 200) / 200,
                       random.randint(0, 200) / 200)
            )
        )

    def show(self):
        plt.show()

#
# graph = MyGraph()
# graph.show()
