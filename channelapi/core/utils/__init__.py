import datetime

def datetime_stringify(obj: datetime) -> str:
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.strftime("%Y-%m-%d %H:%M:%S")

def datetime_rebuild(obj: str) -> datetime:
    return datetime.strptime(obj, "%Y-%m-%d %H:%M:%S")

def get_now() -> str:
    return datetime_stringify(datetime.datetime.now())
