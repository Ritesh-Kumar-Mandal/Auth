from datetime import datetime, timedelta, timezone
import pytz


def get_local_date():
    return datetime.now()


def get_tz_date(tz: str):
    tz = pytz.timezone(tz)
    return datetime.now(tz)


def get_utc_date():
    return datetime.utcnow()


def get_time_minus(end_time: str):
    d = datetime.strptime(end_time, '%H%M') - timedelta(hours=0, minutes=1)
    return d.strftime('%H%M')


def get_time_add(end_time: str):
    d = datetime.strptime(end_time, '%H%M') + timedelta(hours=0, minutes=1)
    return d.strftime('%H%M')
