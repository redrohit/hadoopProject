#!/usr/bin/python2

import   commands,time


ip_list=[]
#It differ from network to network
ipaddr="192.168.10."

#range of ip address
for  i  in   range(121)[-21:]  :
	check=commands.getstatusoutput('ping  -c 1 192.168.10.'+str(i))
	if  check[0] ==  0  :
		ip_list.append(ipaddr+str(i))
	else  :
		print    "IP  Address  "+str(i) + " undefined "

#print the ip which is reachable
print   "scanned  IP    "
time.sleep(2)
print   ip_list

#  checking  cpu core
cpu_ip=[]
cpu_check="lscpu   |  grep -i 'CPU(s):'   |   head  -1  |  cut -d:   -f2"

#  checking memory
mem_check="cat /proc/meminfo | grep -i MemTotal:"

#  extract information which ip is scanned 
for i   in  ip_list:
	#cpu check without entering password of each scanned ip
	ignore_exit_value, cpu_core=commands.getstatusoutput('sshpass -p "redhat" ssh root@'+i+" "+cpu_check)
	cpu=cpu_core.strip()
	
	#memory check without entering of each scanned ip
	ignore1,memory_value=commands.getstatusoutput('sshpass -p "redhat" ssh root@'+i+" "+mem_check)
	
	mem=memory_value.replace(" ","")
	cpu_ip.append("[   IP="+i+"   ,   "+"CPU="+cpu+"   ,   "+"Memory="+mem+"]   ")

#Assigning each cpu information
system_information=cpu_ip[:]
for all_info in system_information:
	print   all_info
