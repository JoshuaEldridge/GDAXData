#!/usr/bin/python
'''
Velocity Calculation

		Xf - Xi
V = -------
		Tf - Ti
		

		Change in Value
V = ---------------
		Change in Time	
'''		

import datetime
#import omniture
import random
import time
import gdax

previous_time = None
previous_value = None

def run_report():
	return random.randint(0,100)


def calculate_velocity(current_time, current_value, previous_time, previous_value):
	if previous_time is None and previous_value is None:
		return 0
	else:
		metric_delta = current_value - previous_value
		time_delta = current_time - previous_time
		time_delta = time_delta.total_seconds()
		#print current_value, previous_value
		#print current_time, previous_time
		#print "Time Delta: " + str(time_delta)
		#print "Metric Delta: " + str(metric_delta)
		velocity = metric_delta / time_delta
		return velocity


while True:
	''' Run Code'''
	current_time = datetime.datetime.now()
	#current_value = run_report()
	public_client = gdax.PublicClient()
	btc = public_client.get_product_order_book('BTC-USD', level=1)
	current_value = float(btc['asks'][0][0])
	print "Current Value: " + str(current_value)
	print "Velocity: " + str(calculate_velocity(current_time, current_value, previous_time, previous_value))
	
	previous_time = current_time
	previous_value = current_value
	
	time.sleep(.15)
