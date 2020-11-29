﻿import pandas as pd
import datetime
from flask import Flask, request #, render_template, url_for,
from .utils import *
from pickle import Unpickler
#import json
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

    origin = request.args.get('origin')
    dest = request.args.get('dest')
    dep = request.args.get('dep')
    arr = request.args.get('arr')
    day = request.args.get('day')

    result = ""

    input = []

    creneaux = np.arange(7,24).tolist()
    if h_dep not in creneaux:
        h_dep = 0
    if h_arr not in creneaux:
        h_arr = 0

    try:
        dflight = datetime.datetime.strptime(day, '%Y-%m-%d').date()

        tmp_origin = get_city(cities, origin)
        tmp_dest = get_city(cities, dest)
        if (tmp_origin == None) or (tmp_dest == None):
            res = 'Pas d"estimation possible'
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
            input.append(h_dep)
        #FROM_HDAYS'
            input.append(abs(from_hdays(app.config['FERIES'], dflight)))
        #DEST_CITY_NAME
            input.append(CITY_lbl.transform([dest])[0])
        #DAY_OF_WEEK'
            input.append(dflight.weekday()+1)
        #ARR_TIME_BLK'
            input.append(h_arr)
        #UNIQUE_CARRIER
            input.append(CARRIER_lbl.transform([carrier])[0])

            result = int(round(regr['lin'].predict([input])[0], 0))

    except ValueError:
        result = "Erreur dans le format de date {}".format(day)

    return {'_In' : {'From' : origin, 'To': dest, 'Day' : day, 'Dep' : dep, 'Arr' : arr }, '_Out' : result}
