import time


def to_timestamp(dt):
  tt = (dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second,
        dt.weekday(), 0, 0)
  return time.mktime(tt)
