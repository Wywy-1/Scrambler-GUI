import datetime as dt

def get_time():
    """Returns the current date and time as 'MMM-dd,HH:MM:SS."""
    date = dt.datetime.now()

    return str(date.strftime("%h-%d,%Y,%H:%M:%S"))