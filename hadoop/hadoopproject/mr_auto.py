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


cpu_core_ip={}
F_ram_ip={}
	
for i   in  ip_listing:
	ignore_exit_value, cpu_core=commands.getstatusoutput('sudo -i sshpass -p "r" ssh -o StrictHostKeyChecking=no root@'+i+" "+cpu_check)
	cpu=cpu_core.strip()
		
	ignore1,memory_value=commands.getstatusoutput('sudo -i sshpass -p "r" ssh root@'+i+" "+mem_check)
		
	mem=memory_value.replace(" ","")
	mem_strip=mem.lstrip("MemFree:")
	mem_rstrip=mem_strip.rstrip("kB")
	

	x1="{"+"\'"+i+"\'"+":"+mem_rstrip+"}"
	

	y1=ast.literal_eval(x1)


	F_ram_ip.update(y1)


	sort_F_ram_ip=sorted(F_ram_ip,key=F_ram_ip.get,reverse=True)




	x2="{"+"\'"+i+"\'"+":"+cpu+"}"
	

	y2=ast.literal_eval(x2)


	cpu_core_ip.update(y2)

	sort_cpu_core_ip=sorted(cpu_core_ip,key=cpu_core_ip.get,reverse=True)


	

#----------------- NAMENODE --------------------

namenode=sort_F_ram_ip[0]


if namenode in sort_F_ram_ip:

	commands.getoutput("sudo -i touch /var/www/cgi-bin/hdfs-site.xml")
	commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/hdfs-site.xml")

	file1=open("/var/www/cgi-bin/hdfs-site.xml","w")
	s1="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>"+"/"+"directory"+"</value>\n</property>\n</configuration>"
	file1.write(s1)
	file1.close()

	commands.getoutput("sudo -i touch /var/www/cgi-bin/core-site.xml")
	commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/core-site.xml")


	file2=open("/var/www/cgi-bin/core-site.xml","w")
	s2="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://ipaddr:10001</value>\n</property>\n</configuration>"
	file2.write(s2)
	file2.close()


	commands.getoutput("sudo -i touch /var/www/cgi-bin/mapred-site.xml")
	commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/mapred-site.xml")


	file3=open("/var/www/cgi-bin/mapred-site.xml","w")
	s3="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n\n</configuration>"
	file3.write(s3)
	file3.close()




	commands.getoutput("sudo -i sshpass -p 'r' scp /var/www/cgi-bin/hdfs-site.xml root@"+namenode+":/etc/hadoop/")

	commands.getoutput("sudo -i sshpass -p 'r' scp /var/www/cgi-bin/core-site.xml root@"+namenode+":/etc/hadoop/")

	commands.getoutput("sudo -i sshpass -p 'r' scp /var/www/cgi-bin/mapred-site.xml root@"+namenode+":/etc/hadoop/")

		

	
	commands.getoutput("sudo -i sshpass -p 'r' ssh -o StrictHostKeyChecking=no root@"+namenode+" "+'\'sed -i \"s/ipaddr/'+namenode+"/"+"\" /etc/hadoop/core-site.xml\'")
	#start the namenode service
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"iptables -F")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"setenforce 0")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop-daemon.sh stop jobtracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop-daemon.sh stop tasktracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop-daemon.sh stop namenode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop-daemon.sh stop datanode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"jps")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop namenode -format")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop-daemon.sh start namenode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"jps")
	 


#------------------JOBTRACKER ----------------------

index1=[]


if namenode in sort_cpu_core_ip[0]:
	n_index=sort_cpu_core_ip.index(namenode)
	index1.append(n_index)
	

new_ip_list=numpy.delete(sort_cpu_core_ip,index1).tolist()

remaining_ip=new_ip_list


jobtracker=remaining_ip[0]


if jobtracker in remaining_ip:
	commands.getoutput("sudo -i touch /var/www/cgi-bin/mapred-site.xml")
	commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/mapred-site.xml")


	file1=open("/var/www/cgi-bin/mapred-site.xml","w")
	s1="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>jobip:90001</value>\n</property>\n</configuration>"
	file1.write(s1)
	file1.close()


	commands.getoutput("sudo -i touch /var/www/cgi-bin/core-site.xml")
	commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/core-site.xml")


	file2=open("/var/www/cgi-bin/core-site.xml","w")
	s2="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://ipaddr:10001</value>\n</property>\n</configuration>"
	file2.write(s2)
	file2.close()


	commands.getoutput("sudo -i touch /var/www/cgi-bin/hdfs-site.xml")
	commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/hdfs-site.xml")

	file3=open("/var/www/cgi-bin/hdfs-site.xml","w")
	s3="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n</configuration>"
	file3.write(s3)
	file3.close()



	commands.getoutput("sudo -i sshpass -p 'r' scp /var/www/cgi-bin/hdfs-site.xml root@"+jobtracker+":/etc/hadoop/")

	commands.getoutput("sudo -i sshpass -p 'r' scp /var/www/cgi-bin/core-site.xml root@"+jobtracker+":/etc/hadoop/")

	commands.getoutput("sudo -i sshpass -p 'r' scp /var/www/cgi-bin/mapred-site.xml root@"+jobtracker+":/etc/hadoop/")
		

	
	commands.getoutput("sshpass -p 'r' ssh -o StrictHostKeyChecking=no root@"+jobtracker+" "+'\'sed -i \"s/jobip/'+jobtracker+"/"+"\" /etc/hadoop/mapred-site.xml\'")

	commands.getoutput("sshpass -p 'r' ssh -o StrictHostKeyChecking=no root@"+jobtracker+" "+'\'sed -i \"s/ipaddr/'+namenode+"/"+"\" /etc/hadoop/core-site.xml\'")

	#start the jobtracker service
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+jobtracker+" "+"iptables -F")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+jobtracker+" "+"setenforce 0")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+jobtracker+" "+"hadoop-daemon.sh stop jobtracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+jobtracker+" "+"hadoop-daemon.sh stop tasktracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+jobtracker+" "+"hadoop-daemon.sh stop namenode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+jobtracker+" "+"hadoop-daemon.sh stop datanode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+jobtracker+" "+"jps")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+jobtracker+" "+"hadoop-daemon.sh start jobtracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+jobtracker+" "+"jps")
	


#-------------------- DATANODE AND TASKTRACKER ------------------------
s=1

index=[]


if namenode and jobtracker in ip_listing:

	n_index=ip_listing.index(namenode)
	index.append(n_index)
	j_index=ip_listing.index(jobtracker)
	index.append(j_index)

new_ip_list=numpy.delete(ip_listing,index).tolist()

datanodes=new_ip_list
		

		

for dn_ip in datanodes:

	commands.getoutput("sudo -i touch /var/www/cgi-bin/mapred-site.xml")
	commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/mapred-site.xml")


	file1=open("/var/www/cgi-bin/mapred-site.xml","w+")
	s1="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>jobip:90001</value>\n</property>\n</configuration>"
	file1.write(s1)
	file1.close()


	commands.getoutput("sudo -i touch /var/www/cgi-bin/core-site.xml")
	commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/core-site.xml")


	file2=open("/var/www/cgi-bin/core-site.xml","w+")
	s2="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://ipaddr:10001</value>\n</property>\n</configuration>"
	file2.write(s2)
	file2.close()


	commands.getoutput("sudo -i touch /var/www/cgi-bin/hdfs-site.xml")
	commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/hdfs-site.xml")

	file3=open("/var/www/cgi-bin/hdfs-site.xml","w")
	s3="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>"+"/"+"directory"+"</value>\n</property>\n</configuration>"
	file3.write(s3)
	file3.close()




	commands.getoutput("sudo -i sshpass -p 'r' scp /var/www/cgi-bin/hdfs-site.xml root@"+dn_ip+":/etc/hadoop/")
	
	commands.getoutput("sudo -i sshpass -p 'r' scp /var/www/cgi-bin/core-site.xml root@"+dn_ip+":/etc/hadoop/")

	commands.getoutput("sudo -i sshpass -p 'r' scp /var/www/cgi-bin/mapred-site.xml root@"+dn_ip+":/etc/hadoop/")

	
	commands.getoutput("sshpass -p 'r' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/jobip/'+jobtracker+"/"+"\" /etc/hadoop/mapred-site.xml\'")

	commands.getoutput("sshpass -p 'r' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/ipaddr/'+namenode+"/"+"\" /etc/hadoop/core-site.xml\'")

	commands.getoutput("sudo -i sshpass -p 'r' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/dfs.name.dir/dfs.data.dir/'+"\""+" /etc/hadoop/hdfs-site.xml\'")
	
	
	commands.getoutput("sshpass -p 'r' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/directory/'+"number"+str(s)+"/"+"\" /etc/hadoop/hdfs-site.xml\'")

	s=s+1
	#start the datanode and tasktracker service
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"iptables -F")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"setenforce 0")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh stop jobtracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh stop tasktracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh stop namenode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh stop datanode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"jps")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh start datanode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh start tasktracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"jps")
	

#----------------------- x x x x x ---------------------------------

print  "<html>"
print  "<head>"
print  "<title>Own SuperComputer</title>"
print  "</head>"
print  "<body bgcolor='BLUE'>"	
print  "<marquee style='font-size: 200%;margin:20px;color:CYAN;'> Good Job </marquee>"
print  "<br/>"
print  "<br/>"
print  "<form  action='http://192.168.122.1/cgi-bin/hadoopproject/service.py' method='POST'>"
print  "<fieldset style='background-color:CYAN;margin:20px;padding:20px;'>"
print  "<legend style='font-size: 200%;color:YELLOW;font-family: \'Raleway\', sans-serif;' >Your MR Cluster is ready now</legend>"
print "<h3 style='color:green'>IP with Memory</h3>"
'''
for i   in  ip_listing:	
	ignore_exit_value, cpu_core=commands.getstatusoutput('sudo -i sshpass -p "r" ssh -o StrictHostKeyChecking=no root@'+i+" "+cpu_check)
	cpu=cpu_core.strip()	
	ignore1,memory_value=commands.getstatusoutput('sudo -i sshpass -p "r" ssh root@'+i+" "+mem_check)
	
	mem=memory_value.replace(" ","")
	mem_strip=mem.lstrip("MemFree:")
	mem_rstrip=mem_strip.rstrip("kB")
	print  i+"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"+mem_strip+"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"+cpu
	print  "<br/>"
print  "<br/>"
print  "<br/>"
'''
for i   in  sort_F_ram_ip:
	print i
print "</br>"
print "<h3 style='color:green'>IP with CPU</h3>"
for i   in  sort_cpu_core_ip:
	print i
print "</br>"
print "<h3 style='color:green'>NameNode</h3>"
print  namenode
print "</br>"
print "</br>"
print "<h3 style='color:green'>JobTracker</h3>"
print  jobtracker
print "</br>"
print "</br>"
print "<h3 style='color:green'>DataNodes and TaskTracker</h3>"
for dn_ip in datanodes:
	print dn_ip+"</br>"
print "</br>"
for element in datanodes:
	print '<input type="hidden" name="my_list" value="%s">' % (cgi.escape(element),)
print '<input style="margin-left:450px;background-color:green;color:CYAN;padding:10px;font-size:30px;cursor: pointer;" type="submit" name="submit" value="Click Here To See the Cluster" />'
print "</fieldset>"
print "</form>"
print  "</body>"
print  "</html>"

