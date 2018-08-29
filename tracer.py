import os
import sys
import time

p = os.popen('ls /usr/bin/ | grep \"^strace$\"', 'r')
line = p.readline()
if line == "strace\n":
    print("You have strace")
else:
    print("Go get strace")
    exit()

if(os.getuid() == 0):
    print("Running in sudo")
else:
    print("Running with lower privileges not recommended, refer to manual")
    exit()

pidlist = []
ppidlist = []
os.system('ps -ef > process.txt')
fileobj = open('process.txt', 'r')
lines = fileobj.readlines()
for line in lines:
    words = line.split()
    if words[1].isdigit():
        pidlist.append(words[1])
    if words[2].isdigit():
        ppidlist.append(words[2])

'''i = 0    
for pid in pidlist:
    if pid == '1' or pid == '3':
        print("Will not strace pid: " + pid)
    else:
        if ppidlist[i] == '1' or ppidlist[i] == '3':
            cmd = "timeout 15 strace -q -ff -o piddetails.txt -p " + pid + " &"
            os.system(cmd)
    i = i + 1
'''
#time.sleep(11)
callType = []
occur = []
p = os.popen('ls', 'r')
lines = p.readlines()
print(lines)
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
        print('-------------------------------------------------------------')
        print('Calls by PID ' + line[15:])
        print('Calls   | CallType\n')
        for i in range(0, len(occur)):
            print('{0:7d}'.format(occur[i]), end = " | ")
            print(callType[i])

os.system('rm process.txt')
