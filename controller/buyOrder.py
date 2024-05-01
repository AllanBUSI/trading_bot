
from utils.json_custom import read_json


def BuyOrder(API, duplicates, sl, tp, candle, currency):
    
    chemin_du_fichier = 'data/config.json'
    data_config = read_json(chemin_du_fichier)
    
    symbol = API.get_Symbol(currency)
        
    print(duplicates)
    
    if duplicates.get('neutre'):
        if duplicates['neutre'] >= 19:
            return
    
    if duplicates.get('vente') and candle == 'vente':
        print("vente")
        if duplicates['vente'] >= 5 and duplicates['neutre'] >= 10:
            prixStopLoss = int(symbol['ask'] + sl/2)
            prixTakeProfit = int(symbol['ask'] + tp/2)
            list = API.make_Trade(symbol=currency, cmd=1,transaction_type=0,volume=0.1,comment="entrer "+currency,order=0, sl=prixStopLoss, tp=prixTakeProfit)
            return

    if duplicates.get('achat') and candle == 'achat':
        print("Achat")
        if duplicates['achat'] >= 5 and duplicates['neutre'] >= 10:
            prixStopLoss = int(symbol['ask'] + sl/2)
            prixTakeProfit = int(symbol['ask'] + tp/2)
            list = API.make_Trade(symbol=currency, cmd=0,transaction_type=0,volume=0.1,comment="entrer "+currency,order=0, sl=prixStopLoss, tp=prixTakeProfit)
            return