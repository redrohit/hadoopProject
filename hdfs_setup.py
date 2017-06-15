#!/usr/bin/python2

import  os,time,commands,sys,socket

options="""
Press   1   to  manual setup  hadoop  Cluster  :
Press   2   to  automatic setup  hadoop  Cluster  :
"""
print  options

# ch  for storing options
ch=raw_input()

if   ch  ==  '1' :
	

elif  ch ==  '2'  :
	

else   :
	print   "bad choice   "
	#switch the previous page
	time.sleep(2)
	execfile('menu.py')
