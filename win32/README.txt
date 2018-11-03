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

Each folder will contain several files, including a ‘raw.pml’ which contains raw-unreadable information, an ‘output.csv’ which contains all the captured data in a comma separated value style output, and a ‘statistics.txt’ which contains an overview of all calls and accompanying DLLs.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

BUGS:
Occasionally I got a bug where the DLL output method would just freeze for no reason. While trying to debug this the problem went away.
For now, I've added some debug output in the form of some work in progress dots. The output should hopefully look something like this:
> Capturing all calls...
>
> list dlls start: 2018-11-03 12:33:33.543341
> .
> ..
> None
> ...
> list dlls end :  2018-11-03 12:33:44.879626
If the output sits for longer than 5 or 10 seconds on the first single dot, then something has gone wrong somewhere, somehow, and the process must be manually killed before the program will continue. Via Windows Task Manager, look for a process called 'ListDlls.exe' and/or 'ListDlls64.exe' and end the task.
(Note: the 'None' indicates no errors running the ListDlls applet)

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Authors Notes:
The statistics output is not sorted by PID at this time. They are listed in the order that they appear in the RAW output and the CSV output. I am not sure if this is an issue at this time, but I did not think it necessary or worth the extra in-program time/cycles.
The way it is now, it can sometimes take longer than the allotted wait time (ie 10 seconds) as getting the DLL information can sometimes take more time than it needs, leading to a delay and extra wait. Tried to get around this with a custom timer.

Probably should have given this program a better name. In hindsight the "portmanteau" of 'tracer' and 'process monitor' isn't very sexy.

Because of the way windows is compared to Linux, it was initially difficult to get this project off the ground. Linux has a very well put-together system in the form of strace (and its variants). Windows does not have any of this native functionality. As I was given the honour of working on the Windows solution on my own, I went out to try to find a prepackaged solution, in the vein of strace. These solutions technically did exist in the form of NTtrace [http://www.howzatt.demon.co.uk/NtTrace/], straceNT [http://intellectualheaven.com/default.asp?BH=StraceNT], DrMemory [http://www.drmemory.org], plus a couple of others. However, none of these solutions was the magic cure-all for what I needed. They didn't work, crashes on startup, crashed the traced program, or whatever else. 
I happened on my current solution after dismissing it earlier. Microsoft’s ‘Process Monitor’ is a beautiful GUI based program that captures calls made by the system and displays them for you in a nice little package. This was not what I was looking for however, needing a streamlined CLI-style implementation. Eventually, I learned that it could be run in a minimal fashion and its contents output in just the right way with some command line trickery.
With the gift of hindsight, I would have taken a much different approach to this project. While there is no perfect Windows solution, a DIY solution would likely have been possible given various Microsoft debugging tools and many hours of reading, debugging and possibly reverse-engineering of the Ntdll.dll among other things.

After tweaking and testing I have realised a misstep I have taken, I am only checking for DLL usage at the start of the application running. For an extended run, with things being open and accessed in teh background, more DLLs and other applications may be loaded, and this is not taken into account.
In a future revision of this application, I would run this at the start (as it is now) and at the end, and during also, giving you a good safety net of all things running.

I hope the solution that I have come up with will suit the short term needs of the client.


-Timothy