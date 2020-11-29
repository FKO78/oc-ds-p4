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

def delay_estimation(dflight="2016-04-10", \
                     origin='Los Angeles, CA', dest='Las Vegas, NV', \
                     h_dep=10, h_arr=14, group=1, carrier='WN'):

    """
        Cette fonction estime le retard à l'arrivée d'un voyage entre 2 villes américaines, selon une régresion linéaire.

        Entrées
            * dflight : date du voyage au format AAAA-MM-JJ
            * origin : nom de la ville de départ
            * dest : nom de la ville d'arrivée
            * h_dep : heure 'pleine' de départ souhaitée (ex., 10 entre 10:00 et 10:59)
            * h_arr : heure 'pleine' d'arrivée souhaitée (ex., 14 entre 14:00 et 14:59)
            * carrrier : le code (2 lettres) de la compagnie aérienne souhaitée dans la liste ci-dessous
                  AA  American Airlines Inc.
                  AS  Alaska Airlines Inc.
                  B6  JetBlue Airways
                  DL  Delta Air Lines Inc.
                  EV  ExpressJet Airlines LLC
                  F9  Frontier Airlines Inc.
                  HA  Hawaiian Airlines Inc.
                  NK  Spirit Air Lines
                  OO  SkyWest Airlines Inc.
                  UA  United Air Lines Inc.
                  VX  Virgin America
                  WN  Southwest Airlines Co

        Sorties
            * le nom standard de la ville de départ
            * le nom standard de la ville de destination
            * le retard (min) estimé à l'arrivée
    """

    input = []

    creneaux = np.arange(7,24).tolist()

    if h_dep not in creneaux:
        h_dep = 0

    if h_arr not in creneaux:
        h_arr = 0

#    try:
#        tmp_origin = cities[cities.NAME.str.contains(origin, case=False)].NAME.values[0]
#    except IndexError:
#        tmp_origin = None


#['MONTH', 'ORIGIN_CITY_NAME', 'DISTANCE_GROUP', 'DEP_TIME_BLK', 'FROM_HDAYS', 'DEST_CITY_NAME', 'DAY_OF_WEEK', 'ARR_TIME_BLK', 'UNIQUE_CARRIER']

#MONTH
    input.append(dflight.month)
#ORIGIN_CITY_NAME
    input.append(CITY_lbl.transform([origin])[0])
#DISTANCE_GROUP
    input.append(group)
#DEP_TIME_BLK'
    input.append(h_dep)
#FROM_HDAYS'
    input.append(abs(from_hdays(conf['FERIES'], dflight)))
#DEST_CITY_NAME
    input.append(CITY_lbl.transform([dest])[0])
#DAY_OF_WEEK'
    input.append(dflight.weekday()+1)
#ARR_TIME_BLK'
    input.append(h_arr)
#UNIQUE_CARRIER
    input.append(CARRIER_lbl.transform([carrier])[0])

    return int(round(regr['lin'].predict([input])[0], 0))
