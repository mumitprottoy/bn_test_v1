import datetime
from django.utils import timezone as tz
from datetime import datetime
from django.utils.timezone import now, make_aware, get_current_timezone, is_naive
from django.utils.timesince import timesince


def current_timestamp() -> int:
    return int(tz.make_aware(
        datetime.datetime.now(), tz.get_default_timezone()).timestamp() * 1000) # milliseconds


def get_clean_dict(obj, target_key: str='_state') -> dict:
    _dict: dict = obj.__dict__.copy()
    if target_key in _dict: _dict.pop(target_key)
    return _dict   



def pretty_timesince(dt):
    if is_naive(dt):
        dt = make_aware(dt, timezone=get_current_timezone())
    if not isinstance(dt, datetime):
        return ""

    delta = now() - dt
    seconds = delta.total_seconds()

    if seconds < 10:
        return "just now"
    elif seconds < 60:
        return "a few seconds ago"

    time_str = timesince(dt).split(',')[0].strip() 

    if time_str.startswith('1 '):
        return f"{time_str[:-1]} ago"
    else:
        return f"{time_str} ago"
