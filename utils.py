import consts
import json
import os
import random

from datetime import datetime, timezone, timedelta


def loads_data(file_path):
    data = None
    
    with open(file_path, "r") as f_in:
        data = json.loads(f_in.read())
        
    return data

def dumps_data(file_path, data):
    with open(file_path, "w") as f_out:
        f_out.write(json.dumps(data, indent=2))
        
def get_current_datetime_str():
    return datetime.now(consts.TZ_INFO).strftime(consts.DATETIME_FORMAT)

def get_current_day_str():
    return datetime.now(consts.TZ_INFO).strftime(consts.DATE_FORMAT)

def get_millennium_datetime_str():
    epoch_time = datetime.fromtimestamp(946684800, timezone.utc)
    return epoch_time.strftime(consts.DATETIME_FORMAT)

def get_future_datetime_str(days_to_add):
    future_datetime = datetime.now(consts.TZ_INFO) + timedelta(days=days_to_add)
    return future_datetime.strftime(consts.DATETIME_FORMAT)

def parse_str_to_datetime(string):
    return datetime.strptime(string, consts.DATETIME_FORMAT)

def calculate_seconds_between_datetimes(datetime_start, datetime_str_end=None):
    if not isinstance(datetime_start, datetime):
        datetime_start = datetime.strptime(datetime_start, consts.DATETIME_FORMAT)
        datetime_start = datetime_start.astimezone(consts.TZ_INFO)
    
    if datetime_str_end:
        datetime_end = datetime.strptime(datetime_str_end, consts.DATETIME_FORMAT)
    else:
        datetime_end = datetime.now(consts.TZ_INFO)

    delta = datetime_end - datetime_start
    
    return delta.total_seconds()

def get_random_floating_number(min_value, max_value):
    return round(random.uniform(min_value, max_value), 2)
