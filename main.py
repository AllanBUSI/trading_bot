import time
import numpy as np
import pandas as pd
from controller.buyOrder import BuyOrder
from controller.candelierorder import candelier_order
from controller.priceOrder import priceOrderCandelier
from controller.tplsgenerator import calculate_tp_sl
from controller.zoneSupport import trading_decision
from function.candelier_detector import detect_candlestick
from service.xtb import XTB
from utils.duplicate import count_duplicates
from utils.json_custom import json_to_pd, read_json
import schedule

from utils.window import estimate_window_size



def main():
    
    currency = [
        "ETHEREUM"
    ]
    
    for v in currency:  
        # try:
            chemin_du_fichier = 'data/config.json'
            data_config = read_json(chemin_du_fichier)          
            
            API = XTB(data_config['compte'], data_config["password"])
            order, tp, sl = candelier_order(["M30"], 30, v)
            print("Take Profit:", tp, "Stop Loss:", sl)
            API = XTB(data_config['compte'], data_config["password"])
            BuyOrder(API, order, sl, tp, v)
            
            API = XTB(data_config['compte'], data_config["password"])
            order, tp, sl = candelier_order(["H4"], 30*8, v)
            print("Take Profit:", tp, "Stop Loss:", sl)
            API = XTB(data_config['compte'], data_config["password"])
            BuyOrder(API, order, sl, tp, v)
            
            API = XTB(data_config['compte'], data_config["password"])
            order, tp, sl = candelier_order(["D1"], 30*48, v)
            print("Take Profit:", tp, "Stop Loss:", sl)
            API = XTB(data_config['compte'], data_config["password"])
            BuyOrder(API, order, sl, tp, v)
            
            API = XTB(data_config['compte'], data_config["password"])
            candles = API.get_Candles(period="D1",symbol=v, qty_candles=60*24)
            filtered_data = [item for item in candles if "digits" not in item]
            data = json_to_pd(filtered_data)
            tp, sl = calculate_tp_sl(data)
            window = estimate_window_size()
            order = trading_decision(data['close'], window)
            API = XTB(data_config['compte'], data_config["password"])
            BuyOrder(API, order, sl, tp, v)

        # except Exception as e:
        #     print("d",e)
            
            

def candle():
    print("candle")
    chemin_du_fichier = 'data/config.json'
    data_config = read_json(chemin_du_fichier)    
    API = XTB(data_config['compte'], data_config["password"])
    order, tp, sl = priceOrderCandelier(API, "D1", 24, "ETHEREUM")
    print("Take Profit:", tp, "Stop Loss:", sl)
    API = XTB(data_config['compte'], data_config["password"])
    BuyOrder(API, order, sl, tp, "ETHEREUM")
            

if __name__ == "__main__":    
    schedule.every(10).minutes.do(main)
    schedule.every(20).minutes.do(candle)
    print("Goooo")
    main()
    while True:
        schedule.run_pending()


