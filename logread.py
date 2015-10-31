#!/usr/bin/env python

import json
import urllib2
import csv
import datetime
import os

# 0             1         2 3          4        5         6         7
# 10.46.184.234 kg7dgh-u2 # 2015-10-25 10:20:33 0.831000  40.435805 -111.790951

logfile = 'log'
hosts = {}

def merge_hosts(file):
  if os.path.isfile(file):
    for host in list(csv.reader(open(file, 'rb'), delimiter='\t')):
      if len(host) > 1:
        hosts[host[0]] = host[1]
      if len(host) > 6 and host[6] != '0.000000':
        print "    <Placemark><name>%s</name><description>%s</description><Point><coordinates>%s,%s,0</coordinates></Point></Placemark>" % (host[1], host[4], host[6], host[5])

#for ip,name in hosts.items():
#  print "%s\t%s" % (name,ip)

print '<?xml version="1.0" encoding="UTF-8"?>'
print '<kml xmlns="http://www.opengis.net/kml/2.2">'
print ' <Document>'
print '  <name>Map of mesh networks</name>'
print '  <open>1</open>'
print '  <description>Map of mesh networks</description>'
print '  <LookAt><longitude>-111.3644</longitude><latitude>39.6181</latitude><altitude>2500</altitude><heading>0</heading><tilt>0</tilt><range>900000</range></LookAt>'
merge_hosts(logfile)
print ' </Document>'
print '</kml>'
