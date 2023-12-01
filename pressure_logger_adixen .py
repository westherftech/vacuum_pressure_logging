# -*- coding: utf-8 -*-
"""
Created on 14 Nov 2023
In the vacuum station located in Klerefontein, there is a Pfeiffer TPG 261 Single Gauge that has a
PKR 251, FPM sealed, DN 40 CF-F vacuum sensor attached

This is a script to:
    - capture the pressure reading from the TPG 261 Single Gauge
    - 




@author: Wesley Newton
"""

# Import functions dependancies
import matplotlib.pyplot as plt
# import matplotlib.animation as animation

#from pylablib.devices import Pfeiffer # The 
import serial
import time
from datetime import date
from datetime import datetime
import os
#import msvcrt  #kbhit()
#import matplotlib.animation as animation
#import datetime # ReadTemperatureStoreFile()
#import numpy as np # ReadTemperatureStoreFile() real time plot

#import warnings

# def fxn():
#     warnings.warn("deprecated", DeprecationWarning)

# with warnings.catch_warnings():
#     warnings.simplefilter("ignore")
#     fxn()


#%%

# Set up Global constants and variable definitions

dut = 'Vacuum Manifold' # description of the device under test
meas = 'Functional Test Adixen' # description of the measurement to use as a file name


measurement_directory ='measurements' # location to save the raw measurement data 
result_directory ='results' # location to save graphs and other processed results

com_port = 'COM6' # the serial port that the gauge is connected to

#%%

# Declare functions that do the work


#%% This function is not used - it is done in the main script

# def read_from_gauge_pfeiffer(com_port,baud):
#     '''
#     A function that reads the pressure data from the Pfeiffer SingleGauge. 
#     It assumes that there is only one sensor connected.  

#     Parameters
#     ----------
#     serial_port : string
#         In the format 'COM1'.
#     baud : int
#         Specify the baud rate for serial comms.

#     Returns
#     -------
#     An array containing, float: The Guage status and float: pressure reading in mb.

#     '''
#     try:
#         # Set up and open the serial port
#         gauge_com=serial.Serial(port=com_port,
#                                 baudrate=baud,
#                                 bytesize=8,
#                                 parity='N',
#                                 stopbits=1,
#                                 timeout=1,
#                                 xonxoff=0,
#                                 rtscts=0)
        
#         gauge_com.flushInput()  # flush the input buffer
#         gauge_com.flushOutput() # flush the output buffer

    
    
    
#         response = (gauge_com.readline().decode().strip()) # received the pressure values from the serial port
#         pressure = [float(item.strip()) for item in response.split(',')]    # convert the string into an array of floating point number  
#         gauge_com.close() # remember to always close the serial port

#         return pressure #only need the first two values for a single   

#     except KeyboardInterrupt:   # If the keyboard halts 
#         gauge_com.close()
#         print('keyboard interrupt')
#         return [0, 0] # returns the sensor default value with status sensor disconnected

#     except:                                         # Close the serial port on any exception
#         gauge_com.close()
#         print('exception, check connection to gauge')
#         return [0, 0] # returns the sensor default value with status sensor disconnected
       
    
#%%    Read from other sensor - Not used
    
    

# def read_from_gauge2(serial_port,baud):
#     '''
#     A function to read from the ACS2000 pressure gauage attached to the SAAO vacuum station
    
#     Parameters
#     -------
#     serial_port : com port to open in the format 'COM4'

#     Returns
#     -------
#     None.

#     '''
   
#     try:
        
#         print('\nDisplay continuous Pressure reading [mB]')
#         # ACS2000 vacuum gauge
        
#         noww=time.time()

            
#         with open('Pressure.txt','a') as in_file:  # create a new file to save the pressure data. If file exists do not overwrite
#             #in_file.write("start time: {}".format(noww))
#             print("Open file: .\Pressure.txt")
#             plt.ion()
#             fig=plt.figure()

#             # i=0
#             x=list()
#             y=list()
            
#     # temp_y=np.random.random();
#     # x.append(i);
#     # y.append(temp_y);


            
            
            
#             while not msvcrt.kbhit():
            
#                 acs.write(b"$PRD\r")
#                 pres=acs.readlines()
#                 val=pres[0].decode()
#                 cur_time=time.time()-noww
#                 print("time:{} Pres [mB]:{}".format(float(cur_time),float(val[-9:])))
#                 #in_file.write("time [s],{},Pres [mB],{},\n".format(cur_time,float(val[-9:])))
#                 in_file.write('{},{},{}\n'.format(float(cur_time), datetime.datetime.now(), float(val[-9:])))

#                 # plt.scatter(cur_time, float(val[-9:]),marker='+', color='#FF8C00')
                
#                 x.append(cur_time)
#                 y.append(float(val[-9:]))
#                 plt.scatter(x,y);
#                 plt.yscale("log")
#                 # plt.pause(step_time)
#                 # plt.show()
#                 plt.minorticks_on()
#                 # plt.axis([0,1000,0,1])
#                 plt.grid(True)
#                 plt.xlabel('Time (s) since test start')
#                 plt.ylabel('Pressure (mb)')
#                 plt.show()
                
#                 # plt.pause(0.05)
#                 time.sleep(0.5)
               
           
#                 acs.close()
#     except KeyboardInterrupt:                       # If the keyboard halts then close the serial port
#                 acs.close()
#     except:                                         # Close the serial port on any exception
#                 acs.close()
#                 print('exception')










    

#%% Main code

if __name__ == "__main__":
    
#%  Initialise and create log files

    # open the log file. If one exists with the current name, then a new one is created
    test_number = 1
    log_file_name = ''+measurement_directory+'\\'+dut+' '+meas+' %i'%(test_number)
    while os.path.exists(log_file_name+'.txt'): # check to see if the log file already exists
        test_number += 1
        log_file_name = ''+measurement_directory+'\\'+dut+' '+meas+' %i'%(test_number)
        
    with open(log_file_name+'.txt', 'w') as log_file: # open the file with write privelages
        log_file.write('Data captured from the '+dut+' '+meas+'\n')
        log_file.write('Start date and time:'+(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        log_file.write('\n Time since start of test (s) \t Presure (mb)\n') # set up header
        
    with open(log_file_name+' error log.txt', 'w') as error_log_file: # open the file with write privelages
       error_log_file.write('The error log for data captured from the '+dut+' '+meas+'\n')
       error_log_file.write('Start date and time:'+(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
       error_log_file.write('\n Time since start of test (s) \t Error\n') # set up header

#%  Create variables for use in main loop
    pressure_values = []
    time_values = []
    test_start_time = datetime.now() # this is the test start time
    test_start_time2 = time.time()

#% Set up the live plot
    plt.ion() # turn on interactive plot
    fig=plt.figure()

# initialise the serial port
    gauge_com=serial.Serial(port=com_port,  # Opening the serial port once seems to be more stable
                            baudrate=9600,
                            bytesize=8,
                            parity='N',
                            stopbits=1,
                            timeout=1,
                            xonxoff=0,
                            rtscts=0)
    
    gauge_com.flushInput()  # flush the input buffer
    gauge_com.flushOutput() # flush the output buffer


#%    Main loop to capture pressure reading, update plot, and save data to log file

    while True: # main loop starts
          
        try:

# capture at least two pressure readings to be able to plot a line graph
                if (len(pressure_values)>>3): ## will only run if the length of the pressure values array is less than 3
                    # get current time
                    current_time = time.time()-test_start_time2
                    # capture pressure reading
                    gauge_com.flushInput()  # flush the input buffer to onlu record the most recent measurement
                    gauge_com.write(b"$PRD\r")
                    time.sleep(1)
                    response = (gauge_com.readline().decode().strip()) # received the pressure values from the serial port
                    pressure_txt = response.split(',')
                    pressure = float(pressure_txt[1])   # convert the string into an array of floating point number  
                    # gauge_com.close() # remember to always close the serial port
                    print('Time since test start (s): %0.1f \t Measured pressure: %.3e'%(current_time, pressure))
                    # Add the data to the plot
                    pressure_values.append(pressure) # pressure values for use in the plot
                    time_values.append(current_time) # time value array for use in the plot
                    with open(log_file_name+'.txt', 'a') as log_file:
                        log_file.write('%0.1f \t %e \n' %((current_time, pressure)))
           

                #enough values are present, now we can start plotting the graph
                # get current time
                current_time = time.time()-test_start_time2
                # capture pressure reading
                # capture pressure reading
                gauge_com.flushInput()  # flush the input buffer to only record the most recent measurement
                gauge_com.write(b"$PRD\r")
                time.sleep(1)
                response = (gauge_com.readline().decode().strip()) # received the pressure values from the serial port
                pressure_txt = response.split(',')
                pressure = float(pressure_txt[1])
                # gauge_com.close() # remember to always close the serial port

                

                # Check gauge status
                '''Transmit: PRX <CR>[<LF>]
                Receive: <ACK><CR><LF>
                Transmit: <ENQ>
                Receive: x,sx.xxxxEsxx,y,sy.yyyyEsyy <CR><LF>
                · ·· ·
                · ·· º Measurement
                · ·· value gauge 2 1)
                · ·· [in current
                · ·· pressure unit]
                · · º¶ Status gauge 2
                · º¶ Measurement value gauge 1 1)
                · [in current pressure unit]
                ·
                º¶ Status gauge 1, x =
                0 –> Measurement data okay
                1 –> Underrange
                2 –> Overrange
                3 –> Sensor error
                4 –> Sensor off (IKR, PKR, IMR, PBR)
                5 –> No sensor
                (output: 5,2.0000E-2 [mbar])
                6 –> Identification error'''
#                sensor_status = "none"
#                
#                if (pressure[0] == 0.0): 
#                    sensor_status = "Good"
#                    
#                if (pressure[0] == 1.0): 
#                    sensor_status = "Underrange"
#                   
#                if (pressure[0] == 2.0): 
#                    sensor_status = "Overrange"
#                 
#                if (pressure[0] == 3.0): 
#                    sensor_status = "Sensor error"
# 
#                if (pressure[0] == 4.0): 
#                    sensor_status = "Sensor off"
#                    
#                if (pressure[0] == 5.0): 
#                    sensor_status = "No sensor attached"
#                    
#                if (sensor_status == "none"):
#                    raise IndexError('r')
                
                print('Time since test start (s): %0.1f \t Measured pressure: %.3e'%(current_time, pressure))
                # Add the data to the plot
                
                
                # check validity of the pressure value 
                
                
                pressure_values.append(pressure) # pressure values for use in the plot. If no value was returned from the serial port, then this will cause an exception
                time_values.append(current_time) # time value array for use in the plot


                plt.clf()   # clear the plot to prevent filling up the memory with many plots
                plt.plot(time_values, pressure_values, label='Pressure (mb)', color="blue", linewidth=1)#, marker='x', )
                plt.minorticks_on()
                plt.grid(True)
                plt.yscale("log")
                plt.xlabel('Time since test start (s)')
                plt.ylabel('Pressure (mb)')
                plt.title('Vacuum Gauge Pressure %s %s' %(dut, meas))
                plt.savefig(log_file_name+'.png', dpi=400 ) 
                # redraw the plot
   #         plt.draw()
                plt.pause(0.001) 
                    
                plt.gcf() # get current figure

            
                # save data to the log file
                with open(log_file_name+'.txt', 'a') as log_file:
                    log_file.write('%0.1f \t %e \n' %(current_time, pressure))
         #   file.close()  # close the file again. Apparently this is not necessary when the with open it used
                # Writing 
            # wait 10 ms
                time.sleep(0.001)
                # plt.clf()   # clear the plot to prevent filling up the memory with many plots
                # plt.close()




     
        except KeyboardInterrupt:   # If the keyboard halts 
            print('keyboard interrupt')
            gauge_com.close() # remember to always close the serial port
            with open(log_file_name+' error log.txt', 'a') as error_log_file:
                error_log_file.write('%0.1f \t keyboard interrupt ended the test \n' %((current_time)))
            break
        except:                                         # On any other exception, restart the loop
            print('An exception occured. Discarded the last sample and restarting the measurement loop')
            with open(log_file_name+' error log.txt', 'a') as error_log_file:
                error_log_file.write('%0.1f \t An exception occured possibly due to corrupt serial data or disconnection of serial port. Discarded last sample and continue the measurement loop \n' %((current_time)))
            continue # try to go back into the main loop again

            
        

            
