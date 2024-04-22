def get_countable(num, label):
    if num == 0:
        return ""
    # print(str(num)[-1])
    if str(num)[-1] == "1":
        return f"{num} {label} "
    return f"{num} {label}s "


def format_duration(s):
    if s == 0:
        return "now"
    years = s // (365 * 24 * 3600)
    s = s - (years * 365 * 24 * 3600)
    days = s // (24 * 3600)
    s = s - (days * 24 * 3600)
    hours = s // (3600)
    s = s - (hours * 3600)
    minutes = s // (60)
    s = s - (minutes * 60)
    return f"""{get_countable(years, 'year')}{get_countable(days, 'day')}\
{get_countable(hours, 'hour')}{get_countable(minutes, 'minute')}\
{get_countable(s, 'second')[:-1]}"""


print(format_duration(0))
print(format_duration(1))
print(format_duration(60))
print(format_duration(61))
