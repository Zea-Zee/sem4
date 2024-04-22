def get_countable(num, label):
    if num == 0:
        return ''
    # print(str(num)[-1])
    if str(num)[-1] == '1':
        return f"{num} {label}"
    return f"{num} {label}s"


def get_postfix(idx, filled):
    if filled[idx]:
        if sum(filled[idx + 1:]) > 1:
            return ', '
        if sum(filled[idx + 1:]) == 1:
            return ' and '
    return ''



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
    filled = [1 if years else 0, 1 if days else 0,
              1 if hours else 0, 1 if minutes else 0, 1 if s else 0]
    return (f"""{get_countable(years, 'year')}{get_postfix(0, filled)}\
{get_countable(days, 'day')}{get_postfix(1, filled)}\
{get_countable(hours, 'hour')}{get_postfix(2, filled)}\
{get_countable(minutes, 'minute')}{get_postfix(3, filled)}\
{get_countable(s, 'second')}""")


print(format_duration(0))
print(format_duration(1))
print(format_duration(60))
print(format_duration(253374061))
