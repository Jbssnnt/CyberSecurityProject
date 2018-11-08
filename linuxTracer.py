"""
    Authors: Liam Pilling, Jabob Boland, Timothy Covich
    Last Date Modified: 08/11/2018
    Description: This program is designed to capture all of the system calls
    that take place on a linux system using strace. The program relies on strace
    to capture the output and then the program analyses the output. The program
    also grabs all of the shared objects that are mapped to processes and
    outputs that information too. It generates three files:
        - MapSummary.txt: contains all of the shared objects linked to each
                          process.
        - TraceCallRaw.txt: contains all the raw system call data sorted by
                          timestamp.
        - TraceCallSummary.txt: contains a summary of the system calls that
                          occured, sorted by process. This summary contains the
                          system calls that the process made and how many that
                          happened.
"""
import os
import sys
import time
import re
import datetime
import shutil

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

def writeSummary(processes, dirName, resultFold):
    callType = []
    occur = []
    # N/A is a placeholder for processes that don't have a name or path
    # associated with them.
    name = "N/A"
    user = "N/A"
    totalCalls = 0
    outfile = open(resultFold + 'TraceCallSummary.txt', 'w')
    p = os.popen('ls -v ' + dirName, 'r')
    lines = p.readlines()

    for line in lines:

        if line[0:17] == 'TraceCallRaw.txt.':
            fileobj = open(dirName + line[:-1], 'r')
            tracelines = fileobj.readlines()

            for traceline in tracelines:
                calls = traceline.split(' ')

                # This is where we check if a call is a repeat or a new call
                if calls[1].split('(')[0] != '+++' and calls[1].split('(')[0] != '---':
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

# This function writes all of the system calls that happened into one file for
# analysing. This file is ordered by timestamp and contains all information
# associated with a system call, including status and contents. This file
# is also essential for the writeMaps function as it needs to read the raw data
# to determine libraries accessed during runtime.

def writeRawData(dirName, resultFold):
    calllist = []
    p = os.popen('ls -v ' + dirName, 'r')
    lines = p.readlines()

    for line in lines:

        if line[0:17] == 'TraceCallRaw.txt.':
            fileobj = open(dirName + line[:-1], 'r')
            tracelines = fileobj.readlines()

            for traceline in tracelines:
                calllist.append('[' + '{0:6d}'.format(int(line[17:-1])) + '] ' + traceline)

    # Here we sort the list by the timestamp in the file
    calllist.sort(key=lambda x:x[8:25])
    outfile = open(resultFold + 'TraceCallRaw.txt', 'w')

    for line in calllist:
        outfile.write(line)

# This is the function where we write all of the shared objects to a file. This
# starts by finding the objects that were accessed during runtime and prints
# those and then prints all the objects that were accessed before runtime that
# were already mapped to a process.

def writeMaps(maplist, processes, resultFold):
    runtime = []
    fileobj = open(resultFold + 'TraceCallRaw.txt', 'r')
    calls = fileobj.readlines()
    # Here we check the TraceCallRaw.txt file for access to shared objects
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

    outfile = open(resultFold + 'MapSummary.txt', 'w')
    name = 'N/A'
    currpid = 1
    outfile.write('---------SHARED OBJECTS LINKED DURING RUNTIME---------\n')

    # Here we write the shared object paths to the file. Sometimes none will
    # exist if we didn't start new processes or current processes didn'r access
    # any.
    for mapline in runtime:
        pid = str(int(mapline[1:7]))

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

    outfile.write('\n\n\n---------SHARED OBJECTS LINKED BEFORE RUNTIME---------\n')

    # Here we are writing the rest of the shared objects.
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

# This is a function just to make sure we delete the directory in /tmp before we
# finish since these files can be quite large
def finish(dirName):
    try:
        shutil.rmtree(dirName)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    exit()

# This is the main function. It is primarily responsible for the flow of the
# program by grabbing information, creating files and running strace. All of the
# I/O is in seperate functions.
def main():
    # Should be running as root or with sudo
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
    dirName = '/tmp/tracer' + datetime.datetime.now().strftime(
                              "%Y%m%d%H%M%S") + '/'
    try:
        os.mkdir(dirName)
    except FileExistsError:
        print("Error, directory " + dirName + " already exists")
        finish(dirName)

    proc = os.popen('ps -ef', 'r')
    processes = proc.readlines()
    for line in processes[1:-2]:
        words = line.split()
        if words[7][0] != '[':
            pidlist.append(words[1])
    # We build our list of shared objects
    maplist = getSOMaps(pidlist)
    # execute the strace program for each PID, catching all processes
    cmd = "timeout -k 2 " + sys.argv[1] + " strace -q -ff -ttt -o " + dirName + "TraceCallRaw.txt"
    print("Beginning tracing of processes")
    for pid in pidlist:
        cmd = cmd + " -p " + str(pid)
    # Here we redirect the output from stderr to stdout
    cmd = cmd + " 2>&1"
    out = os.popen(cmd)

    # Here we wait for the strace to finish. We add 2 incase a strace hangs the
    # terminal and we have to force kill it
    time.sleep(int(sys.argv[1]) + 2)
    resultFold = 'TraceResults-' + datetime.datetime.now().strftime(
                              "%Y%m%d%H%M%S") + '/'
    try:
        os.mkdir(resultFold)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        finish(dirName)

    print("Tracing complete, generating summaries to " + resultFold)
    # Now we write all our information to files
    writeSummary(processes, dirName, resultFold)
    writeRawData(dirName, resultFold)
    writeMaps(maplist, processes, resultFold)
    print("Program complete")

    finish(dirName)

if __name__ == '__main__':
    main()
