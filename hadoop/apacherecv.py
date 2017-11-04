#!/usr/bin/python

import cgi

print "Content-type:text/html\r\n\r\n"

data=cgi.FieldStorage()

user=data.getvalue("x")
pas=data.getvalue("y")

print user
print pas
