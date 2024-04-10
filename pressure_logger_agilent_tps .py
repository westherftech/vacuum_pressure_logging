# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 10:01:53 2024

@author: wnewton
"""

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
# import matplotlib.pyplot as plt
import matplotlib
# import matplotlib.animation as animation
# from matplotlib.animation import FuncAnimation
#from pylablib.devices import Pfeiffer # The 
import serial
import time
from datetime import date
from datetime import datetime
import os
import keyboard
#import msvcrt  #kbhit()
#import matplotlib.animation as animation
#import datetime # ReadTemperatureStoreFile()
import numpy as np # ReadTemperatureStoreFile() real time plot

#import warnings

# def fxn():
#     warnings.warn("deprecated", DeprecationWarning)

# with warnings.catch_warnings():
#     warnings.simplefilter("ignore")
#     fxn()


#%%

# Set up Global constants and variable definitions
# name = input("Enter a suitable graph title. Include the intended goal of the measurement: ")
# measurement = input("Enter a suitable sub-title. Include a description, location and condition of the system under test to give context to the data: ")

dut = 'Tee and sensor' # description of the device under test
meas = 'After cleaning purge valve' # description of the measurement to use as a file name


measurement_directory ='measurements' # location to save the raw measurement data 
result_directory ='results' # location to save graphs and other processed results

com_port = 'COM3' # the serial port that the gauge is connected to

def makepacket(ADDR,WIN,COM):
    '''
    A function to generate the Hex packet required for reading from the Agilent TPS vacuum station

    Parameters
    ----------
    ADDR : HEX bytestring
        <ADDR> (Unit address) = 0x80 (for RS 232) or = 0x80 + device number (0 to 31)(for RS 485)
    WIN : HEX bytestring
        <WIN> (Window) = a string of 3 numeric character indicating the window number (from ‘000’ to ‘999’); 
        for the meaning of each window see the relevant paragraph in the TPS manual
    COM : HEX bytestring
        <COM> (Command) = 0x30 to read the window, 0x31 to write into the window

    Returns
    -------
    packet : Hex Bytestring
        The MESSAGE is a string with the following format: <STX>+<ADDR>+<WIN>+<COM>+<DATA>+<ETX>+<CRC>

    '''
    
    STX = b'\x02' # <STX> (Start of transmission) = 0x02
    
     # read from device
    ETX = b'\x03' # <ETX> (End of transmission) = 0x03
    #DATA = '' # <DATA> = an alphanumeric ASCII string with the data to be written into the window. In case of a reading command this field is not present.

    payload = ADDR + WIN + COM
    payload += ETX

    CRC = payload[0]
    for b in payload[1:]:
        CRC ^= b
    CRC = hex(CRC)[2:].upper().zfill(2).encode()

    packet = STX + payload + CRC

    return packet

def makepacketWrite(ADDR,WIN,COM,DATA):
    '''
    A function to generate the Hex packet required for reading from the Agilent TPS vacuum station

    Parameters
    ----------
    ADDR : HEX bytestring
        <ADDR> (Unit address) = 0x80 (for RS 232) or = 0x80 + device number (0 to 31)(for RS 485)
    WIN : HEX bytestring
        <WIN> (Window) = a string of 3 numeric character indicating the window number (from ‘000’ to ‘999’); 
        for the meaning of each window see the relevant paragraph in the TPS manual
    COM : HEX bytestring
        <COM> (Command) = 0x30 to read the window, 0x31 to write into the window

    Returns
    -------
    packet : Hex Bytestring
        The MESSAGE is a string with the following format: <STX>+<ADDR>+<WIN>+<COM>+<DATA>+<ETX>+<CRC>

    '''
    
    STX = b'\x02' # <STX> (Start of transmission) = 0x02
    
     # read from device
    ETX = b'\x03' # <ETX> (End of transmission) = 0x03
    #DATA = '' # <DATA> = an alphanumeric ASCII string with the data to be written into the window. In case of a reading command this field is not present.

    payload = ADDR + WIN + COM + DATA
    payload += ETX

    CRC = payload[0]
    for b in payload[1:]:
        CRC ^= b
    CRC = hex(CRC)[2:].upper().zfill(2).encode()

    packet = STX + payload + CRC

    return packet


def crc_check(message):
    '''
    Generates the CRC check from a received message

    Parameters
    ----------
    message : TYPE
        This is the complete message received from the Vacuum pump including the CRC

    Returns
    -------
    CRC : bytestring of length 2
        The CRC 

    '''
    payload = message[1:-2] # remove the CRC and STX byte from the message
    CRC = payload[0]
    for b in payload[1:]:
        CRC ^= b
    CRC = hex(CRC)[2:].upper().zfill(2).encode()
    
    return CRC

def getPressure():
    
    gauge_com=serial.Serial(port=com_port,  # Opening the serial port once seems to be more stable
                            baudrate=9600,
                            bytesize=8,
                            parity='N',
                            stopbits=1,
                            timeout=1,
                            xonxoff=0,
                            rtscts=0)
    try:
        message = makepacket(ADDR = b'\x80',WIN = b'224',COM = b'\x30') #
    
        
    
        gauge_com.flushInput()  # flush the input buffer
        gauge_com.flushOutput() # flush the output buffer
    
        gauge_com.write(message)
        response = gauge_com.readline()
        gauge_com.close()
    
        pressure = response[5:-3].decode()


                    # response = gauge_com.readline()
                    # check_e = response[9] # this is a very simple check to see that the E is in the right place
                    
                    # if (check_e != 69):
                    #     raise IndexError('r') # this can be refined. An exception is raised if E is not in the correct location in the recieved data
                    
                    
                    # pressure_txt = response[5:-3].decode() # changes the bytestring into a string and discard the rest
                    # pressure = float(pressure_txt)   # convert the string into an array of floating point number  


        return float(pressure)
    except:
        gauge_com.close() # remember to always close the serial port
        return 


def getPumpCurrent():
    '''
    

    Raises
    ------
    IndexError
        DESCRIPTION.

    Returns
    -------
    current : TYPE
        DESCRIPTION.

    '''
    gauge_com=serial.Serial(port=com_port,  # Opening the serial port once seems to be more stable
                            baudrate=9600,
                            bytesize=8,
                            parity='N',
                            stopbits=1,
                            timeout=1,
                            xonxoff=0,
                            rtscts=0)
    
    try: 
        
        message = makepacket(ADDR = b'\x80',WIN = b'200',COM = b'\x30') #
    

        
        gauge_com.flushInput()  # flush the input buffer
        gauge_com.flushOutput() # flush the output buffer
        
        gauge_com.write(message)
        response = gauge_com.readline()
        gauge_com.close()
    
        current = response[5:-3].decode()
        crc_1 = response[-2:] # this is a very simple check to see that the E is in the right place
        if (crc_1 != crc_check(response)):
            raise IndexError('r') # this can be refined. An exception is raised if the received CRC is not equal to the calculated CRC
        return float(current) # return the turbopump current in mA
    except:
        gauge_com.close() # remember to always close the serial port
        return 
    
def startPump():
    '''
    

    Raises
    ------
    IndexError
        DESCRIPTION.

    Returns
    -------
    current : TYPE
        DESCRIPTION.

    '''
    gauge_com=serial.Serial(port=com_port,  # Opening the serial port once seems to be more stable
                            baudrate=9600,
                            bytesize=8,
                            parity='N',
                            stopbits=1,
                            timeout=1,
                            xonxoff=0,
                            rtscts=0)
    
    try: 
        
        message = makepacketWrite(ADDR = b'\x80',WIN = b'000',COM = b'\x31', DATA = b'1') #
    

        
        gauge_com.flushInput()  # flush the input buffer
        gauge_com.flushOutput() # flush the output buffer
        
        gauge_com.write(message)
        response = gauge_com.readline()
        gauge_com.close()
    
        
        crc_1 = response[-2:] # 
        if (crc_1 != crc_check(response)):
            raise IndexError('r') # this can be refined. An exception is raised if the received CRC is not equal to the calculated CRC
        return # 
    except:
        gauge_com.close() # remember to always close the serial port
        return 
    
    
def stopPump():
    '''
    

    Raises
    ------
    IndexError
        DESCRIPTION.

    Returns
    -------
    current : TYPE
        DESCRIPTION.

    '''
    gauge_com=serial.Serial(port=com_port,  # Opening the serial port once seems to be more stable
                            baudrate=9600,
                            bytesize=8,
                            parity='N',
                            stopbits=1,
                            timeout=1,
                            xonxoff=0,
                            rtscts=0)
    
    try: 
        
        message = makepacketWrite(ADDR = b'\x80',WIN = b'000',COM = b'\x31', DATA = b'0') #
    

        
        gauge_com.flushInput()  # flush the input buffer
        gauge_com.flushOutput() # flush the output buffer
        
        gauge_com.write(message)
        response = gauge_com.readline()
        gauge_com.close()
    
        
        crc_1 = response[-2:] # 
        if (crc_1 != crc_check(response)):
            raise IndexError('r') # this can be refined. An exception is raised if the received CRC is not equal to the calculated CRC
        return # 
    except:
        gauge_com.close() # remember to always close the serial port
        return 
        
    
    
# def remoteMode():
#     '''
    

#     Raises
#     ------
#     IndexError
#         DESCRIPTION.

#     Returns
#     -------
#     current : TYPE
#         DESCRIPTION.

#     '''
#     gauge_com=serial.Serial(port=com_port,  # Opening the serial port once seems to be more stable
#                             baudrate=9600,
#                             bytesize=8,
#                             parity='N',
#                             stopbits=1,
#                             timeout=1,
#                             xonxoff=0,
#                             rtscts=0)
    
#     try: 
        
#         message = makepacket(ADDR = b'\x80',WIN = b'000',COM = b'\x31',DATA=b'1') #
    

        
#         gauge_com.flushInput()  # flush the input buffer
#         gauge_com.flushOutput() # flush the output buffer
        
#         gauge_com.write(message)
#         response = gauge_com.readline()
#         gauge_com.close()
    
        
#         crc_1 = response[-2:] # 
#         if (crc_1 != crc_check(response)):
#             raise IndexError('r') # this can be refined. An exception is raised if the received CRC is not equal to the calculated CRC
#         return # 
#     except:
#         gauge_com.close() # remember to always close the serial port
#         return     

def update_plot():
    # matplotlib.use("Qt5Agg")
    # clear plots
    subplots[0].clear()
    subplots[1].clear()
    # subplots[2].cla()
    # subplots[3].cla()
    
    # Pressure plot
    subplots[0].set_title('Pressure and Pump Current')
    subplots[0].set_ylabel('Pressure [mBar]')
    subplots[0].set_yscale("log")
    subplots[0].grid(True)  
    subplots[0].minorticks_on()
    subplots[0].plot(time_values, pressure_values, label = 'pressure: %.2e'%(pressure))
    subplots[0].set_xticklabels([])
    for i, txt in enumerate(annotation_labels):
        subplots[0].plot(annotation_x[i], annotation_y[i],'o',label=annotation_labels[i])
    subplots[0].legend()
# axis[0].plot(time_values, pressure_values)#, label='Pressure (mB): %.2e'%(pressure), color="blue", linewidth=1)#, marker='x', )
               
# axis[0].set_yscale("log") # ax1.set_color('orange')



# Spectrum Plot ADC0
    # subplots[1].set_title('Pump Current')
    subplots[1].set_ylabel('Pump current [mA]')
    subplots[1].grid(True)  
    subplots[1].plot(time_values, pump_current_values, label = 'current: %i mA'%(pump_current))
    subplots[1].set_xlabel('Time since test start [min]')
    subplots[1].legend()
    fig.tight_layout()
    # update_plot.counter += 1
    matplotlib.pyplot.savefig(log_file_name+'.png', dpi=400 )    
    matplotlib.pyplot.pause(0.1)
    matplotlib.pyplot.show()
    # matplotlib.pyplot.savefig(log_file_name+'.png', dpi=400 )     

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
        log_file.write('\n Time since start of test (s) \t Pressure (mb) \t Turbopump Current \n') # set up header
        
    with open(log_file_name+' error log.txt', 'w') as error_log_file: # open the file with write privelages
       error_log_file.write('The error log for data captured from the '+dut+' '+meas+'\n')
       error_log_file.write('Start date and time:'+(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
       error_log_file.write('\n Time since start of test (m) \t Error\n') # set up header

#%  Create variables for use in main loop
    pressure_values = []
    pump_current_values = []
    time_values = []
    annotation_labels =[]
    annotation_x =[]
    annotation_y =[]
    test_start_time = datetime.now() # this is the test start time
    test_start_time2 = time.time()



#%    Main loop to capture pressure reading, update plot, and save data to log file

    while True: # main loop starts
          
        try:

# capture at least two pressure readings to be able to plot a line graph
                if (len(pressure_values)<3): ## will only run if the length of the pressure values array is less than 3
                    # get current time
                    current_time = time.time()-test_start_time2
                    # capture pressure reading
                    
                    pressure = getPressure()
                    pump_current = getPumpCurrent()
                    print('less than 3')
                    
                    # gauge_com.close() # remember to always close the serial port
                    print('Time since test start (m): %0.1f \n Measured pressure: %.3e mBar \n Pump current %f mA '%(current_time/60, pressure, pump_current))


                    # Add the data to the plot
                    pressure_values.append(pressure) # pressure values for use in the plot
                    pump_current_values.append(pump_current)
                    
                    time_values.append(current_time/60) # time value array for use in the plot
                    with open(log_file_name+'.txt', 'a') as log_file:
                        log_file.write('%0.1f \t %e \t %f \n' %((current_time/60, pressure, pump_current)))
           

                #enough values are present, now we can start plotting the graph
                # get current time
                current_time = time.time()-test_start_time2
                # capture pressure reading
                # capture pressure reading

                pressure = getPressure()
                pump_current = getPumpCurrent()

                print('Time since test start (m): %0.1f \n Measured pressure: %.3e mBar \n Pump current %f mA '%(current_time/60, pressure, pump_current))
                print('Press a to add an annotation')
                print('Press s to start the pump')
                print('Press t to stop the pump')
                


                # print('Time since test start (m): %0.1f \n Measured pressure: %.3e mBar \n Pump current %f mA'%(current_time/60, pressure, pump_current))
                # Add the data to the plot
                
               
                pressure_values.append(pressure) # pressure values for use in the plot. If no value was returned from the serial port, then this will cause an exception
                time_values.append(current_time/60) # time value array for use in the plot
                pump_current_values.append(pump_current)

                if keyboard.is_pressed('a'):
                    temp = input("enter the annotation? ")
                    annotation_labels.append(temp)
                    annotation_x.append(current_time/60)
                    annotation_y.append(pressure)

                if keyboard.is_pressed('s'):
                    startPump()    
                    temp = "Pump started"
                    print("pump started")
                    annotation_labels.append(temp)
                    annotation_x.append(current_time/60)
                    annotation_y.append(pressure)

                if keyboard.is_pressed('t'):
                    stopPump()
                    temp = "Pump stopped"
                    print("pump stopped")
                    annotation_labels.append(temp)
                    annotation_x.append(current_time/60)
                    annotation_y.append(pressure)
                             

                #set up the figure with a subplot to be plotted
                matplotlib.pyplot.rcParams['figure.dpi'] = 400
                fig, subplots = matplotlib.pyplot.subplots(2,1)
                update_plot()
                

                
                # plt.pause(0.01) 
                # save data to the log file
                with open(log_file_name+'.txt', 'a') as log_file:
                    log_file.write('%0.1f \t %e \t %f \n' %(current_time/60, pressure, pump_current))
         #   file.close()  # close the file again. Apparently this is not necessary when the with open it used
                # Writing 
            # wait 10 ms
                # time.sleep(0.001)
                # plt.clf()   # clear the plot to prevent filling up the memory with many plots
                # plt.close()




     
        except KeyboardInterrupt:   # If the keyboard halts 
            print('keyboard interrupt')
            # plt.close()
            
            with open(log_file_name+' error log.txt', 'a') as error_log_file:
                error_log_file.write('%0.1f \t keyboard interrupt ended the test \n' %((current_time/60)))
            break
        except:                                         # On any other exception, restart the loop
            print('An exception occured. Discarded the last sample and restarting the measurement loop')
            with open(log_file_name+' error log.txt', 'a') as error_log_file:
                error_log_file.write('%0.1f \t An exception occured possibly due to corrupt serial data or disconnection of serial port. Discarded last sample and continue the measurement loop \n' %((current_time/60)))
            continue # try to go back into the main loop again

            
        

            
