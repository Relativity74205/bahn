from typing import List, Tuple
from datetime import datetime, timedelta
import math


def get_missing_default_plan_dates(current_time: datetime, last_datehour: str, max_default_plans: int) \
        -> List[Tuple[int, int, int, int]]:
    if last_datehour is not None:
        last_time = get_last_default_plan_time(last_datehour)
    else:
        last_time = None

    if last_time is not None:
        time_delta = math.floor((last_time - current_time).total_seconds() / (60 * 60))
        amount_missing_datehours = max_default_plans - time_delta - 1
    else:
        last_time = current_time.replace(microsecond=0, second=0, minute=0) - timedelta(hours=1)
        amount_missing_datehours = max_default_plans + 1

    missing_dates = generate_missing_dates(last_time, amount_missing_datehours)
    return missing_dates


def generate_missing_dates(last_time: datetime, amount_missing_dates: int) -> List[Tuple[int, int, int, int]]:
    missing_dates = []
    for i in range(amount_missing_dates):
        default_plan_time = last_time + timedelta(hours=i + 1)
        missing_dates.append(default_plan_time)

    missing_dates_tuple = convert_missing_dates(missing_dates)

    return missing_dates_tuple


def convert_missing_dates(missing_dates: List[datetime]) -> List[Tuple[int, int, int, int]]:
    missing_dates = [(missing_date.year,
                      missing_date.month,
                      missing_date.day,
                      missing_date.hour) for missing_date in missing_dates]
    return missing_dates


def get_last_default_plan_time(last_datehour: str) -> datetime:
    return datetime.strptime(last_datehour, '%Y%m%d%H')
