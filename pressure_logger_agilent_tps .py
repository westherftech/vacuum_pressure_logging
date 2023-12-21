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

com_port = 'COM11' # the serial port that the gauge is connected to

    

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
                    gauge_com.write(b'\x02') #ASCII STX is 0x2 in hex       
                    gauge_com.write(b'\x80') #Address of the TPS in hex 
                    gauge_com.write(b'\x32') #Window character 1  
                    gauge_com.write(b'\x32') #Window character 2
                    gauge_com.write(b'\x34') #Window character 3 
                    gauge_com.write(b'\x30') #Character denoted read from device
                    gauge_com.write(b'\x03') #ASCII ETX is 0x3 in hex
                    gauge_com.write(b'\x38') #CRC ASCII 8 is 0x38 in hex
                    gauge_com.write(b'\x37') #CRC ASCII 7 is 0x37 in hex
                    # time.sleep(1)
                    
                    response = gauge_com.readline()
                    check_e = response[9] # this is a very simple check to see that the E is in the right place
                    
                    if (check_e != 69):
                        raise IndexError('r') # this can be refined. An exception is raised if E is not in the correct location in the recieved data
                    
                    
                    pressure_txt = response[5:-3].decode() # changes the bytestring into a string and discard the rest
                    pressure = float(pressure_txt)   # convert the string into an array of floating point number  
                    
                    
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
                gauge_com.write(b'\x02') #ASCII STX is 0x2 in hex       
                gauge_com.write(b'\x80') #Address of the TPS in hex 
                gauge_com.write(b'\x32') #Window character 1  
                gauge_com.write(b'\x32') #Window character 2
                gauge_com.write(b'\x34') #Window character 3 
                gauge_com.write(b'\x30') #Character denoted read from device
                gauge_com.write(b'\x03') #ASCII ETX is 0x3 in hex
                gauge_com.write(b'\x38') #CRC ASCII 8 is 0x38 in hex
                gauge_com.write(b'\x37') #CRC ASCII 7 is 0x37 in hex
                # time.sleep(1)
                 
                response = gauge_com.readline()
                check_e = response[9] # this is a very simple check to see that the E is in the right place
                 
                if (check_e != 69):
                    raise IndexError('r') # this can be refined. An exception is raised if E is not in the correct location in the recieved data
             
                pressure_txt = response[5:-3].decode() # changes the bytestring into a string and discard the rest
                pressure = float(pressure_txt)   # convert the string into an array of floating point number  

                print('Time since test start (s): %0.1f \t Measured pressure: %.3e'%(current_time, pressure))
                # Add the data to the plot
                
               
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

            
        

            
