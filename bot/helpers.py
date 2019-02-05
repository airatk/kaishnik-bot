import datetime

def get_week(is_reverse):
    if datetime.datetime.today().isocalendar()[1] % 2 == 0:
        return "Эта неделя чётная." if not is_reverse else "Эта неделя нечётная."
    else:
        return "Эта неделя нечётная." if not is_reverse else "Эта неделя чётная."
