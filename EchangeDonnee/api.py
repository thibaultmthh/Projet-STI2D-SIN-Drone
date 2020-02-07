#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask import redirect, request
import random
import json

app = Flask(__name__)


datas = {"temperature": 0,
         "fumee": False,
         "presence": False,
         "luminosite": 0,
         "deplacement": "standby",
         "batterie": 0,
         "alerte": None}


"""
temperature
fummée
presence drone
luminositée
donnée de deplacement
batterie
alerte
"""


def get_data(data):
    return datas[data]


def set_data(index, data):
    datas[index] = data
    return "OK"


def gen_int():
    return str(random.randint(10, 25))


def gen_bool():
    if random.random() < 0.5:
        return "true"
    else:
        return 'false'


def gen_deplacement():
    if random.random() < 0.5:
        return "forward"
    elif random.random() < 0.3:
        return "none"
    else:
        return 'backward'


routes = {"index": "/",
          "get_temperature": '/get/temperature',
          "get_fumee": '/get/fumee',
          "get_presence": "/get/presence",
          "get_luminosite": "/get/luminosite",
          "get_deplacements": "/get/deplacement",
          "get_batterie": "/get/batterie",
          "get_alert": "/get/alerte",
          "get_all_datas": "/get/all"}


@app.errorhandler(404)
def error404(error):
    return redirect('/')


@app.route("/")
def index(*arg):
    text = ""
    for x, y in routes.items():
        text += " <a href = {} > {} </a> <br>".format(y, x)
    return text

# routes pour recuperer des infos

@app.route(routes["get_all_datas"])
def xddaahah():
    return datas

@app.route(routes["get_temperature"])
def get_temperature():
    return get_data("temperature")


@app.route(routes["get_fumee"])
def get_fumee():
    return get_data('fumee')


@app.route(routes["get_presence"])
def get_presence():
    return get_data("presence")


@app.route(routes["get_luminosite"])
def page_get_luminosite():
    return get_data("luminosite")


@app.route(routes["get_deplacements"])
def get_deplacements():
    return get_data("deplacement")


@app.route(routes["get_batterie"])
def get_batterie():
    return get_data("batterie")


@app.route(routes["get_alert"])
def get_alert():
    return get_data("alert")


# routes pour set des info

@app.route("/set", methods=['GET', 'POST'])
def page_set():

    for key, data in request.form.items():
        set_data(key, data)
    return "OK"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


"""
temperature
fummée
presence drone
luminositée
donnée de deplacement
batterie
alerte
"""
