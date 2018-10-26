TRACERMON
--------------------

The goal of this application is to gather information about the system, and the calls it is making in the background unbeknown to the user. It will output captured information into several formats, inducing a human readable format.

To use the WINDOWS portion of this project, you will need to be running a command prompt with elevated privileges.
You will need to either have set your python 3 executable path already, or to point toward the python 3 executable yourself manually.
EG:
$> python3 tracermon.py
$> “C:\Program Files x86\Python 3\python3.exe” tracermon.py

Furthermore, you can give the program a custom run-time
EG:
$> python3 tracermon.py 30
In which the program will collect information for thirty seconds, before processing.

Once the application has run its course, you can find all the information from the capture in organised folders within the “working” directory. They are sorted in a ISO 8601-style standard (YEAR-MONTH-DAY-HOUR-MINUTE-SECOND) into folders, so you should always be able to find your latest output.

Each folder will contain several files, including a ‘raw.pml’ which contains raw-unreadable information, a ‘output.csv’ which contains all the captured data in a comma separated value style output, and a ‘statistics.txt’ which contains an overview of all calls and accompanying DLLs.

-Timothy