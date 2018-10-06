# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 21:11:29 2018

@author: Timothy Covich
"""



##
##
## NOTE:
##  Apparently, you cannot just run the Listdlls.exe
##  It requires you to accept a licening agreement before it will work!
##
##

from subprocess import Popen, PIPE
import psutil



index=0
array_proc = []
#read through all processes ang grab PID, executable name, and user
for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid'])#, 'name', 'username', "name", "exe", "cmdline", 'status'])
    except psutil.NoSuchProcess:
        pass
    else:
        print(pinfo)
        array_proc.append(pinfo)
        #print("""pinfo, """ "proc:", proc, "index:", index)
        index = index+1

#neww = (array_proc[0]['pid'])
#print(neww)

counter=0
for i in array_proc:
    print(i) #debug
    currentPID = (array_proc[counter]['pid'])
    print(currentPID) #debug
    counter = counter + 1 #theres a better way to do this, i dont remember how



    
    
    ##runs listdlls.exe with argument from previously
    process = Popen(["Listdlls.exe", str(currentPID), ""], stdout=PIPE)
    #process = Popen(["Listdlls.exe", "5008", ""], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    #print(output)
    #print(err)
    #print(exit_code)
    
    
    newoutput = str(output).split("\\r\\n")
    for line in newoutput:
        if not line:
            zzz=0 #makes sure the line is not null
        else:
            #print("line is '",line,"'")
            if(line[0] == '0'):
                #print(line)
                
                #note: AttributeError: 'list' object has no attribute 'split'
                #finaloutput = newoutput.split()
                
                #lets cheat instead. assume string length is always 30
                #print(line[30:]) #hack
                print(line) 
                #NOTE: wont work because its not always 30 characters :\
            #else:
            #    print("- - - - - - - - - - FAILED - - - - - - - - - -")
            #    print(line)
    
    #print(newoutput)