#!/usr/bin/python

import  cgi,cgitb,os,time,commands,sys
cgitb.enable()
print  "content-type:text/html"
print  ""

x=cgi.FieldStorage()
user=x.getvalue('uname')
password=x.getvalue('psw')

if  user  ==  'root'  and  password  == 'redhat' :
	
	print  "<html>"
	print  "<body style='background-color:GREEN;'>"
	print  "<h2 style='text-align:center ; color:WHITE; '>authentication Done  redirecting to new page</h2>"
	print  "<br/>"
	print  "<br/>"
	#print  "<img src='h.jpg'>"
	print  "<meta  http-equiv='refresh' content='2;url=http://192.168.122.1/hadoopproject/select.html'/>"
	print  "</body>"
	print  "</html>"

else  :
	print   "bad  authentication  details !!"
	print  "<meta  http-equiv='refresh' content='2;url=http://192.168.122.1/hadoopproject/login.html'/>"
