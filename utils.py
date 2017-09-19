import datetime, time

preset_days = ['M', 'Tu', 'W', 'Th', 'F']


class TimeInterval:
    def __init__(self, day_col, time_col):
        self.sanitize_inputs(day_col, time_col)

    def sanitize_inputs(self, day_col, time_col):
        self.days = self.get_days(day_col)
        self.times = self.get_times(time_col)


    def get_days(self, day_list):
        ret_days = []
        for day in preset_days:
            if day in day_list:
                ret_days.append(day)
        return ret_days

    def get_times(self, time_col):
        if time_col.find('-') == -1:
            return []
        ret_times = []
        for b_time in time_col.split('-'):
            b_time += 'm'
            g_time = time.strptime(b_time,'%I:%M%p')
            ret_times.append(g_time)
        return ret_times

    def overlaps(self, other):
        for day in self.days:
            if day in other.days:
                if self.overlaps_times(other):
                    return True
        return False

    def overlaps_times(self, other):
        my_start = self.times[0]
        my_end = self.times[1]

        other_start = other.times[0]
        other_end = other.times[1]

        return (other_start <= my_start <= other_end) or (my_start <= other_start <= my_end)