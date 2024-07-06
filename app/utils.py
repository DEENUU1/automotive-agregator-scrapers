import datetime


def get_hashed_run_id() -> str:
    return str(hash(datetime.datetime.now()))
