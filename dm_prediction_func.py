def time_enumrate():
    times = []
    hour = 0
    while hour < 24:
        min  = 0
        while min < 60:
            times.append(hour * 100 + min)
            min += 5
        hour += 1
    return times
