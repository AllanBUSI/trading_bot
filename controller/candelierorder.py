


import time
from controller.priceOrder import priceOrder
from service.xtb import XTB
from utils.json_custom import read_json


def candelier_order(array, bougie, currency):
    for i, v in enumerate(array):
        chemin_du_fichier = 'data/config.json'
        data_config = read_json(chemin_du_fichier)
        API = XTB(data_config['compte'], data_config["password"])
        time.sleep(1)
        a, tp, sl = priceOrder(API, v, bougie, currency)
        order = a
        API.disconnect()
    return order, tp, sl