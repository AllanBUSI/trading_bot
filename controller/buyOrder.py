
from utils.json_custom import read_json


def BuyOrder(API, order, sl, tp, currency):
    
    chemin_du_fichier = 'data/config.json'
    data_config = read_json(chemin_du_fichier)
    
    symbol = API.get_Symbol(currency)
        
    print(order)
    
    if order == 'neutre':
        return
    
    if order == 'vente':
        print('Vente')
        prixStopLoss = int(symbol['ask'] + sl)
        prixTakeProfit = int(symbol['ask'] + tp)
        list = API.make_Trade(symbol=currency, cmd=1,transaction_type=0,volume=0.1,comment="entrer "+currency,order=0, sl=prixStopLoss, tp=prixTakeProfit)
        return

    if order == 'achat':
        print("Achat")
        prixStopLoss = int(symbol['ask'] + sl)
        prixTakeProfit = int(symbol['ask'] + tp)
        list = API.make_Trade(symbol=currency, cmd=0,transaction_type=0,volume=0.1,comment="entrer "+currency,order=0, sl=prixStopLoss, tp=prixTakeProfit)
        return