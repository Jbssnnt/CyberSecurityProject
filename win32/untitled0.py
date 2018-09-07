# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 15:27:16 2018

@author: winter
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 12:57:22 2018

@author: winter
"""


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

neww = (array_proc[0]['pid'])
print(neww)


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

##runs listdlls.exe with argument from previously
process = Popen(["Listdlls.exe", 0, ""], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()
print(output)
print(err)
print(exit_code)
