@echo off

set message=10648

> app_dlls.txt (
#echo Checking your system infor, Please wating...

echo APP: %1
echo PID: %2
Listdlls.exe %2

)


>> app_trace.txt (

echo APP: %1
echo PID: %2
NtTrace.exe %2

)
