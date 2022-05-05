import json

from transactions.models import MarketTransaction, LimitTransaction


def update_transactions(ws, message):
    data = json.loads(message)
    btc_price = float(data['p'])

    market_transactions = MarketTransaction.objects.all()

    for trx in market_transactions:
        trx.execute(btc_price)
        trx.delete()







