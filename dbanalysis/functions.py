from datetime import datetime

def get_unix_timestamp(utc_date_string):
    if utc_date_string is None:
        return None
    date_obj = datetime.strptime(utc_date_string, '%Y-%m-%dT%H:%M:%SZ')
    return int(date_obj.timestamp())