# CyberSecurityProject
2018 Curtin Cybersecurity Project

Authors: Liam Pilling, Jabob Boland, Timothy Covich
Last Date Modified: 08/11/2018

linuxTracer.py - This program is designed to capture all of the system calls that take place on a linux system using strace. The program relies on strace to capture the output and then the program analyses the output. The program also grabs all of the shared objects that are mapped to processes and outputs that information too. It generates three files:
    - MapSummary.txt: contains all of the shared objects linked to each
                      process.
    - TraceCallRaw.txt: contains all the raw system call data sorted by
                      timestamp.
    - TraceCallSummary.txt: contains a summary of the system calls that
                      occured, sorted by process. This summary contains the system calls that the process made and how many that happened.
