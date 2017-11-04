#!/usr/bin/python

import  cgi,cgitb,os,time,commands,sys,numpy,ast
cgitb.enable()
print  "content-type:text/html"
print  ""

x=cgi.FieldStorage()
#  here  setup  choice  will store 

jobtracker=x.getvalue('setup')

all_ip=x.getlist('my_list')

namenode_ip=x.getlist('nn')

#converting list to string(namenode)

namenode =''.join(namenode_ip)



#---------------- JOBTRACKER ----------------------

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

#------------------ DATANODE AND TASKTRACKER ----------------------

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


s=1

index1=[]


if jobtracker in all_ip:


	n_index=all_ip.index(jobtracker)
	index1.append(n_index)
	

new_ip_list=numpy.delete(all_ip,index1).tolist()

data_task=new_ip_list


for dn_ip in data_task:
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
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh stop datanode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh stop namenode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"jps")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh start datanode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"hadoop-daemon.sh start tasktracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+dn_ip+" "+"jps")

#--------------Cluster-----------------
print  "<html>"
print  "<head>"
print  "<title>Own SuperComputer</title>"
print  "</head>"
print  "<body bgcolor='BLUE'>"
print  "<marquee style='font-size: 200%;margin:20px;color:CYAN;'> Good Job</marquee>"
print  "<br/>"
print  "<br/>"	
print  "<form  action='http://192.168.122.1/cgi-bin/hadoopproject/service.py' method='POST'>"
print  "<fieldset style='background-color:CYAN;margin:20px;padding:20px;'>"
print  "<legend style='font-size: 200%;color:YELLOW;font-family: \'Raleway\', sans-serif;' >Your MR Cluster is ready now</legend>"
print  "<br/>"
print "<h3 style='color:green'>NameNode</h3>"
print  namenode
print "</br>"
print "</br>"
print "<h3 style='color:green'>JobTracker</h3>"
print  jobtracker
print "</br>"
print "</br>"
print "<h3 style='color:green'>DataNodes and TaskTrackers</h3>"
for dn_ip in data_task:
	print dn_ip+"</br>"
print "</br>"
for element in data_task:
	print '<input type="hidden" name="my_list" value="%s">' % (cgi.escape(element),)
print '<input style="margin-left:450px;background-color:green;color:CYAN;padding:10px;font-size:30px;cursor: pointer;" type="submit" name="submit" value="Click Here To See the Cluster" />'
print "</fieldset>"
print "</form>"
print  "</body>"
print  "</html>"

