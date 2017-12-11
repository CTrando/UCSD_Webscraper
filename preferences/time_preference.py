from preferences.preference import Preference


class TimePreference(Preference):
    def get_score(self, cur_class, time_interval):
        score = 0
        dist = cur_class.distance_from_interval(time_interval)
        if cur_class.inside_time(time_interval):
            score += 10
        # If it does overlaps in the interval reward the set a little less
        elif cur_class.overlaps_time(time_interval):
            score -= dist
        # Otherwise punish the set
        else:
            score -= 10 * dist

        # Make sure not earlier
        if cur_class.earlier_time(time_interval):
            score -= 100

        return score
