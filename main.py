from controller.priceOrder import priceOrder
from controller.tplsgenerator import calculate_tp_sl
from service.xtb import XTB
from utils.duplicate import count_duplicates
from utils.json_custom import read_json
import schedule


def main():
    
    chemin_du_fichier = 'data/config.json'

    data_config = read_json(chemin_du_fichier)

    API = XTB(data_config['compte'], data_config["password"])
    
    wallet = API.get_Balance()    
    for items, value in enumerate(data_config["crypto"]):
        symbol = API.get_Symbol(value['name'])
        print(symbol)
    
    a, tp, sl = priceOrder(API, "MN1", 52)
        
    has_duplicates, duplicates = count_duplicates(a)
    
    print(a)

    API = XTB(data_config['compte'], data_config["password"])
    
    if duplicates.get('vente'):
        if duplicates['vente'] >= 1:
            return

    if duplicates.get('achat'):
        if duplicates['achat'] >= 2:
            prixStopLoss = int(symbol['ask'] + sl)
            prixTakeProfit = int(symbol['ask'] + tp)
            list = API.make_Trade(symbol="ETHEREUM", cmd=0,transaction_type=0,volume=0.1,comment="entrer ethereum ",order=0, sl=prixStopLoss, tp=prixTakeProfit)
    

if __name__ == "__main__":    
    schedule.every(1).minutes.do(main)
    print("Goooo")
    main()
    while True:
        schedule.run_pending()


