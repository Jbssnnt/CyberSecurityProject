"""
import psutil

pids = psutil.pids() # get all pids
print(pids)

print(pids[0])

print(psutil.users())

#To access the process information, use:
#p = psutil.Process(1245)  # The pid of desired proces…
"""



from subprocess import Popen, PIPE
import psutil
for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
    except psutil.NoSuchProcess:
        pass
    else:
        print(pinfo)

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
