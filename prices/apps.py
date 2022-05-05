import sys
import os

from django.apps import AppConfig


class PricesConfig(AppConfig):
    if os.environ.get('RUN_MAIN') == 'true':
        default_app_config ='django.db.models.BigAutoField'

        def ready(self):
            from .utils.update_transactions import update_transactions
            from .utils.candle_data_streamer import get_price_candle_data
            if 'runserver' in sys.argv:
                get_price_candle_data(update_transactions, 'btcusdt', '5m')

    name = 'prices'


