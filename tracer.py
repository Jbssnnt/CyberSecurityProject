import os
import sys
import time

def writeSummary():
    callType = []
    occur = []
    outfile = open('TraceCallSummary.txt', 'w')
    p = os.popen('ls -v /tmp/tracer/', 'r')
    lines = p.readlines()
    for line in lines:
        if line[0:17] == 'TraceCallRaw.txt.':
            fileobj = open("/tmp/tracer/" + line[:-1], 'r')
            tracelines = fileobj.readlines()
            for traceline in tracelines:
                calls = traceline.split(' ')
                if calls[1].split('(')[0] not in callType:
                        callType.append(calls[1].split('(')[0])
                        occur.append(int(1))
                else:
                    occur[callType.index(calls[1].split('(')[0])] += 1
            outfile.write('--------------------------------------------------\n')
            outfile.write('Calls by PID ' + line[17:-1] + '\n')
            outfile.write('Calls   | CallType\n')
            for i in range(0, len(occur)):
                outfile.write('{0:7d} | '.format(occur[i]))
                outfile.write(callType[i] + '\n')
        callType = []
        occur = []

def writeRawData():
    calllist = []
    p = os.popen('ls -v /tmp/tracer/', 'r')
    lines = p.readlines()
    for line in lines:
        if line[0:17] == 'TraceCallRaw.txt.':
            fileobj = open("/tmp/tracer/" + line[:-1], 'r')
            tracelines = fileobj.readlines()
            for traceline in tracelines:
                calllist.append('[' + '{0:5d}'.format(int(line[17:-1])) + '] ' + traceline)
    calllist.sort(key=lambda x:x[8:25])
    outfile = open('TraceCallRaw.txt', 'w')
    for line in calllist:
        outfile.write(line)

def main():
    if(os.getuid() != 0):
        print("Unable to run with lower privileges not recommended, refer to manual")
        exit()

    checkstrace = os.popen('ls /usr/bin/ | grep strace', 'r')
    if len(checkstrace.readlines()) == 0:
        print("Program requires strace for operation\nTry installing using:")
        print("\n\tsudo apt-get install strace\n")
        exit()

    # Get a list of PIDs
    pidlist = []

    os.popen('mkdir /tmp/tracer')
    proc = os.popen('ps -ef', 'r')
    lines = proc.readlines()
    for line in lines[1:-2]:
        words = line.split()
        if words[7][0] != '[':
            pidlist.append(words[1])

    # execute the strace program for each PID, catching all processes
    cmd = "timeout " + sys.argv[1] + " strace -q -ff -ttt -o /tmp/tracer/TraceCallRaw.txt"
    for pid in pidlist:
        cmd = cmd + " -p " + str(pid)
    cmd = cmd + " &"
    out = os.popen(cmd)

    time.sleep(int(sys.argv[1]))

    writeSummary()
    writeRawData()
    os.popen('rm -rf /tmp/tracer')

if __name__ == '__main__':
    main()
