#!/usr/bin/python

import  cgi,cgitb,os,time,commands,sys
cgitb.enable()
print  "content-type:text/html"
print  ""

x=cgi.FieldStorage()
#download hive

commands.getoutput("sudo -i wget http://192.168.122.1/hive/apache-hive-1.2.1-bin.tar.gz -P /root/Desktop/a/")

#extract hive
commands.getoutput("sudo -i tar -xvzf /root/Desktop/a/apache-hive-1.2.1-bin.tar.gz -C /root/Desktop/a/")

#copy in / location
commands.getoutput("sudo -i mv /root/Desktop/a/apache-hive-1.2.1-bin /hive1")

#set in path in /root/.bashrc
commands.getoutput("sudo -i chmod 777 /root/.bashrc")
f=open("/root/.bashrc","w")
s="# .bashrc\n\n# User specific aliases and functions\nalias rm='rm -i'\nalias cp='cp -i'\nalias mv='mv -i'\n# Source global definitions\nif [ -f /etc/bashrc ]; then\n    . /etc/bashrc\nfi\nJAVA_HOME=/usr/java/jdk1.7.0_79\nHIVE_PREFIX=/hive1\nPATH=$JAVA_HOME/bin:$HIVE_PREFIX/bin:$PATH\nexport PATH\n"
f.write(s)
f.close()







