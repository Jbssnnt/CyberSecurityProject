# -*- coding: utf-8 -*-
"""
Last updated on Tue Oct  9 20:22:33 2018

@author: overlord00
"""

# NOTE: msvcr100.dll and msvcp100.dll are required for NtTrace.exe
#from subprocess import Popen, PIPE
import psutil
import time
import os


#make sure the working directory exists
workingDirectory = ".\\working\\"
if not os.path.exists(workingDirectory):
    os.makedirs(workingDirectory)

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
#for i in array_process:


#print(i) #debug
current_app_PID = (array_process[counter]['pid'])
print(current_app_PID) #debug
current_app_name = (array_process[counter]['name'])
print(current_app_name) #debug
current_app_owner = (array_process[counter]['username'])
print(current_app_owner) #debug
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

#convert into usable format
##DEBUG: Procmon.exe /NoFilter /AcceptEula /OpenLog C:\temp\output.pml /SaveAs C:\temp\output.csv
process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/OpenLog", "C:\\temp\\output.pml", "/SaveAs", workingDirectory+"output.csv"]) ## or to a fixed path: "C:\\temp\\output.csv"])

#process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/OpenLog", "C:\\temp\\output.pml", "/SaveAs", "C:\\temp\\output.xml"])
#process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/OpenLog", "C:\\temp\\output.pml", "/SaveAs1", "C:\\temp\\output-stacktrace.xml"])
#process = Popen(["Procmon.exe", "/AcceptEula", "/NoFilter", "/Quiet", "/Minimized", "/OpenLog", "C:\\temp\\output.pml", "/SaveAs2", "C:\\temp\\output-stacktracesymbols.xml"])

time.sleep(10)  


#open new file made.

#read line by line and sort into individual files named via PID