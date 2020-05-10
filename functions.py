import pytz
from datetime import datetime

def getActualTime():
    tz = pytz.timezone('Europe/Warsaw')
    actualltime = datetime.now(tz).replace(microsecond=0, tzinfo=None)
    return actualltime