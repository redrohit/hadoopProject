#!/usr/bin/python
import  cgi,cgitb,os,time,commands,sys,numpy,ast,webbrowser
cgitb.enable()
print  "content-type:text/html"
print  ""

x=cgi.FieldStorage()
#namenode=x.getvalue("nn")
namenode=x.getlist('my_list')
nn= ''.join(namenode)
<a href='open_new_tab.py'>fgbhyg</a>
#webbrowser.open_new_tab(nn+":50070")

'''
commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"iptables -F")
commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"setenforce 0")
commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop-daemon.sh stop jobtracker")
commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop-daemon.sh stop tasktracker")
commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop-daemon.sh stop namenode")
commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop-daemon.sh stop datanode")
commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop namenode -format")
commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+namenode+" "+"hadoop-daemon.sh start namenode")

for datanode in dn_ip:
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+datanode+" "+"iptables -F")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+datanode+" "+"setenforce 0")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+datanode+" "+"hadoop-daemon.sh stop jobtracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+datanode+" "+"hadoop-daemon.sh stop tasktracker")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+datanode+" "+"hadoop-daemon.sh stop namenode")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+datanode+" "+"hadoop-daemon.sh stop datanode")
	#commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+datanode+" "+"hadoop namenode -format")
	commands.getoutput("sudo -i sshpass -p 'r' ssh root@"+datanode+" "+"hadoop-daemon.sh start datanode")
'''
