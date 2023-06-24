import datetime

def DtCalc(stTime,edTime):
    st = datetime.datetime.strptime(stTime, "%Y-%m-%d %H:%M")
    ed = datetime.datetime.strptime(edTime, "%Y-%m-%d %H:%M")
    rtn = ed - st
    y = round(rtn.total_seconds()/60/60)
    return y

def get_week_number(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
    day = date.weekday()
    return day
