import pandas as pd
import datetime
from flask import Flask, request #, render_template, url_for,
from .utils import *
from pickle import Unpickler
import json
#import sys

#sys.setrecursionlimit(20000)

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']


with open(app.config['SOURCE_FILE'], 'rb') as file:
    unpickler = Unpickler(file)
    trips = unpickler.load()
    CITY_lbl = unpickler.load()
    cities = unpickler.load()
    CARRIER_lbl = unpickler.load()
    regr = unpickler.load()

@app.route('/')
def index():
   return "Anticipation des retards d'avions"

@app.route('/delay/')
def estimate():
    """
    Cette fonction estime le retard à l'arrivée d'un voyage entre 2 villes américaines, selon une régresion linéaire.

    Entrées
        * dflight : date du voyage au format AAAA-MM-JJ
        * origin : nom de la ville de départ
        * dest : nom de la ville d'arrivée
        * h_dep : heure 'pleine' de départ souhaitée (ex., 10 entre 10:00 et 10:59)
        * h_arr : heure 'pleine' d'arrivée souhaitée (ex., 14 entre 14:00 et 14:59)

    Sorties
        * le nom standard de la ville de départ
        * le nom standard de la ville de destination
        * le retard (min) estimé à l'arrivée
    """

    result = ""
    input = []
    origin = ''
    dest = ''
    dep = 0
    arr = 0
    day = ''

    if len(request.args) != 5:
        result = "Veuillez vérifier les paramètres passés"
    else:
        origin = request.args.get('origin')
        dest = request.args.get('dest')
        dep = request.args.get('dep')
        arr = request.args.get('arr')
        day = request.args.get('day')

        creneaux = np.arange(7,24).tolist()
        dep = test_h(creneaux, dep)
        arr = test_h(creneaux, arr)

        try:
            dflight = datetime.datetime.strptime(day, '%Y-%m-%d').date()

            tmp_origin = get_city(cities, origin)
            tmp_dest = get_city(cities, dest)
            if tmp_origin is None or tmp_dest is None:
                result = 'Pas d"estimation possible'
            else:
                origin, dest = tmp_origin, tmp_dest
                group, carrier  = trips[(trips.ORIGIN_CITY_NAME == origin) & \
                                        (trips.DEST_CITY_NAME == dest)]\
                                        [['DISTANCE_GROUP', 'UNIQUE_CARRIER']].values[0]
            #MONTH
                input.append(dflight.month)
            #ORIGIN_CITY_NAME
                input.append(CITY_lbl.transform([origin])[0])
            #DISTANCE_GROUP
                input.append(group)
            #DEP_TIME_BLK'
                input.append(dep)
            #FROM_HDAYS'
                input.append(abs(from_hdays(app.config['FERIES'], dflight)))
            #DEST_CITY_NAME
                input.append(CITY_lbl.transform([dest])[0])
            #DAY_OF_WEEK'
                input.append(dflight.weekday()+1)
            #ARR_TIME_BLK'
                input.append(arr)
            #UNIQUE_CARRIER
                input.append(CARRIER_lbl.transform([carrier])[0])

                result = int(round(regr['lin'].predict([input])[0], 0))

        except ValueError:
            result = "Erreur dans le format de date {}".format(day)

    return json.dumps({'_In' : {'1_From' : origin, '2_To': dest, '3_Day' : day, \
                                '4_Dep' : dep, '5_Arr' : arr }, \
                      '_Out' : {'1_Delay (min)' : result}}, \
                      sort_keys=True, indent=4)
