# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 14:04:09 2018

@author: Timothy
"""

import platform

import tracermon as tim
#import linuxtracer as liam


print(platform.system())

platf0rm = platform.system()

if( platf0rm == "Windows"):
    tim.main()
elif( platf0rm == "Linux"):
    print("do liam func here :)")
else:
    print("You are trying to run this application on an operating system that is not currently supported. Exiting...")
