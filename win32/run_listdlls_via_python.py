# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 12:57:22 2018

@author: winter
"""


from subprocess import Popen, PIPE
import psutil
"""
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
        #print(***********proc******** "proc:", proc, "index:", index)
        index = index+1

neww = (array_proc[30]['pid'])
print(neww)
"""

"""
#
# NOTE:
#
# we are running via powershell (for Windows OS) because CMD will not work
#

# just to get directory listing
process = Popen(["powershell.exe", "pwd", "."], stdout=PIPE)
(output, err) = process.communicate()
print(output)

#runs DIR as a test 
process = Popen(["powershell.exe", "dir", "."], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()
print(output)
print(err)
print(exit_code)
"""

"""
for i in range(0, index):
    print(i)
    ##runs listdlls.exe with argument from previously
    process = Popen(["Listdlls.exe", str(array_proc[i]['pid']), ""], stdout=PIPE)
    #process = Popen(["Listdlls.exe", "5008", ""], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    print(output)
    print(err)
    print(exit_code)
"""


##runs listdlls.exe with argument from previously
process = Popen(["Listdlls.exe", "3012", ""], stdout=PIPE)
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
            print(line[30:]) #hack
            #NOTE: wont work because its not always 30 characters :\

#print(newoutput)