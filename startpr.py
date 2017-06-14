#!/usr/bin/python2


import  os,time,commands,sys,socket,getpass

print   "Welcome  To world  of  data  !!"
print   "_______________________________"
print   "_______________________________"
print   "_______________________________"
print   "###############################"
time.sleep(2)

#wrong authentication count
count = 1

#taking username and password for authentication
def login():
	user=raw_input("enter  user name to access project  :  ")
	password=getpass.getpass("enter password  :  ")
	
	if  user  ==  'root' and  password  ==  'redhat' :
		print  "access granted  !!"
		time.sleep(2)
		#switch the menu selection
		execfile('menu.py')
	else   :
		print   "wrong  authentication !!!"
		time.sleep(1)
		print "Do you try again (y/n) : "
		#ch for storing option
		ch=raw_input()
		if ch=='y':
			global count
			count+=1
			if count == 4 :
				print "You have cross the maximum limit!!!"
				time.sleep(1)
				print "Thank you!!!!"				
				time.sleep(2)
				exit()
			login()		
		else:	
			time.sleep(1)
			print "Thank you!!!"		
			exit()
			
			
			
login()
