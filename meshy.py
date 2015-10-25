#!/usr/bin/env python

import json
import urllib2
import csv
import os.path

import grovepi
from grove_rgb_lcd import *

# also see /var/run/services_olsr

hostfile = '/var/run/hosts_olsr'
logfile = '/home/pi/meshy/log'
buzzer_pin = 8

setText('')
setRGB(0,0,0)
grovepi.pinMode(buzzer_pin, "OUTPUT")

hosts = dict()

while True:
  time.sleep(3)

  text = ""

  try:
    links = json.load(urllib2.urlopen('http://localhost:9090/links'))['links']
    sorted_links = sorted(links, key=lambda link: -link['linkQuality'])
    if len(links) > 0:
      setRGB(255,255,255)
      grovepi.digitalWrite(buzzer_pin, 1)
      time.sleep(0.01 + sorted_links[0]['linkQuality']/2)
      grovepi.digitalWrite(buzzer_pin, 0)
    else:
      setRGB(0,0,0)

    if os.path.isfile(hostfile):
      for host in list(csv.reader(open(hostfile, 'rb'), delimiter='\t')):
        if len(host) > 1:
          hosts[host[0]] = host[1]

    for link in sorted_links:
      remoteIP = link['remoteIP']
      quality = int(link['linkQuality'] * 10)
      text += ("%s " % (hosts.get(remoteIP, remoteIP)))

    setText(text)
  except:
    print "pausing meshy"


