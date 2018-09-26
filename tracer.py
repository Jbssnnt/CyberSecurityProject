import os
import sys
import time

# if(os.getuid() == 0):
#     print("Running in sudo")
# else:
#     print("Running with lower privileges not recommended, refer to manual")
#     exit()

pidlist = []
proc = os.popen('ps -ef', 'r')
lines = proc.readlines()
for line in lines[1:]:
    words = line.split()
    if words[7][0] != '[':
        pidlist.append(words[1])

for pid in pidlist:
    cmd = "timeout 10 python strace.py -f -o piddetails.txt." + str(pid) + " -p " + str(pid) + " &"
    os.system(cmd)

time.sleep(11)
callType = []
occur = []
outfile = open('results.txt', 'w')
p = os.popen('ls', 'r')
lines = p.readlines()
for line in lines:
    if line[0:9] == 'piddetail':
        fileobj = open(line[:-1], 'r')
        tracelines = fileobj.readlines()
        for traceline in tracelines:
            calls = traceline.split('(')
            if calls[0][0] != '+' and calls[0][0] != '-':
                if calls[0] not in callType:
                    callType.append(calls[0])
                    occur.append(int(1))
                else:
                    occur[callType.index(calls[0])] += 1
        outfile.write('--------------------------------------------------\n')
        outfile.write('Calls by PID ' + line[15:] + '\n')
        outfile.write('Calls   | CallType\n\n')
        for i in range(0, len(occur)):
            outfile.write('{0:7d} |'.format(occur[i]))
            outfile.write(callType[i] + '\n')
    callType = []
    occur = []

os.system("rm -f pid*")
