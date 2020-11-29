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

def get_trips_info(source, origin, dest):
    tmp = source[(source.ORIGIN_CITY_NAME == origin) & \
                (source.DEST_CITY_NAME == dest)][['DISTANCE_GROUP', 'UNIQUE_CARRIER']].values[0]
    return tmp[0], tmp[1]

#def delay_estimation(dflight="2016-04-10", \
#                     origin='Los Angeles, CA', dest='Las Vegas, NV', \
#                     h_dep=10, h_arr=14, group=1, carrier='WN'):
