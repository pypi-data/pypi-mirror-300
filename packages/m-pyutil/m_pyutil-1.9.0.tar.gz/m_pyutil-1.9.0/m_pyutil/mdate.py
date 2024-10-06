import datetime
from enum import Enum


class Format(Enum):
    YYYY = '%Y'
    YYYY_MM = '%Y-%m'
    YYYY_MM_DD = '%Y-%m-%d'
    YYYY_MM_DD_HH = '%Y-%m-%d %H'
    YYYY_MM_DD_HH_MI = '%Y-%m-%d %H:%M'
    YYYY_MM_DD_HH_MI_SS = '%Y-%m-%d %H:%M:%S'


class DeltaType(Enum):
    DAY = 3
    HOUR = 4
    MIN = 5
    SEC = 6


def nowt() -> str:
    return datetime.datetime.now().strftime(Format.YYYY_MM_DD_HH_MI_SS.value)


def nowd() -> str:
    return datetime.datetime.now().strftime(Format.YYYY_MM_DD.value)


def add_secs(time_str: str,
             delta: int = 1) -> str:
    return add_times(time_str=time_str, delta=delta, delta_type=DeltaType.SEC)[:len(time_str)]


def add_mins(time_str: str,
             delta: int = 1) -> str:
    return add_times(time_str=time_str, delta=delta, delta_type=DeltaType.MIN)[:len(time_str)]


def add_hours(time_str: str,
              delta: int = 1) -> str:
    return add_times(time_str=time_str, delta=delta, delta_type=DeltaType.HOUR)[:len(time_str)]


def add_days(date_str: str,
             delta: int = 1) -> str:
    return add_times(time_str=date_str, delta=delta, delta_type=DeltaType.DAY)[:len(date_str)]


def add_times(time_str: str,
              delta: int = 1,
              delta_type: DeltaType = DeltaType.SEC,
              return_format: Format = Format.YYYY_MM_DD_HH_MI_SS) -> str:
    full_time = '0000-00-00 00:00:00'
    time_str = time_str + full_time[len(time_str):]
    time = datetime.datetime.strptime(time_str, Format.YYYY_MM_DD_HH_MI_SS.value)
    if delta_type == DeltaType.SEC:
        time = time + datetime.timedelta(seconds=delta)
    elif delta_type == DeltaType.MIN:
        time = time + datetime.timedelta(minutes=delta)
    elif delta_type == DeltaType.HOUR:
        time = time + datetime.timedelta(hours=delta)
    elif delta_type == DeltaType.DAY:
        time = time + datetime.timedelta(days=delta)
    else:
        raise ValueError(f'delta_type={type(delta_type)} is not supported')
    return time.strftime(return_format.value)
