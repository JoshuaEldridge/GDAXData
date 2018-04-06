#!/usr/bin/python

# currencies = client.get_currencies()
# products = client.get_products()

# order_book = public_client.get_product_order_book('BTC-USD', level=1)
# 
# print "ORDER BOOK:"
# print order_book
# 
# product_ticker = public_client.get_product_ticker(product_id='ETH-USD')
# 
# print "PRODUCT TICKER:"
# print product_ticker
# 
# product_trades = public_client.get_product_trades(product_id='ETH-USD')
# 
# print "PRODUCT TRADES:"
# print product_trades

from datetime import datetime, timedelta
from time import sleep
import gdax
import gzip
import json

start_date = datetime.strptime('2018-04-01T00:00:00', '%Y-%m-%dT%H:%M:%S')
file_date = start_date.date().strftime('%Y%m%d')
# This is the interim dates we will use to get to the end_date
incremental_date = start_date + timedelta(hours=1)
# This is the actual end date
end_date = datetime.strptime('2018-04-02T00:00:00', '%Y-%m-%dT%H:%M:%S')

def convert_timestamp(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')

client = gdax.PublicClient()

products = ['LTC-USD', 'ETH-USD', 'BTC-USD', 'BCH-USD']

rates_header = ['product', 'time', 'low', 'high', 'open', 'close', 'volume']

def get_rates_dict(product, s, e):
    historic_rates_data = []
    historic_rates = client.get_product_historic_rates(product, granularity=60, start=s.strftime('%Y-%m-%dT%H:%M:%S'), end=e.strftime('%Y-%m-%dT%H:%M:%S'))
    for i in historic_rates:
        try:
            i.insert(0, product)
        except:
            raise RuntimeError("Product is: " + product + " and i was: " + i)
        historic_rates_data.append(dict(zip(rates_header, i)))
    return historic_rates_data

json_rates = []

while incremental_date <= end_date:
    for product in products:
        print product, start_date, incremental_date, end_date
        json_rates.append(get_rates_dict(product, start_date, incremental_date))
    start_date = incremental_date
    incremental_date = start_date + timedelta(hours=1)
    sleep(1)

with gzip.open(str(file_date) + '-gdax-historic-rates.json.gz', mode='wb') as f:
    f.write(json.dumps(json_rates, separators=(',', ': '), ensure_ascii=False))