from datetime import datetime


def human_time(t: int):
    dt = datetime.fromtimestamp(t)
    return dt.strftime("%Y-%m-%d %H:%M")
