import datetime
import numpy as np

def from_hdays(fdict, date=datetime.date.today()):
    res = []
    for d in fdict:
        delta = abs(date - datetime.datetime.strptime(d,'%Y-%m-%d').date() )
        res.append(delta.days )
    return min(res)

def get_city(source, city):
    try:
        res = source[source.NAME.str.contains(city, case=False)].NAME.values[0]
    except IndexError:
        res = None
    return res

def test_h(liste, h):
    try:
        res = int(h)
        if res not in liste:
            res = 0
    except ValueError:
        res = 0
    return res
