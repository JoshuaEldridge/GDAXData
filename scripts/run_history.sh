#
#!/bin/bash

start=`date +"%Y-%m-%d" -d "01/01/2018"`
end=`date +"%Y-%m-%d" -d "03/31/2018"`

while [ "$start" != "$end" ] ; 
do 
        start=`date +"%Y-%m-%d" -d "$now + 1 day"`; 
	python get_btc_history_csv.py $start
done
