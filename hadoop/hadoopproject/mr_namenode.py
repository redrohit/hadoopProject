#!/usr/bin/python

import  cgi,cgitb,os,time,commands,sys
cgitb.enable()
print  "content-type:text/html"
print  ""
x=cgi.FieldStorage()
nn_ip=x.getvalue("nnip")
directory=x.getvalue("dirname")

jobtracker=x.getlist('my_list')





#------------------- NAMENODE--------------------------


commands.getoutput("sudo -i touch /var/www/cgi-bin/hdfs-site.xml")
commands.getoutput("sudo -i chmod 777 /var/www/cgi-bin/hdfs-site.xml")

file1=open("/var/www/cgi-bin/hdfs-site.xml","w")
s1="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\""+"text/xsl\""+" href="+"\"configuration.xsl\""+"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>"+"/"+directory+"</value>\n</property>\n</configuration>"
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

namenode=nn_ip


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

#------------------IP for JOBTRACKER------------------------------

cpu_check="lscpu   |  grep -i 'CPU(s):'   |   head  -1  |  cut -d:   -f2"
mem_check="cat /proc/meminfo | grep -i MemFree:"

print  "<html>"
print  "<head>"
print  "<title>Own SuperComputer</title>"
print  "</head>"
print  "<body bgcolor='BLUE'>"
print  "<marquee style='font-size: 200%;margin:20px;color:CYAN;'> Welcome to MapReduce manual setup </marquee>"
print  "<br/>"
print  "<br/>"
print  "<form  action='http://192.168.122.1/cgi-bin/hadoopproject/mr_jobtracker.py' method='POST'>"
print  "<fieldset style='background-color:CYAN;margin:20px;padding:30px;'>"
print  "<legend style='font-size: 200%;color:YELLOW;font-family: \'Raleway\', sans-serif;' >Select anyone IP for JobTracker</legend>"
for i   in  jobtracker:
	ignore_exit_value, cpu_core=commands.getstatusoutput('sudo -i sshpass -p "q" ssh -o StrictHostKeyChecking=no root@'+i+" "+cpu_check)
	cpu=cpu_core.strip()
			
	ignore1,memory_value=commands.getstatusoutput('sudo -i sshpass -p "q" ssh root@'+i+" "+mem_check)
	
	mem=memory_value.replace(" ","")
	mem_strip=mem.lstrip("MemFree:")
	mem_rstrip=mem_strip.rstrip("kB")
	print  "<input  type='radio' name='setup' value="+i+" >"+i +"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" +"RAM= "+mem_strip +"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" +"CPU core= "+cpu+ "<br/>"
	print  "<br/>"
	print  "<br/>"
	
#converting string to list
nn=namenode.split(' ')	
for element in nn:
	print '<input type="hidden" name="nn" value="%s">' % (cgi.escape(element),)
	
		
	
for element1 in jobtracker:
	print '<input type="hidden" name="my_list" value="%s">' % (cgi.escape(element1),)
print '<input type="submit" name="submit" value="Submit" />'
print "</form>"
print "</fieldset>"
print "</form>"

print  "</body>"
print  "</html>"
