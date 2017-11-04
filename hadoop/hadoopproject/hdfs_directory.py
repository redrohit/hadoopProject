#!/usr/bin/python

import  cgi,cgitb,os,time,commands,sys,numpy,ast
cgitb.enable()
print  "content-type:text/html"
print  ""

x=cgi.FieldStorage()
#  here  setup  choice  will store 

choice=x.getvalue('setup')

all_ip=x.getlist('my_list')

index1=[]


if choice in all_ip:


	n_index=all_ip.index(choice)
	index1.append(n_index)
	

new_ip_list=numpy.delete(all_ip,index1).tolist()

datanodes=new_ip_list

print  "<html>"
print  "<head>"
print  "<title>Own SuperComputer</title>"
print  "</head>"
print  "<body bgcolor='BLUE'>"
print  "<marquee style='font-size: 200%;margin:20px;color:CYAN;'> Welcome to HDFS manual setup </marquee>"
print  "<br/>"
print  "<br/>"

print  "<form  action='http://192.168.122.1/cgi-bin/hadoopproject/hdfs_namenode.py' method='POST'>"
print  "<fieldset style='background-color:CYAN;margin:20px;padding:30px;'>"
print  "<legend style='font-size: 200%;color:YELLOW;font-family: \'Raleway\', sans-serif;' >Enter directory name for Namenode</legend>"
print  "<div style='padding-left:400px;'>"
print  "<input  type='radio' name='nnip' checked='checked' value="+choice+" >"+choice
for element in datanodes:
	print '<input type="hidden" name="my_list" value="%s">' % (cgi.escape(element),)

print "<br/>"
print "<br/>"
print "Directory:"
print "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"
print "<input  type='text' name='dirname' placeholder='enter directory name here'  required>   <br/><br/>"
print  "<input  type='submit' value='send'>"
print  "</div>"
print "</fieldset>"
print "</form >"
print  "</body>"
print  "</html>"
