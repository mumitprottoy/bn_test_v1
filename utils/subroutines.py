import datetime
from django.utils import timezone as tz
from datetime import datetime
from django.utils.timezone import now
from django.utils.timesince import timesince


def current_timestamp() -> int:
    return int(tz.make_aware(
        datetime.datetime.now(), tz.get_default_timezone()).timestamp() * 1000) # milliseconds


def get_clean_dict(obj, target_key: str='_state') -> dict:
    _dict: dict = obj.__dict__.copy()
    if target_key in _dict: _dict.pop(target_key)
    return _dict   



def pretty_timesince(dt):
    if not isinstance(dt, datetime):
        return ""

    delta = now() - dt
    seconds = delta.total_seconds()

    if seconds < 10:
        return "just now"
    elif seconds < 60:
        return "a few seconds ago"

    time_str = timesince(dt).split(',')[0].strip() 
    # time_str = time_str.replace('minutes', 'minute')
    # time_str = time_str.replace('hours', 'hour')
    # time_str = time_str.replace('days', 'day')
    # time_str = time_str.replace('weeks', 'week')
    # time_str = time_str.replace('months', 'month')
    # time_str = time_str.replace('years', 'year')

    if time_str.startswith('1 '):
        return f"{time_str} ago"
    else:
        return f"{time_str} ago"
