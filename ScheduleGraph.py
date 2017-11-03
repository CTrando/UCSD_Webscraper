import random
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.patches as patches
from matplotlib import ticker
from settings import DAY_GRAPH_INTERVAL

# Dict of days to corresponding index
days = {'M': 0,
        'Tu': 1,
        'W': 2,
        'Th': 3,
        'F': 4}

# List of days
day_list = ['M', 'Tu', 'W', 'Th', 'F']
# Locations for the x ticks
# Note: The ticks are spaced by the day graph interval because they are between days
# Spaced like this for readability
x_ticks = [days['M'] + DAY_GRAPH_INTERVAL,
           days['Tu'] + DAY_GRAPH_INTERVAL,
           days['W'] + DAY_GRAPH_INTERVAL,
           days['Th'] + DAY_GRAPH_INTERVAL,
           days['F'] + DAY_GRAPH_INTERVAL]

# this locator puts ticks at regular intervals of .5 - half an hour
loc = plticker.MultipleLocator(base=.5)


class MyGraph:
    """
    This class will graph the given schedule using matplotlib and pyplot.
    """

    def __init__(self):
        # Initializing the subplots and axes
        self.fig, self.ax = plt.subplots()

        self.fig.canvas.set_window_title('Your Generated Schedule')

        # Setting the title - note using plt
        plt.title('Your Generated Schedule')

        # Setting it to grid mode
        plt.grid()

        # Setting axes names
        plt.ylabel('Times')
        plt.xlabel('Days')

        # Setting formatter to null and then to days
        self.ax.xaxis.set_major_formatter(ticker.NullFormatter())
        self.ax.xaxis.set_minor_locator(ticker.FixedLocator(x_ticks))
        # Setting min and max for x
        self.ax.set_xlim(xmin=0, xmax=5)
        # Setting xaxis formatter to days
        self.ax.xaxis.set_minor_formatter(ticker.FixedFormatter(day_list))

        # Setting spacing to half an hour
        self.ax.yaxis.set_major_locator(loc)
        # Using specific function for parsing hours
        self.ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.time_format))
        # Set limit to go from 0 to 24
        self.ax.set_ylim(ymin=0, ymax=24)
        # Set the yaxis to inverted mode like WebReg
        self.ax.invert_yaxis()

    @staticmethod
    def time_format(x, y):
        """
            This function will take in an x and y, with the x being the axis of focus. It will
            format the x accordingly depending whether it is AM or PM and modulus it if it goes
            over 12 hours.

            :param x given in hours
            :param y unimportant, do not know why this is passed in
        """

        # Modifier set to am at first
        modifier = 'am'
        minutes = x * 60
        # Getting only the hours part
        hour = str(int(minutes // 60) % 12)
        # Check if it pm by seeing if modulus is greater than 1 and if minutes/12 is odd
        # to produce PM instead of AM.
        # Ex. 13/12 % 2 = 1 so it goes PM
        # But 26/12 % 2 = 0 so it goes AM
        if x // 12 > 0 and x // 12 % 2 == 1:
            modifier = 'pm'
        # In the case when hour is 0 then it becomes 12 o'clock
        if hour == '0':
            hour = '12'

        # Redefine minutes to be whole number minute
        minutes = str(int(minutes % 60))
        # Append a 0 if it is not :30 - TODO change this
        if '3' not in minutes:
            minutes += '0'
        # Return the string formatted correctly
        return '{}:{}{}'.format(hour, minutes, modifier)

    def add_class_time(self, day, time, text=None, color=None):
        """
        Will add the given class time to the graph. Only one at a time.
        :param day: The day of the class
        :param time: The times of the class
        :param text: The name of the class
        :param color: The color of the class
        """

        # Randomize it if none is passed in
        if not color:
            color = (random.randint(0, 200) / 200,
                     random.randint(0, 200) / 200,
                     random.randint(0, 200) / 200)

        # Get the index of the day from days dict
        day = days[day]
        # Find the height of the rectangle from given times
        dy = time[1] - time[0]
        # Find starting y
        y = time[0]
        # Draw the rectangle
        self.ax.add_patch(
            patches.Rectangle(
                xy=(day, y),
                width=1,
                height=dy,
                color=color
            )
        )
        # Put the text
        self.ax.text(day, y + dy, text)

        # Rescale the graph
        self.ax.relim()
        self.ax.autoscale()

    @staticmethod
    def show():
        """
        Shows the graph.
        """
        plt.show()
