# Coxisrobbingme
A python application that I made to calculate how much my ISP is overcharging me 
***NOTE The speed_test script requires speedtest-cli to run***

-Hardware
The device I am currently using is a Jetson Nano 2GB plugged with an ethernet connection, however, any linux device can run the speed_test script

"speed_test" is a bash script that is run on the device that is collecting the speed data.

Intitially, I had planned to run a speed test every 5 minutes, but due to constraints, I had to adjust my speed tests to every 20 minutes. 
coxrobbingme.py is set to run every 20 minutes to update the output files. 
cost_dict.py and static/speeds.png will be created on initial run and overwritten on subsequent runs of coxrobbingme.py

app.py runs the Flask site to display the data
