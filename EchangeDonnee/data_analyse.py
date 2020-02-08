import time
import requests
import json

ip = '127.0.0.1'
port = '5000'

SEUIL_LUMINOSITE = 24
SEUIL_TEMPERATURE = 26
SEUIL_BATTERIE = 10

def get_all_datas(ip,port):
    reponse = requests.get("http://{}:{}/get/all".format(ip,port))
    datas = json.loads(reponse.text)
    return datas

def set_data(dataname, value, ip, port):
    print(value)
    dict = {dataname: value}
    #dict = json.dumps(dict)
    print(dict)
    reponse = requests.post("http://{}:{}/set".format(ip,port), data =dict )
    print(reponse.text)
"""
temperature
fummée
presence drone
luminositée
donnée de deplacement
batterie
alerte
"""
def gen_alert(ip, port):
    datas = get_all_datas(ip,port)
    alertes = []
    print(datas["fumee"])
    if int(datas['luminosite']) < SEUIL_LUMINOSITE:
        alertes.append('luminosite too low')
    if int(datas['temperature']) > SEUIL_TEMPERATURE:
        alertes.append("temperature too high")
    if datas['fumee'] == "True":
        print("ffe")
        alertes.append("fummee oulala")
    if int(datas["batterie"]) < SEUIL_BATTERIE:
        alertes.append('batterie too low')

    set_data("alerte", alertes, ip, port)
