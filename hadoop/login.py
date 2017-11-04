#!/usr/bin/python

import cgi


data=cgi.FIeldStorage()

usr=data.getvalue('usr')
pas=data.getvalue('pass')
print   "content-type:text/html \r\n\r\n"

print "<h2>htgujft: %r</h2>"%usr
print "<h2>htgujft: %r</h2>"%pas

