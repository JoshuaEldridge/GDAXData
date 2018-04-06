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
import csv
import sys

def valid_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    return True

if valid_date(sys.argv[1]):
    start_date = datetime.strptime(sys.argv[1], '%Y-%m-%d')
else:
    print "This script requires a start date as the first argument in the format YYYY-MM-DD"

# This script will run for a daily window pulling per-minute
# history on the listed products.

end_date = start_date + timedelta(days=1)

print "Running from: " + str(start_date) + " to " + str(end_date)

file_date = start_date.date().strftime('%Y%m%d')
incremental_date = start_date + timedelta(hours=1)

def convert_timestamp(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')

client = gdax.PublicClient()

products = ['LTC-USD', 'ETH-USD', 'BTC-USD', 'BCH-USD']
rates_header = ['product', 'time', 'low', 'high', 'open', 'close', 'volume']
with open(str(file_date) + '-gdax-historic-rates.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(rates_header)

def get_rates(product, s, e):
    historic_rates_data = client.get_product_historic_rates(product, granularity=60, start=s.strftime('%Y-%m-%dT%H:%M:%S'), end=e.strftime('%Y-%m-%dT%H:%M:%S'))
    return historic_rates_data

while incremental_date <= end_date:
    for product in products:
        print product, start_date, incremental_date, end_date
        csv_rates = get_rates(product, start_date, incremental_date)
        with open(str(file_date) + '-gdax-historic-rates.csv', 'a') as f:
            writer = csv.writer(f)
            for rate in csv_rates:
                rate.insert(0, product)
                writer.writerow(rate)
    start_date = incremental_date
    incremental_date = start_date + timedelta(hours=1)
    sleep(1)

# with open(str(file_date) + '-gdax-historic-rates.csv') as f_in, gzip.open(str(file_date) + '-gdax-historic-rates.csv.gz', 'wb') as f_out:
#     f_out.writelines(f_in)
