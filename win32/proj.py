"""
import psutil

pids = psutil.pids() # get all pids
print(pids)

print(pids[0])

print(psutil.users())

#To access the process information, use:
#p = psutil.Process(1245)  # The pid of desired proces…
"""


#import subprocess
#from subprocess import Popen, PIPE
#import psutil
"""
for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
    except psutil.NoSuchProcess:
        pass
    else:
        print(pinfo)
"""
        

"""
process = Popen(["cmd.exe", "", "dir"], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()
print(output)
print(err)
print(exit_code)
"""

#subprocess.run(["cmd", "dir", "."], capture_output=True)
#print("true")
"""
from subprocess import check_output
check_output("dir C:", shell=True)


import subprocess
cmdCommand = "cmd dir C:"   #specify your cmd command
process = subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
print(output)
"""

"""
import subprocess
proc = subprocess.Popen("cmd.exe", stdin = subprocess.PIPE, stdout = subprocess.PIPE)
out, err = proc.communicate("dir c:\\")
"""

import os
os.system("pwd", stdout=PIPE)