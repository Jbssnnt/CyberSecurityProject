import os
import sys
import time
import re

# This is a regular expression for finding files containing .so 
objectRegex = re.compile('''
(.*\.so.*)
''', re.VERBOSE)

# This is a function for obtaining all the shared opjects for the processes
# before we run the strace. The program iterates through all the maps files in
# the /proc folder and grabs the linked shared objects.

def getSOMaps(pidlist):
    maplist = []
    # Keeping track of list positions to save time and avoid iterating over
    # the whole list over and over
    i = 0
    j = 0

    for pid in pidlist:
        mapfile = open('/proc/' + pid + '/maps', 'r')
        maps = mapfile.readlines()

        for line in maps:
            line = line.strip()
            soline = objectRegex.search(line)

            # We don't want to add duplicates to the list as there is a lot
            if soline:
                mapline = ('[' + '{0:5d}'.format(int(pid)) + '] ' + soline.group().split()[5])
                if mapline not in maplist[i:]:
                    maplist.append(mapline)
                    j += 1
        i += j
        j = 0
    return maplist

# This function writes a summary of the system calls for the process and outputs
# them into a file called TraceCallSummary.txt. This summary includes the 
# system calls that the process made and the number of times that the call was
# made. 

def writeSummary(processes):
    callType = []
    occur = []
    # N/A is a placeholder for processes that don't have a name or path
    # associated with them.
    name = "N/A"
    user = "N/A"
    totalCalls = 0
    outfile = open('TraceCallSummary.txt', 'w')
    p = os.popen('ls -v /tmp/tracer/', 'r')
    lines = p.readlines()

    for line in lines:

        if line[0:17] == 'TraceCallRaw.txt.':
            fileobj = open("/tmp/tracer/" + line[:-1], 'r')
            tracelines = fileobj.readlines()

            for traceline in tracelines:
                calls = traceline.split(' ')
                
                # This is where we check if a call is a repeat or a new call
                if calls[1].split('(')[0] not in callType:
                        callType.append(calls[1].split('(')[0])
                        occur.append(int(1))
                else:
                    occur[callType.index(calls[1].split('(')[0])] += 1
            
            # Here we are grabbing the assiciated name or path for each process
            # if it is available
            for proc in processes:
                proc = proc.split()

                if line[17:-1] == proc[1]:
                    name = proc[7]
                    user = proc[0]

            outfile.write('PID: ' + line[17:-1] + '\n')
            outfile.write('Name: ' + name + '\n')
            outfile.write('User: ' + user + '\n')
            outfile.write('-------------------------------\n')
            outfile.write('Times Called | System Call Name\n')

            for i in range(0, len(occur)):
                outfile.write('{0:12d} : '.format(occur[i]))
                outfile.write(callType[i] + '\n')
            outfile.write('-------------------------------\n')
            outfile.write('\n\n')
        callType = []
        occur = []
        name = 'N/A'
        user = 'N/A'

def writeRawData():
    calllist = []
    p = os.popen('ls -v /tmp/tracer/', 'r')
    lines = p.readlines()
    for line in lines:
        if line[0:17] == 'TraceCallRaw.txt.':
            fileobj = open("/tmp/tracer/" + line[:-1], 'r')
            tracelines = fileobj.readlines()
            for traceline in tracelines:
                calllist.append('[' + '{0:6d}'.format(int(line[17:-1])) + '] ' + traceline)
    calllist.sort(key=lambda x:x[8:25])
    outfile = open('TraceCallRaw.txt', 'w')
    for line in calllist:
        outfile.write(line)

def writeMaps(maplist, processes):
    runtime = []
    fileobj = open('TraceCallRaw.txt', 'r')
    calls = fileobj.readlines()
    for call in calls:
        call = call.strip()
        soline = objectRegex.search(call)
        if soline:
            soline = soline.group().split('"')
            for word in soline:
                obj = objectRegex.search(word)
                if obj:
                    newObj = "[" + call[1:7] + "] " + obj.group()
                    if newObj not in runtime:
                        runtime.append(newObj)

    outfile = open('MapSummary.txt', 'w')
    name = 'N/A'
    currpid = 1
    outfile.write('---------SHARED OBJECTS LINKED DURING RUNTIME---------')
    for mapline in runtime:
        pid = str(int(mapline[1:6]))
        for proc in processes[1:]:
            proc = proc.split()
            if pid == proc[1]:
                name = proc[7]
        if pid != currpid:
            outfile.write('--------------------------------------------------\n')
            outfile.write('PID: ' + '{0:5d}'.format(int(pid)) + ' | Process Path: ' + name + '\n')
            outfile.write('\t' + mapline[8:] + '\n')
            currpid = pid
        else:
            outfile.write('\t' + mapline[8:] + '\n')
        name = 'N/A'

    outfile.write('\n\n\n---------SHARED OBJECTS LINKED BEFORE RUNTIME---------')
    for mapline in maplist:
        pid = str(int(mapline[1:6]))
        for proc in processes[1:]:
            proc = proc.split()
            if pid == proc[1]:
                name = proc[7]
        if pid != currpid:
            outfile.write('--------------------------------------------------\n')
            outfile.write('PID: ' + '{0:5d}'.format(int(pid)) + ' | Process Path: ' + name + '\n')
            outfile.write('\t' + mapline[8:] + '\n')
            currpid = pid
        else:
            outfile.write('\t' + mapline[8:] + '\n')
        name = 'N/A'

def main():
    if(os.getuid() != 0):
        print("Unable to run with lower privileges not recommended, refer to manual")
        exit()
    
    # Here we are checking to see if our system has strace installed. If it 
    # doesn't then it should exit
    checkstrace = os.popen('ls /usr/bin | grep strace', 'r')
    if len(checkstrace.readlines()) == 0:
        print("Program requires strace for operation\nTry installing using:")
        print("\n\tsudo apt-get install strace\n")
        exit()

    # Get a list of PIDs
    pidlist = []

    os.popen('mkdir /tmp/tracer')
    proc = os.popen('ps -ef', 'r')
    processes = proc.readlines()
    for line in processes[1:-2]:
        words = line.split()
        if words[7][0] != '[':
            pidlist.append(words[1])

    maplist = getSOMaps(pidlist)
    # execute the strace program for each PID, catching all processes
    cmd = "timeout " + sys.argv[1] + " strace -q -ff -ttt -o /tmp/tracer/TraceCallRaw.txt"
    print("Beginning tracing of processes")
    for pid in pidlist:
        cmd = cmd + " -p " + str(pid)
    cmd = cmd + " &"
    out = os.popen(cmd)

    time.sleep(int(sys.argv[1]))
    print("Tracing complete, generating summary")
    writeSummary(processes)
    writeRawData()
    writeMaps(maplist, processes)
    print("Program complete")
    os.popen('rm -rf /tmp/tracer')

if __name__ == '__main__':
    main()
