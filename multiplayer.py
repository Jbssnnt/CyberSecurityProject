# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 14:04:09 2018

Multi-platform python starter. 
 Run this file and it will chose which script to run based on OS.
  Currently only the Windows implementation is setup, but the linux will be soon ;)

@author: Timothy
"""

import platform

import win32.tracermon as tim
#import linuxtracer as liam


print( platform.system() )

platf0rm = platform.system()

if( platf0rm == "Windows"):
    tim.main( "multi" )
elif( platf0rm == "Linux"):
    print("do liam func here :)")
    #liam.main()
else:
    print("You are trying to run this application on an operating system that is not currently supported. Exiting...")
