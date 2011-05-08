import time

GH_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def to_timestamp(dt):
  tt = (dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second,
        dt.weekday(), 0, 0)
  return dt.strftime(GH_DATE_FORMAT)
