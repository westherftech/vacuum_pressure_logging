# pressure_logging
Two scripts for logging pressure from the Adixen and Pffeifer vacuum gauges
Both are connected 
the Device under test (DUT) and Measurement purpose (measurement) is specified for each test at the start of the python script.
The strings entered into DUT and measurement are used to name the log files and graph title.
The following files are generated:
  - A log file saves the measured pressure values and time stamps
  - An error log saves any other exceptions including disconnections and test interrupted by keyboard
  - A PNG graph is also generated 

The script is intended to run in Spyder in the Anaconda 3 environment

The module pyserial is required.

Hardware required:
A serial to USB converter is recommended to connect to the Gauge
Both gauges are set to a BAUD rate of 9600 
The Pffeifer single gauge requires a crossover cable (TX on one end connects to RX on the other end) 
