# -*- coding: utf-8 -*-
"""
Last updated on Fri Oct 26 00:00:00 2018

@author: overlord00
"""
    
from subprocess import Popen
import psutil
import time
import os
import pandas as pd
#import numpy as np
import datetime
import sys

# - - - - - - - - - -

#wait for Procmon.exe and/or Procmon64.exe to finalise before continuing.
def wait_for_process():
    continued = True
    while continued:
        continued=False 
        for proc in psutil.process_iter():
            if( proc.name() == "Procmon.exe" or proc.name() == "Procmon64.exe" ):
                #print("still open. waiting...")
                continued = True
        time.sleep(2) 

# - - - - - - - - - -

def bigfunc( runtime ):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print("Current date and time: " , timestamp)
    
    
    #make sure the working directory exists
    workingDirectory = ".\\working\\"
    if not os.path.exists(workingDirectory):
        os.makedirs(workingDirectory)
        
    if not os.path.exists(workingDirectory+timestamp):
        os.makedirs(workingDirectory+timestamp)
    
    

    ##runs listdlls.exe with argument from previously
    
    #run process monitor (from sysinternals)
    ##DEBUG: Procmon.exe /NoFilter /AcceptEula /BackingFile C:\temp\output.pml
    process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/BackingFile", workingDirectory+timestamp+"\\"+"output.pml"]) ## or to a fixed path: "C:\\temp\\output.pml"])
    
    #process = Popen(["Listdlls.exe", "5008", ""], stdout=PIPE)
    #(output, err) = process.communicate()
    #exit_code = process.wait()
    #print(output)
    #print(err)
    #print(exit_code)
    
    
    #gather data for x seconds
    time.sleep( runtime )   
    
    #after sleeping, close the procmon app
    ##DEBUG: Procmon.exe /Terminate
    process = Popen(["Procmon.exe", "/Terminate"])
    
    
    
    wait_for_process()
    
    
    
    
    #make sure the file is closed before trying to read it. :)
    #time.sleep(10)  
    #instead of sleeping for an undetermined amount of time, we should wait to see if the process has been killed.
    
    #convert into usable format
    ##DEBUG: Procmon.exe /NoFilter /AcceptEula /OpenLog C:\temp\output.pml /SaveAs C:\temp\output.csv
    process = Popen(["Procmon.exe", "/AcceptEula", "/LoadConfig", "ProcmonConfiguration.pmc", "/SaveApplyFilter", "/Quiet", "/Minimized", "/OpenLog", workingDirectory+timestamp+"\\"+"output.pml", "/SaveAs", workingDirectory+timestamp+"\\"+"output.csv"]) 
    #we use /LoadConfig ProcmonConfiguration.pmc and /SaveApplyFilter to filter out instances of ProcMon for speed
    
    #process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/OpenLog", "C:\\temp\\output.pml", "/SaveAs", "C:\\temp\\output.xml"])
    #process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/OpenLog", "C:\\temp\\output.pml", "/SaveAs1", "C:\\temp\\output-stacktrace.xml"])
    #process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/OpenLog", "C:\\temp\\output.pml", "/SaveAs2", "C:\\temp\\output-stacktracesymbols.xml"])
    

    wait_for_process()
    
    
    
    #this is a different way
    #read the outputted file as a CSV via pandas library
    output = pd.read_csv(workingDirectory+timestamp+"\\"+"output.CSV", na_values=['.'])
    
    print("sorting starting: "+ str(datetime.datetime.now()))
    
    
    PIDs=[]
    pending=True
    syscall_exists=True
    for i in range (0, len(output)):
        PIDs_String = output['PID'][i]
        PIDs_Exe    = output['Process Name'][i]
        PIDs_Op     = output['Operation'][i]
        #print(">loop number:"+str(i) + " and PID:"+ str( output['PID'][i]) )
        #print(PIDs)
        
        #array is empty, add the first PID
        if( len(PIDs) == 0):
                PIDs.append([]) #initiate array
                PIDs[0].append( PIDs_String ) #add first PID
                PIDs[0].append( str( PIDs_Exe ) ) #add first PID name for future reference
                PIDs[0].append( str( PIDs_Op ) ) #add first PID call
                PIDs[0].append( 1 ) #add first counter for syscall
        else:
            for j in range (0, len(PIDs)):
                #print("j:"+str(j))
                if(PIDs_String != PIDs[j][0] ):
                    #print("new PID -- adding to array")
                    pending=True
                else:
                    #The PIDs exists in our array, so increase the counter to show that this specific all has been used multiple times           
                    for k in range (2, len(PIDs[j]), 2):
                        
                        if( PIDs[j][k] != PIDs_Op):
                            syscall_exists=False
                        else:
                            #PIDs[j].append( str(output['Operation'][i]) )
                            #print("same" + str( PIDs[j][k+1] ) )
                            PIDs[j][k+1] = PIDs[j][k+1] + 1
                            syscall_exists=True
                            break
                    if(syscall_exists==False):                    
                        PIDs[j].append( str( PIDs_Op ) ) #add new PID call
                        PIDs[j].append( 1 ) #add counter for new syscall
                    
                    #we dont need to check any more PIDs. STOP!
                    pending=False
                    break
                
            #add new PID to our array
            if(pending==True):
                PIDs.append([])
                PIDs[j+1].append( PIDs_String )
                #PIDs_List.extend( str(output['Operation'][i])  )
                PIDs[j+1].append( str( PIDs_Exe ) ) #add new PID name for future reference
                PIDs[j+1].append( str( PIDs_Op ) ) #add new PID call
                PIDs[j+1].append( 1 ) #add counter for new syscall
            
    
                
    
    print("sorting complete: "+ str(datetime.datetime.now()))
    
    
    
    #now write this to file nicely
    print("DEBUG: writing start "+ str(datetime.datetime.now()))
    
    #with open(workingDirectory+timestamp+"\\"+"\\" +"output_for_.txt", "a", "utf-8") as myfile:
    with open(workingDirectory+timestamp+"\\"+"output.txt", "w") as myfile:
        #myfile.write(str(PIDs))
        for each_process in PIDs:
            for index,per_value in enumerate(each_process):
                #print("index: "+ str(index) )
                if(index==0):
                    myfile.write("PID:  "+ str(per_value)+"\n")
                elif(index==1):
                    myfile.write("Name: "+ str(per_value)+"\n")
                    myfile.write("------------------------------\n")
                    myfile.write("Syscall:   |   Times called: \n")
                    myfile.write("------------------------------\n")
                else:
                    
                    myfile.write( str(per_value) )
                    if(index%2==1):
                        myfile.write("\n")
                    else:
                        myfile.write(" : ")
            myfile.write("\n\n\n")
    print("DEBUG: writing complete: "+ str(datetime.datetime.now()))

# - - - - - - - - - -
#  M  A  I  N
# - - - - - - - - - -

def main():
    
    try:
        runtime = int(sys.argv[1])
    except IndexError:
        print("No custom timeframe set, defaulting to 10 seconds.") 
        runtime = 10
    except ValueError:
        print("Non-numeric value set, defaulting to 10 seconds.") 
        runtime = 10
       

    
    bigfunc(runtime)
    
# - - - - - - - - - -
if __name__ == "__main__":
    main()