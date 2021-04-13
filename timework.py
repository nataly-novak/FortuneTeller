import pytz
import datetime


def toUTC(date, time, zone):
    local_time = pytz.timezone(zone.rstrip())
    line = date + " " + time+":00"
    naive_datetime = datetime.datetime.strptime(line, "%Y-%m-%d %H:%M:%S")
    local_datetime = local_time.localize(naive_datetime, is_dst=None)
    utc_datetime = local_datetime.astimezone(pytz.utc)
    conversion = (str(utc_datetime).split(sep="+")[0]).rsplit(sep=":",maxsplit=1)[0]+" UTC"
    return conversion


def currentUTC():
    current = str(datetime.datetime.utcnow())
    current = current.split(sep=".")[0]
    current = current.rsplit(sep=":",maxsplit=1)[0]
    return current

def toLocal(date, time, zone):
    local_time = pytz.timezone(zone.rstrip())
    utc_time = pytz.timezone("UTC")
    line = date + " " + time+":00"
    naive_datetime = datetime.datetime.strptime(line, "%Y-%m-%d %H:%M:%S")
    utc_datetime = utc_time.localize(naive_datetime, is_dst=None)
    local_datetime = utc_datetime.astimezone(local_time)
    conversion = (str(local_datetime).split(sep="+")[0]).rsplit(sep=":",maxsplit=1)[0]+" "+ zone
    return conversion

def getToday(zone):
    current = currentUTC().split(sep=" ")
    date = toLocal(current[0],current[1],zone).split(sep=' ',maxsplit=1)[0]
    return date

def utcToday():
    return currentUTC().split(sep=" ")[0]


def timeConversion(time, zone1, zone2):
        date = getToday(zone1)
        utctime = (toUTC(date, time, zone1).rsplit(sep=" ", maxsplit=1)[0]).split(sep=" ")
        localtime = toLocal(utctime[0],utctime[1], zone2).split(sep=' ')
        return localtime[1]

def getToday(zone):
    current = currentUTC().split(sep=" ")
    date = toLocal(current[0],current[1],zone).split(sep=' ',maxsplit=1)[0]
    return date

def utcToday():
    return currentUTC().split(sep=" ")[0]










