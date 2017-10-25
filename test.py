import random

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.patches as patches
import datetime

def add_time(ax, day, time):
    dy = time[1] - time[0]
    y = time[0]
    ax.add_patch(
        patches.Rectangle(
            (day - .5, y),
            1,
            dy,
            color=(random.randint(0, 200)/200,
                   random.randint(0, 200)/200,
                   random.randint(0, 200)/200)
        )
    )


days = ['M', 'T', 'W', 'Th', 'F']
x = [1, 2, 3, 4, 5]

fig, ax = plt.subplots()
loc = plticker.MultipleLocator(base=.5) # this locator puts ticks at regular intervals

plt.title('Your Generated Schedule')

plt.grid()
plt.ylabel('Times')
plt.xlabel('Days')
plt.xticks(x, days)
plt.xlim([0, 6])
plt.ylim([6, 19])

add_time(ax, 2, (8, 10))
add_time(ax, 2, (13, 14))
ax.yaxis.set_major_locator(loc)


plt.show()
