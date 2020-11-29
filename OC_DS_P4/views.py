import pandas as pd
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

    origin = request.args.get('origin')
    dest = request.args.get('dest')
    dep = request.args.get('dep')
    arr = request.args.get('arr')
    day = request.args.get('day')

    result = ""

    try:
        dflight = datetime.datetime.strptime(day, '%Y-%m-%d').date()

        tmp_origin = get_city(cities, origin)
        tmp_dest = get_city(cities, dest)
        if (tmp_origin == None) or (tmp_dest == None):
            res = 'Pas d"estimation possible'
        else:
            origin, dest = tmp_origin, tmp_dest
            group, carrier  = trips[(trips.ORIGIN_CITY_NAME == origin) & (trips.DEST_CITY_NAME == dest)][['DISTANCE_GROUP', 'UNIQUE_CARRIER']].values[0]
            estimation = delay_estimation(origin=origin, dest=dest, h_dep=dep, h_arr=arr, dflight=dflight, group=group, carrier=carrier)

    except ValueError:
        result = "Erreur dans le format de date {}".format(day)

    return {'_In' : {'From' : origin, 'To': dest, 'Day' : day, 'Dep' : dep, 'Arr' : arr }, '_Out' : result}
