# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 14:04:09 2018

Multi-platform python starter.
 Run this file and it will chose which script to run based on OS.
  Currently only the Windows implementation is setup, but the linux will be soon ;)

@author: Timothy
"""

import platform

print( platform.system() )

platf0rm = platform.system()

if( platf0rm == "Windows"):
    import win32.tracermon as win
    win.main()
elif( platf0rm == "Linux"):
    import linuxTracer as linux
    linux.main()
else:
    print("You are trying to run this application on an operating system that is not currently supported. Exiting...")
