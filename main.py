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
        "BITCOIN", "ETHEREUM", "SOLANA",
    ]
    for v in currency:    
        
        
        try:
            chemin_du_fichier = 'data/config.json'
            data_config = read_json(chemin_du_fichier)
            API = XTB(data_config['compte'], data_config["password"])
            order = []
            order, tp, sl, candle = candelier_order(["M30", "H1", "H4", "D1", "MN1"], order, v)
            print("Take Profit:", tp/2, "Stop Loss:", sl/2)
            has_duplicates, duplicates = count_duplicates(order)
            API = XTB(data_config['compte'], data_config["password"])
            BuyOrder(API, duplicates, sl, tp, candle, v)
        except:
            print('Suivant')
        
    

if __name__ == "__main__":    
    schedule.every(30).minutes.do(main)
    print("Goooo")
    main()
    while True:
        schedule.run_pending()


