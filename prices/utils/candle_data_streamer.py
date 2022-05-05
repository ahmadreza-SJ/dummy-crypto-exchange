import websocket
import threading
import signal

from celery import shared_task
from .update_transactions import update_transactions

WEBSOCKET_URL = "wss://stream.binance.com:9443/ws/{pair}@trade"


@shared_task()
def get_price_candle_data(on_message, pair, timestamp):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(WEBSOCKET_URL.format(pair=pair, timestamp=timestamp), on_open=lambda webs: print("Connection Openned"),
                                on_close=lambda webs: print("Connection Closed!"), on_message=on_message)

    x = threading.Thread(target=ws.run_forever)
    x.start()

