import time
import numpy as np
import pandas as pd
from controller.buyOrder import BuyOrder
from controller.candelierorder import candelier_order
from controller.priceOrder import priceOrder
from controller.tplsgenerator import calculate_tp_sl
from function.candelier_detector import detect_candlestick
from service.xtb import XTB
from utils.duplicate import count_duplicates
from utils.json_custom import read_json
import schedule



def main():
    
    currency = [
        "ETHEREUM"
    ]
    for v in currency:  
        try:
            chemin_du_fichier = 'data/config.json'
            data_config = read_json(chemin_du_fichier)          
            
            API = XTB(data_config['compte'], data_config["password"])
            order, tp, sl = candelier_order(["M30"], 30, v)
            print("Take Profit:", tp/2, "Stop Loss:", sl/2)
            API = XTB(data_config['compte'], data_config["password"])
            BuyOrder(API, order, sl, tp, v)
            
            API = XTB(data_config['compte'], data_config["password"])
            order, tp, sl = candelier_order(["H4"], 30*8, v)
            print("Take Profit:", tp/2, "Stop Loss:", sl/2)
            API = XTB(data_config['compte'], data_config["password"])
            BuyOrder(API, order, sl, tp, v)
        except Exception as e:
            print(e)
            
            
    

if __name__ == "__main__":    
    schedule.every(1).minutes.do(main)
    print("Goooo")
    main()
    while True:
        schedule.run_pending()


