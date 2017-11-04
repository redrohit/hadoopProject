#!/usr/bin/python

import  cgi,cgitb,os,time,commands,sys,ast,numpy,random
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
cpu_check="lscpu   |  grep -i 'CPU(s):'   |   head  -1  |  cut -d:   -f2"
mem_check="cat /proc/meminfo | grep -i MemFree:"
	
commands.getoutput("sudo -i touch /var/www/cgi-bin/hdfs-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/hdfs-site.xml")

#generate random variable
r=random.randint(1,1000)
file1=open("/var/www/cgi-bin/hdfs-site.xml","w+")
s1="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>"+"/"+"directory"+str(r)+"</value>\n</property>\n</configuration>"
file1.write(s1)
file1.close()

commands.getoutput("sudo -i touch /var/www/cgi-bin/core-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/core-site.xml")


file2=open("/var/www/cgi-bin/core-site.xml","w+")
s2="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://ipaddr:10001</value>\n</property>\n</configuration>"
file2.write(s2)
file2.close()

commands.getoutput("sudo -i touch /var/www/cgi-bin/mapred-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/mapred-site.xml")

file3=open("/var/www/cgi-bin/mapred-site.xml","w+")
s3="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n\n</configuration>"
file3.write(s3)
file3.close()

# remote login in systems and extracting information about  CPU core and FREE memory size of RAM
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





############################################################### NAMENODE ############################################################################

namenode=sort_F_ram_ip[0]


if namenode in sort_F_ram_ip:
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
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop namenode -format")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"jps")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop-daemon.sh start namenode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"jps")
#--------------------------------- DATANODE ------------------------------



index=[]
if namenode in ip_listing:

	n_index=ip_listing.index(namenode)
	index.append(n_index)
		
new_ip_list=numpy.delete(ip_listing,index).tolist()
	
datanodes=new_ip_list

for dn_ip in datanodes:
	s=random.randint(1,1000)
	commands.getoutput("sudo -i sshpass -p 'r' scp /var/www/cgi-bin/core-site.xml root@"+dn_ip+":/etc/hadoop/")
	
	commands.getoutput("sudo -i sshpass -p 'r' scp /var/www/cgi-bin/hdfs-site.xml root@"+dn_ip+":/etc/hadoop/")

	commands.getoutput("sudo -i sshpass -p 'r' scp /var/www/cgi-bin/mapred-site.xml root@"+dn_ip+":/etc/hadoop/")

	#commands.getoutput("sudo -i sshpass -p 'r' scp /root/.bashrc root@"+dn_ip+":/root/")
	#commands.getoutput("sudo -i sshpass -p 'r' scp /root/jack.txt root@+"dn_ip+":/root/")
	
	commands.getoutput("sudo -i sshpass -p 'r' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/ipaddr/'+namenode+"/"+"\" /etc/hadoop/core-site.xml\'")
	commands.getoutput("sudo -i sshpass -p 'r' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/dfs.name.dir/dfs.data.dir/'+"\""+" /etc/hadoop/hdfs-site.xml\'")
	
	commands.getoutput("sudo -i sshpass -p 'r' ssh -o StrictHostKeyChecking=no root@"+dn_ip+" "+'\'sed -i \"s/directory/'+"number"+str(s)+"/"+"\" /etc/hadoop/hdfs-site.xml\'")

	#start the datanode service
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"iptables -F")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"setenforce 0")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh stop jobtracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh stop tasktracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh stop namenode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh stop datanode")
	
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"/usr/java/jdk1.7.0_79/bin/jps")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh start datanode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"/usr/java/jdk1.7.0_79/bin/jps")
	#commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"time.sleep(1)")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip)

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
print  "<legend style='font-size: 200%;color:YELLOW;font-family: \'Raleway\', sans-serif;' >Your HDFS Cluster is ready now</legend>"
print "<h3 style='color:green'>IP with Memory</h3>"
'''
for i   in  ip_listing:		
	ignore1,memory_value=commands.getstatusoutput('sudo -i sshpass -p "r" ssh root@'+i+" "+mem_check)
	
	mem=memory_value.replace(" ","")
	mem_strip=mem.lstrip("MemFree:")
	mem_rstrip=mem_strip.rstrip("kB")
	print  i+"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"+mem_strip
	print  "<br/>"
print  "<br/>"
print  "<br/>"
'''
for i   in  sort_F_ram_ip:
	print i
	
print "<h3 style='color:green'>NameNode</h3>"
print  namenode
print "</br>"
print "</br>"
print "<h3 style='color:green'>DataNodes</h3>"
for dn_ip in datanodes:
	print dn_ip+"</br>"
print "</br>"
print '<input type="hidden" name="my_list" value="%s">' % (cgi.escape(namenode),)
#for element in namenode:
	#print '<input type="hidden" name="my_list" value="%s">' % (cgi.escape(element),)
print '<input style="margin-left:450px;background-color:green;color:CYAN;padding:10px;font-size:30px;cursor: pointer;" type="submit" name="submit" value="Click Here To See the Cluster" />'
print "</fieldset>"
print "</form>"
print  "</body>"
print  "</html>"
