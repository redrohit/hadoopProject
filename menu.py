#!/usr/bin/python2

import  os,time,commands,sys,socket

options="""
press  1  to  setup  Hadoop Cluster  :
press  2  to  setup  MR  :
press  3  to  setup  HIVE    :
"""
print   options 
#   ch  for  storing  options  
ch=raw_input()

if  ch  ==  '1' :
	print   "Nice  choice  lets  start  process  "
	time.sleep(1)
	#switch the hdfs_setup process
	execfile('hdfs_setup.py')


elif   ch  ==  '2' :
	print   "make sure  you have enough  Amount to CPU cores "
	time.sleep(1)
	#switch the mr_setup process
	#execfile('mr_setup.py')

elif   ch ==  '3'  :
	print   "lets  start  the  setup  HIVE  "
	time.sleep(1)
	#switch the hive_setup process
	#execfile('hive_setup.py')

else  :
	print  "wrong  option"
	time.sleep(1)
	#switch the previous page
	execfile('startpr.py')


