import pytz
from pytz import timezone, common_timezones
from datetime import datetime


def local_to_utc(local_time, local_tz, aware=True):
    if local_tz not in common_timezones:
        raise ValueError('Timezone: %s is not in common list' % (local_tz))
    utc = pytz.utc
    tz = timezone(local_tz)
    if aware:
        time = tz.localize(datetime.strptime(local_time, '%d/%m/%Y %H:%M'))

        return time.astimezone(utc)
    else:
        time = tz.localize(datetime.strptime(local_time, '%d/%m/%Y %H:%M'))
        time = time.astimezone(utc)

        return time.replace(tzinfo=None)


def utc_to_local(utc_time, local_tz):
    if local_tz not in common_timezones:
        raise ValueError('Timezone: %s is not in common list' % (local_tz))
    fmt = '%d/%m/%Y %H:%M'
    local_tz = timezone(local_tz)
    utc_time = pytz.utc.localize(utc_time)
    local_time = utc_time.astimezone(local_tz)

    return local_time.strftime(fmt)
