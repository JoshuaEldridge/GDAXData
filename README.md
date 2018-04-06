# GDAXData
This repository is a small collection of scripts I used to collect historical data from
Coinbase on minute-by-minute prices for the primary crypto-currencies listed on the GDAX.
I've also included the initial scrape data so others won't have to hit the API just to 
get some data to test with.

This script requires the excellent library by Dan Paquin: https://github.com/danpaquin/gdax-python

The method I used for invoking the script is a simple bash file (included) that simply
loops over dates between a given start and end date.
