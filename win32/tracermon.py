# -*- coding: utf-8 -*-
"""
Last updated on Tue Oct  9 20:22:33 2018

@author: overlord00
"""

# NOTE: msvcr100.dll and msvcp100.dll are required for NtTrace.exe
from subprocess import Popen
import psutil
import time
import os
import pandas as pd
import numpy as np
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
print("Current date and time: " , timestamp)


#make sure the working directory exists
workingDirectory = ".\\working\\"
if not os.path.exists(workingDirectory):
    os.makedirs(workingDirectory)
    
if not os.path.exists(workingDirectory+timestamp):
    os.makedirs(workingDirectory+timestamp)

index=0
array_process = []
#array_proc_name = []
#array_proc_title = []
#read through all processes ang grab PID, executable name, and user
for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])#, 'name', 'username', "name", "exe", "cmdline", 'status'])

    except psutil.NoSuchProcess:
        pass
    else:
        #print(pinfo)
        #print(proc.pid)
        #print(proc.name())
        #print(proc.username()) #doesnt work for some reason
        array_process.append(pinfo)
        #array_proc_name.append(proc.pid)
        #array_proc_title.append(proc.name)
        #print(\"""pinfo, \""" "proc:", proc, "index:", index)
        index = index+1
        

counter=0
#for i in array_process:


#print(i) #debug
current_app_PID = (array_process[counter]['pid'])
print(current_app_PID) #debug
#current_app_name = (array_process[counter]['name'])
#print(current_app_name) #debug
#current_app_owner = (array_process[counter]['username'])
#print(current_app_owner) #debug
counter = counter + 1 #theres a better way to do this, i dont remember how

#currently using random executable as testing
#if("VisualBoyAdvance-M.exe" in current_app_name ):
#print("werfkjmhfgehjklsaRFGhjklgsedrkgjlheaweagjkhlwsekrajghwlghjkarewgkjhaerwghjkaerwkghjaewrgkhjaewrgkhjlgkjhlarew")
#
##runs listdlls.exe with argument from previously

#run process monitor (from sysinternals)
##DEBUG: Procmon.exe /NoFilter /AcceptEula /BackingFile C:\temp\output.pml
process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/BackingFile", workingDirectory+"output.pml"]) ## or to a fixed path: "C:\\temp\\output.pml"])

#process = Popen(["Listdlls.exe", "5008", ""], stdout=PIPE)
#(output, err) = process.communicate()
#exit_code = process.wait()
#print(output)
#print(err)
#print(exit_code)


#gather data for x seconds
time.sleep(10)   # delays for 5 seconds. You can Also Use Float Value.

#after sleeping, close the procmon app
##DEBUG: Procmon.exe /Terminate
process = Popen(["Procmon.exe", "/Terminate"])

#make sure the file is closed before trying to read it. :)
time.sleep(10)  
#instead of sleeping for an undetermined amount of time, we should wait to see if the process has been killed.

#convert into usable format
##DEBUG: Procmon.exe /NoFilter /AcceptEula /OpenLog C:\temp\output.pml /SaveAs C:\temp\output.csv
process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/OpenLog", workingDirectory+"output.pml", "/SaveAs", workingDirectory+"output.csv"]) ## or to a fixed path: "C:\\temp\\output.csv"])

#process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/OpenLog", "C:\\temp\\output.pml", "/SaveAs", "C:\\temp\\output.xml"])
#process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/OpenLog", "C:\\temp\\output.pml", "/SaveAs1", "C:\\temp\\output-stacktrace.xml"])
#process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/OpenLog", "C:\\temp\\output.pml", "/SaveAs2", "C:\\temp\\output-stacktracesymbols.xml"])

#wait for the conversion....
time.sleep(10)  


#open new file made.
#this is the pythonic way to do it without opening a HUGE file.
#with open(workingDirectory+"output.csv") as file:
#    for line in file:
#        print(line)
#        #do something with data

#this is a different way
#read the outputted file as a CSV via pandas library
output = pd.read_csv(workingDirectory+"output.csv", na_values=['.'])

array_name_command = []

print("sorting started: "+ str(datetime.datetime.now()))
for i in range (0, len(output)):
    #print("!")
    #print(output['Process Name'][i])
    #print(i)
    #if(output['PID'][i] not in array_name_command): 
    #    array_name_command.append(output['PID'][i])
        #create file 
        
    if( i % 10000 == 0):
        print(" - - working - - ")
    
    #dump line to file
    #print(output)

    #"PID","Operation","Path","Result","Detail"
    with open(workingDirectory+timestamp+"\\"+str(output['PID'][i])+".txt", "a") as myfile:
        #myfile.write(str(output['PID'][i])) 
        myfile.write('"' + #str(output['PID'][i])    + '", "' + 
                     str(output['Operation'][i])    + '", "' + 
                     str(output['Path'][i])         + '", "' + 
                     str(output['Result'][i])       + '", "' + 
                     str(output['Detail'][i])       +  ##invalid symbols. unicode error. please fix
                     '"\n' )




#read line by line and sort into individual files named via PID

print("sorting complete: "+ str(datetime.datetime.now()))