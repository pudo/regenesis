import re
from datetime import datetime, timedelta

second = timedelta(seconds=1)

YEAR = re.compile('^(\d{4})$')
DATE = re.compile('^(\d{2}).(\d{2}).(\d{4})$')
DECADE = re.compile('^(\d{4})-(\d{4})$')
YEARS = re.compile('^(\d{4})/(\d{2})$')
WEEK = re.compile('^KW (\d{2})/(\d{4})$')
SEMESTER_WS = re.compile('^WS (\d{4})/(\d{2})$')
SEMESTER_SS = re.compile('^SS (\d{4})$')
Q1 = re.compile('^I/(\d{4})$')
Q2 = re.compile('^II/(\d{4})$')
Q3 = re.compile('^III/(\d{4})$')
Q4 = re.compile('^IV/(\d{4})$')

def parse_date(date_text):
    m = YEAR.match(date_text)
    if m is not None:
        year = int(m.group(1))
        return (datetime(year, 1, 1), datetime(year+1, 1, 1)-second)
    m = DATE.match(date_text)
    if m is not None:
        year, month, day = int(m.group(3)), int(m.group(2)), int(m.group(1))
        return (datetime(year, month, day), datetime(year, month, day)+timedelta(days=1)-second)
    m = DECADE.match(date_text)
    if m is not None:
        begin, end = int(m.group(1)), int(m.group(2))
        return (datetime(begin, 1, 1), datetime(end+1, 1, 1)-second)
    m = YEARS.match(date_text)
    if m is not None:
        begin, end = int(m.group(1)), int(m.group(1)[:2] + m.group(2))
        return (datetime(begin, 1, 1), datetime(end+1, 1, 1)-second)
    m = SEMESTER_WS.match(date_text)
    if m is not None:
        year = int(m.group(1))
        return (datetime(year, 10, 1), datetime(year+1, 4, 1)-second)
    m = SEMESTER_SS.match(date_text)
    if m is not None:
        year = int(m.group(1))
        return (datetime(year, 4, 1), datetime(year, 10, 1)-second)
    m = WEEK.match(date_text)
    if m is not None:
        week, year = int(m.group(1)), int(m.group(2))
        some_day = datetime(year, 1, 1) + timedelta(weeks=week-1)
        return some_day - timedelta(days=some_day.weekday()), \
               some_day + timedelta(days=7-some_day.weekday()) - second
    m = Q1.match(date_text)
    if m is not None:
        year = int(m.group(1))
        return (datetime(year, 1, 1), datetime(year, 4, 1)-second)
    m = Q2.match(date_text)
    if m is not None:
        year = int(m.group(1))
        return (datetime(year, 4, 1), datetime(year, 7, 1)-second)
    m = Q3.match(date_text)
    if m is not None:
        year = int(m.group(1))
        return (datetime(year, 7, 1), datetime(year, 10, 1)-second)
    m = Q4.match(date_text)
    if m is not None:
        year = int(m.group(1))
        return (datetime(year, 10, 1), datetime(year+1, 1, 1)-second)
    return (None, None)

def parse_bool(bool_text):
    return bool_text == 'J'

if __name__ == '__main__':
    print parse_date('2013')
    print parse_date('2013-2017')
    print parse_date('2013/17')
    print parse_date('WS 2007/08')
    print parse_date('KW 10/2013')
