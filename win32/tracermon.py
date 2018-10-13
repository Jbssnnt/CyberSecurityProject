# -*- coding: utf-8 -*-
"""
Last updated on Tue Oct  9 20:22:33 2018

@author: overlord00
"""

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
    
#if not os.path.exists(workingDirectory+timestamp):
#    os.makedirs(workingDirectory+timestamp)
"""
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
"""

#open new file made.
#this is the pythonic way to do it without opening a HUGE file.
#with open(workingDirectory+"output.csv") as file:
#    for line in file:
#        print(line)
#        #do something with data

#this is a different way
#read the outputted file as a CSV via pandas library
output = pd.read_csv(workingDirectory+"noexplorernopromon.CSV", na_values=['.'])
"""
array_name_command = []
newPID = False

print("sorting started: "+ str(datetime.datetime.now()))
for i in range (0, len(output)):
    newPID=False
    #print("!")
    #print(output['Process Name'][i])
    #print(i)
    #if(output['PID'][i] not in array_name_command): 
    #    array_name_command.append(output['PID'][i])
        #create file 
        
    print(str(i)+"--"+str(len(array_name_command)))
    
    #if the array is empty, put the first thing in it
    if( len(array_name_command) == 0):
        #array_name_command[0] = str(output['PID'][i])
        array_name_command.append( str(output['PID'][i]) )
        print("2-"+str(len(array_name_command)))
    else:
        for j in range (0, len(array_name_command)):
            #print("Start:"+str(j))
        #    print("yo")
            #print("PID:"+str(output['PID'][i]))
            if( str(output['PID'][i]) == str(array_name_command[j]) ):
                #check to see if the Operation has happened before
                #if yes, add to tally,
                #if no, add to array
                zzz=0
                print("OLD PID")
                #print("3-"+str(len(array_name_command))+"-"+str(output['PID'][i]))
                #print("3-"+str(len(array_name_command))+"-"+str(array_name_command[j]))
                
            else:
                print("NEW PID")
                #newPID = True
                array_name_command.append( str(output['PID'][i]) )
                j = len(array_name_command)+1

            #    #array_name_command[j] = str(output['PID'][i]
                #array_name_command.append( str(output['PID'][i]) )
            #j = j+1 #hack
            #    print("4-"+str(len(array_name_command)))
            #else:
            #    print("adding to already array")
            #print("End:"+str(j))
#        if(newPID==True):
#            array_name_command.append( str(output['PID'][i]) )
#            newPID=False
"""
"""
read the array into memory
go per line
check pid
if no match, add to array
if match check if the line matches
if not add to secondarty array 
if match plus one cound

"""
print("sorting starting: "+ str(datetime.datetime.now()))

#broo = np.array(["test1"]["test2"])

PIDs=[]
pending=True
for i in range (0, len(output)):
    PIDs_String = output['PID'][i]
    #print(">loop number:"+str(i) + " and PID:"+ str( output['PID'][i]) )
    #print(PIDs)
    
    #array is empty, add the first PID
    if( len(PIDs) == 0):
            PIDs.append([])
            PIDs[0].append( PIDs_String )
    else:
        for j in range (0, len(PIDs)):
            #print("j:"+str(j))
            if(PIDs_String != PIDs[j][0] ):
                #print("new PID -- adding to array")
                pending=True
            else:
                #The PIDs match, so increase the counter to show that this specific all has been used multiple times
                #print("dont add PID")
                pending=False
                
                break
        if(pending==True):
            PIDs.append([])
            PIDs[j+1].append( PIDs_String )
            #PIDs_List.extend( str(output['Operation'][i])  )
        


#    if( i % 10000 == 0):
#        print(" - - working - - ")
#    
#    #dump line to file
#    #print(output)
#
#    #"PID","Operation","Path","Result","Detail"
#    with open(workingDirectory+timestamp+"\\"+str(output['PID'][i])+".txt", "a") as myfile:
#        #myfile.write(str(output['PID'][i])) 
#        myfile.write('"' + #str(output['PID'][i])    + '", "' + 
#                     str(output['Operation'][i])    + '", "' + 
#                     str(output['Path'][i])         + '", "' + 
#                     str(output['Result'][i])       + '", "' + 
#                     str(output['Detail'][i])       +  ##invalid symbols. unicode error. please fix
#                     '"\n' )
#
#
#
#
#read line by line and sort into individual files named via PID
#
print(PIDs)
print("sorting complete: "+ str(datetime.datetime.now()))