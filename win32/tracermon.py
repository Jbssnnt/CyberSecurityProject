# -*- coding: utf-8 -*-
"""
Last updated on Nov 08 18:30:00 2018

@author: TimothyC
"""
    
from subprocess import Popen, PIPE
import psutil
import time
import os
import pandas as pd
import datetime
import sys
import platform

# - - - - - - - - - -

#wait for Procmon.exe and/or Procmon64.exe to finalise before continuing.
def wait_for_process(proc1, proc2):
    continued = True
    while continued:
        continued=False 
        for proc in psutil.process_iter():
            #if( proc.name() == "Procmon.exe" or proc.name() == "Procmon64.exe" ):
            if( proc.name() == proc1 or proc.name() == proc2 ):
                #print("still open. waiting...")
                continued = True
        #time.sleep(2) 

# - - - - - - - - - -

#make sure stuff isnt running 
def cleanup():
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == "Listdlls.exe":
            proc.kill()
        if proc.name() == "Listdlls64.exe":
            proc.kill()

# - - - - - - - - - -

def bigfunc( runtime ):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print("Current date and time: " , timestamp)
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\"
    

    #make sure the working directory exists
    workingDirectory = dir_path+"working\\"
    if not os.path.exists(workingDirectory):
        os.makedirs(workingDirectory)

    #create directory to put new output into based on the day
    if not os.path.exists(workingDirectory+timestamp):
        os.makedirs(workingDirectory+timestamp)

    
    #make sure there's not already something running in the background. - gracefully close the program
    try:
        process = Popen([dir_path+"Procmon.exe", "/Terminate"])
    except:
        zzz=0 #do nothing
    else:
        wait_for_process("Procmon.exe", "Procmon64.exe")
    
    #start the process capture
    ##DEBUG: Procmon.exe /NoFilter /AcceptEula /BackingFile C:\temp\raw.pml
    process = Popen([dir_path+"Procmon.exe", "/accepteula", "/NoFilter", "/Quiet", "/Minimized", "/BackingFile", workingDirectory+timestamp+"\\"+"raw.pml"])

    print("Capturing all calls...")
    
    timestamp_dll_start = datetime.datetime.now()
    
    print("  dll capture start...", end='', flush=True)
    DLLSoutput = []
    with os.popen(dir_path+'ListDlls.exe -accepteula') as cmd:
        for line in cmd:
            DLLSoutput.append(line.rstrip()) #remove newline characters
    print("finished\n")
    
    timestamp_dll_end = datetime.datetime.now()     
    timestamp_dll_runtime = timestamp_dll_end-timestamp_dll_start
    
    if ( float(timestamp_dll_runtime.seconds) > float(runtime)):
        #took a little longer than expected. sorry.
        zzz=0
    else:
        #gotta wait the remaining time before continuing...
        time.sleep( float(runtime) - float(timestamp_dll_runtime.seconds) )   
    
    #after sleeping, close the procmon app
    ##DEBUG: Procmon.exe /Terminate
    process = Popen([dir_path+"Procmon.exe", "/Terminate"])
    
    wait_for_process("Procmon.exe", "Procmon64.exe")
    
    print("Converting raw output to CSV...")
    print("(Depending on time run and programs open, it may take a while)\n")
        
    #convert into usable format
    ##DEBUG: Procmon.exe /NoFilter /AcceptEula /OpenLog C:\temp\raw.pml /SaveAs C:\temp\output.csv
    process = Popen([dir_path+"Procmon.exe", "/accepteula", "/LoadConfig", dir_path+"config.pmc", "/SaveApplyFilter", "/Quiet", "/Minimized", "/OpenLog", workingDirectory+timestamp+"\\"+"raw.pml", "/SaveAs", workingDirectory+timestamp+"\\"+"output.csv"]) 

    wait_for_process("Procmon.exe", "Procmon64.exe")

    #read the outputted file as a CSV via pandas library
    output = pd.read_csv(workingDirectory+timestamp+"\\"+"output.CSV", na_values=['.'])
    
    print("Sorting statistics...")
    print("(Depending on time run and programs open, it may take even longer)\n")
    
    PIDs=[]
    pending=True
    syscall_exists=True
    for i in range (0, len(output)):
        PIDs_String = output['PID'][i]
        PIDs_Exe    = output['Process Name'][i]
        PIDs_Op     = output['Operation'][i]
        PIDs_User  = output['User'][i]
        
        #array is empty, add the first PID
        if( len(PIDs) == 0):
                PIDs.append([]) #initiate array
                PIDs[0].append( PIDs_String ) #add first PID
                PIDs[0].append( str( PIDs_Exe ) ) #add first PID name for future reference
                PIDs[0].append( str( PIDs_User ) ) #add first owner of the PID name for future reference
                PIDs[0].append( str( PIDs_Op ) ) #add first PID call
                PIDs[0].append( 1 ) #add first counter for syscall
        else:
            for j in range (0, len(PIDs)):
                if(PIDs_String != PIDs[j][0] ):
                    pending=True
                else:
                    #The PIDs exists in our array, so increase the counter to show that this specific all has been used multiple times           
                    for k in range (3, len(PIDs[j]), 2):
                        
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
                PIDs[j+1].append( str( PIDs_User ) ) #add new PID name for future reference
                PIDs[j+1].append( str( PIDs_Op ) ) #add new PID call
                PIDs[j+1].append( 1 ) #add counter for new syscall
            
            
    #checks the captured DLLs and puts them into an array/list to use for later
    dll_show_pid = False
    dll_list=[]
    dll_index = -1 #har har, gotta start here so we can actually start at 0
    #put all the dll calls into a simple array/list for laters
    for outs in DLLSoutput:
        #check to see if we want to capture the output
        if( ".exe pid: " in outs):
            dll_show_pid = True
            dll_index = dll_index+1
        
        #check for invalid entries
        if( "Error opening " in outs 
           or outs == "------------------------------------------------------------------------------"
           or outs == "'"):
            dll_show_pid = False
            
        #if we do, put into a new array
        if(dll_show_pid == True):
            #print(outs)
            if( ".exe pid: " in outs):
                splitline = outs.split(' ')
                dll_list.append([]) #add new item to our array-list
                dll_list[dll_index].append( splitline[-1] )
            else:
                dll_list[dll_index].append( outs )       

    
    #now write this to file nicely
    print("Writing statistics to file")
    
    temp = "temp"
    #with open(workingDirectory+timestamp+"\\"+"\\" +"output_for_.txt", "a", "utf-8") as myfile:
    with open(workingDirectory+timestamp+"\\"+"statistics.txt", "w") as myfile:
        #myfile.write(str(PIDs))
        for each_process in PIDs:
            for index,per_value in enumerate(each_process):
                #print("index: "+ str(index) )
                if(index==0):
                    PIDs_String = str(per_value)
                    myfile.write("PID:  "+ PIDs_String +"\n")
                elif(index==1):
                    PIDs_Exe    = str(per_value)
                    myfile.write("Name: "+ PIDs_Exe +"\n")
                elif(index==2):
                    PIDs_User  = str(per_value)
                    myfile.write("User: "+ PIDs_User +"\n")
                    myfile.write("-------------------------------\n")
                    myfile.write("Times Called | System Call Name\n")
                    myfile.write("-------------------------------\n")
                elif(index==3):
                    temp =  str(per_value) 
                else:
                    if(index%2==0):
                        myfile.write( '{0:12d}'.format(int(per_value) ) )
                        myfile.write(" : ")
                        myfile.write( str(temp) )
                        myfile.write("\n")
                    else:
                        temp =  str(per_value) 
                        
            for index,per_value in enumerate(dll_list):
                if( per_value[0] == PIDs_String):  
                    myfile.write("-------------------------------\n")
                    myfile.write("DLLs used:\n")
                    for count,zxc in enumerate(per_value):
                        if(count > 2):
                            myfile.write(zxc)
                            myfile.write("\n")
                    myfile.write("\n")            
            myfile.write("\n\n\n")


# - - - - - - - - - -
#  M  A  I  N
# - - - - - - - - - -

def main( ):
    platf0rm = platform.system()
    runtime = 10

    try:
        runtime = int(sys.argv[1])
    except IndexError:
        print("No custom timeframe set, defaulting to 10 seconds.") 
    except ValueError:
        print("Non-numeric value set, defaulting to 10 seconds.")
    else:
        print("Running for ", runtime, "seconds.")

    #lets do a sanity check for OS
    if( platf0rm == "Windows"):    
        cleanup() 
        bigfunc( runtime )
        cleanup() 
    else:
        print("You are trying to run this application on an operating system that is not currently supported. Exiting...")

# - - - - - - - - - -
if __name__ == "__main__":
    main( )
