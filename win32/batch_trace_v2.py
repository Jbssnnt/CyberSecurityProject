# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 19:17:13 2018

@author: overlord00
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 21:11:29 2018

@author: Timothy Covich
"""


# NOTE: msvcr100.dll and msvcp100.dll are required for NtTrace.exe
from subprocess import Popen, PIPE
import psutil



index=0
array_process = []
array_proc_name = []
array_proc_title = []
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
        #print("""pinfo, """ "proc:", proc, "index:", index)
        index = index+1
        

counter=0
for i in array_process:
    #print(i) #debug
    current_app_PID = (array_process[counter]['pid'])
    print(current_app_PID) #debug
    current_app_name = (array_process[counter]['name'])
    print(current_app_name) #debug
    current_app_owner = (array_process[counter]['username'])
    print(current_app_owner) #debug
    counter = counter + 1 #theres a better way to do this, i dont remember how
    
    #currently using random executable as testing
    if("notepad.exe" in current_app_name ):
        #print("werfkjmhfgehjklsaRFGhjklgsedrkgjlheaweagjkhlwsekrajghwlghjkarewgkjhaerwghjkaerwkghjaewrgkhjaewrgkhjlgkjhlarew")
#
        ##runs listdlls.exe with argument from previously
        process = Popen([".\\NtTrace64\\protobat.bat", str(current_app_name), str(current_app_PID), ""])
        #process = Popen(["Listdlls.exe", "5008", ""], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        #print(output)
        #print(err)
        #print(exit_code)
