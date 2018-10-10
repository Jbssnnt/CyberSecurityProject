import os
import sys
import time

def writeSummary():
    callType = []
    occur = []
    outfile = open('TraceCallSummary.txt', 'w')
    p = os.popen('ls -v /tmp/', 'r')
    lines = p.readlines()
    for line in lines:
        if line[0:17] == 'TraceCallRaw.txt.':
            fileobj = open("/tmp/" + line[:-1], 'r')
            tracelines = fileobj.readlines()
            for traceline in tracelines:
                calls = traceline.split('(')
                if calls[0] not in callType:
                        callType.append(calls[0])
                        occur.append(int(1))
                else:
                    occur[callType.index(calls[0])] += 1
            outfile.write('--------------------------------------------------\n')
            outfile.write('Calls by PID ' + line[17:-1] + '\n')
            outfile.write('Calls   | CallType\n')
            for i in range(0, len(occur)):
                outfile.write('{0:7d} | '.format(occur[i]))
                outfile.write(callType[i] + '\n')
        callType = []
        occur = []

def writeRawData():
    outfile = open('TraceCallRaw.txt', 'w')
    p = os.popen('ls -v /tmp/', 'r')
    lines = p.readlines()
    for line in lines:
        if line[0:17] == 'TraceCallRaw.txt.':
            fileobj = open("/tmp/" + line[:-1], 'r')
            tracelines = fileobj.readlines()
            for traceline in tracelines:
                outfile.write('[' + line[17:-1] + '] ' + traceline)

def main():
    if(os.getuid() != 0):
        print("Unable to run with lower privileges not recommended, refer to manual")
        exit()

    # Get a list of PIDs
    pidlist = []
    proc = os.popen('ps -ef', 'r')
    lines = proc.readlines()
    for line in lines[1:]:
        words = line.split()
        if words[7][0] != '[':
            pidlist.append(words[1])

    # execute the strace program for each PID, catching all processes
    cmd = "timeout " + sys.argv[1] + " strace -q -ff -o /tmp/TraceCallRaw.txt"
    for pid in pidlist:
        cmd = cmd + " -p " + str(pid)
    cmd = cmd + " &"
    out = os.popen(cmd)

    time.sleep(int(sys.argv[1]))

    writeSummary()
    writeRawData()

if __name__ == '__main__':
    main()
