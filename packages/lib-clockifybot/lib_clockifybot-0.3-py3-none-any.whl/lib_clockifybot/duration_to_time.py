from datetime import timedelta as td


def duration_to_time(duration_str):
    duration_str = duration_str[2:]
    hours, minutes, seconds = 0, 0, 0
    start = 0
    for i, char in enumerate(duration_str):
        if not char.isdigit():
            end = i
            if char == "H":
                hours = int(duration_str[start:end])
            elif char == "M":
                minutes = int(duration_str[start:end])
            elif char == "S":
                seconds = int(duration_str[start:end])
            start = i + 1
    return td(hours=hours, minutes=minutes, seconds=seconds)
