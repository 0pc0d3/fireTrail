#!/usr/bin/python

import smtplib

print "+++++++++++++++++++++++"
print "Sending Notification..."
print "+++++++++++++++++++++++\n\n"

#Load SF Notification Message
sfnotifybuf = open("sfNotify","rb").read()
sfnotify = sfnotifybuf.splitlines()

#Load ET Notification Message
with open ("etNotify", "r") as etfile:
    strETNotify=etfile.read().replace('\n', '<br>')

#Parse SF Notification Message into tables
strSFNotify=""

for item in sfnotify:
        sItem = ''.join(item)
        entry = sItem.split("\t")
        strSFNotify += '<tr>'
        for cel in entry:
                sCel = ''.join(cel)
                td = '<td>' + sCel + '</td>'
                strSFNotify += td
        strSFNotify += '</tr>'


#Setup E-mail
sender = '0pc0d3@github.com'
receivers = ['0pc0d3@github.com','0x0pc0d3gmail.com']
message = """From: 0pc0d3 <0pc0d3@github.com>
To: 0pc0d3 <0pc0d3@github.com>
MIME-Version: 1.0
Content-type: text/html
Subject: FireTrail Notification

<html>
<head>
<style>
td {font-size: 75%;}
th {font-size: 75%;}
table, th, td {
    border: 1px solid black;
}

</style>
</head>
<body>

<b>DO NOT REPLY</b> <br><br>

New signatures are available for selected <b>Key Words</b> monitored by FireTrail.
<br><br>
Sourcefire:
<br><br>

<table>
<thead>
                         <tr><th rowspan="2">Keyword</th><th rowspan="2">GID</th><th rowspan="2">SID</th><th rowspan="2">Rule Group</th><th rowspan="2">Rule Message</th><th colspan="3">Policy State</th></tr>
                         <tr><th>Con.</th><th>Bal.</th><th>Sec.</th></tr>
                 </thead>
<tbody>

"""

mid = """</tbody></table><br><br> ET Ruleset: <br><br>"""
closing ="""<br><br></body></html>"""

#Send E-mail
try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message+strSFNotify+mid+strETNotify+closing) 
   print "***Successfully sent email"
except SMTPException:
   print "Error: unable to send email"

