#!/usr/bin/env python

import json
import urllib2
import csv
import datetime
import os

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

def merge_hosts(file):
  if os.path.isfile(file):
    for host in list(csv.reader(open(file, 'rb'), delimiter='\t')):
      if len(host) > 1:
        hosts[host[0]] = host[1]

while True:
  time.sleep(3)

  text = ""

  try:
    links = json.load(urllib2.urlopen('http://localhost:9090/links'))['links']
    sorted_links = sorted(links, key=lambda link: -link['linkQuality'])
    if len(links) > 0:
      setRGB(255,255,255)
      grovepi.digitalWrite(buzzer_pin, 1)
      time.sleep(0.01 + sorted_links[0]['linkQuality'])
      grovepi.digitalWrite(buzzer_pin, 0)
    else:
      setRGB(0,0,0)

    merge_hosts(logfile)
    merge_hosts(hostfile)

    for link in sorted_links:
      remoteIP = link['remoteIP']
      quality = link['linkQuality']
      name = hosts.get(remoteIP, remoteIP)
      text += "%s " % (name)
      with open(logfile, 'a') as log:
        log.write("%s\t%s\t#\t%s\t%f\n" % (remoteIP, name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), quality))
      os.system("sync")

    setText(text)
  except:
    print "pausing meshy"


