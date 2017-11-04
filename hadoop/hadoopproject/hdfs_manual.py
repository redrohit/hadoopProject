#!/usr/bin/python

import  cgi,cgitb,os,time,commands,sys,ast,numpy
cgitb.enable()
print  "content-type:text/html"
print  ""

x=cgi.FieldStorage()
#  here  setup  choice  will store 

ip_list=["192.168.122.248","192.168.122.125","192.168.122.186"]

ip_listing=[]

cpu_check="lscpu   |  grep -i 'CPU(s):'   |   head  -1  |  cut -d:   -f2"
mem_check="cat /proc/meminfo | grep -i MemFree:"

for i in ip_list:
	
	check=commands.getstatusoutput('ping  -c 1 '+i)
	if  check[0] ==  0  :
	
		ip_listing.append(i)


print  "<html>"
print  "<head>"
print  "<title>Own SuperComputer</title>"
print  "</head>"
print  "<body bgcolor='BLUE'>"
print  "<marquee style='font-size: 200%;margin:20px;color:CYAN;'> Welcome to HDFS manual setup </marquee>"
print  "<br/>"
print  "<br/>"
print  "<form  action='http://192.168.122.1/cgi-bin/hadoopproject/hdfs_directory.py' method='POST'>"
print  "<fieldset style='background-color:CYAN;margin:20px;padding:30px;'>"
print  "<legend style='font-size: 200%;color:YELLOW;font-family: \'Raleway\', sans-serif;' >Select anyone IP for NAMENODE</legend>"
for i   in  ip_listing:
	ignore_exit_value, cpu_core=commands.getstatusoutput('sudo -i sshpass -p "r" ssh -o StrictHostKeyChecking=no root@'+i+" "+cpu_check)
	cpu=cpu_core.strip()
			
	ignore1,memory_value=commands.getstatusoutput('sudo -i sshpass -p "r" ssh root@'+i+" "+mem_check)
	
	mem=memory_value.replace(" ","")
	mem_strip=mem.lstrip("MemFree:")
	mem_rstrip=mem_strip.rstrip("kB")
			

	print  "<input  type='radio' name='setup' value="+i+" >"+i +"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" +"RAM= "+mem_strip +"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" +"CPU core= "+cpu+ "<br/>"
	print  "<br/>"
	print  "<br/>"
for element in ip_listing:
	print '<input type="hidden" name="my_list" value="%s">' % (cgi.escape(element),)
print '<input type="submit" name="submit" value="Submit" />'
print "</fieldset>"
print "</form>"

print  "</body>"
print  "</html>"
