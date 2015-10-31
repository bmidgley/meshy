#!/usr/bin/env python

import json
import urllib2
import csv
import datetime
import os
from gps import *
import threading

import grovepi
from grove_rgb_lcd import *

# also see /var/run/services_olsr

hostfile = '/var/run/hosts_olsr'
logfile = '/home/pi/meshy/log'
buzzer_pin = 8
gpsd = None

setText('')
setRGB(0,0,0)
grovepi.pinMode(buzzer_pin, "OUTPUT")

hosts = dict()

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd
    gpsd = gps(mode=WATCH_ENABLE)
    self.current_value = None
    self.running = True

  def run(self):
    global gpsd
    while self.running:
      gpsd.next()

def merge_hosts(file):
  if os.path.isfile(file):
    for host in list(csv.reader(open(file, 'rb'), delimiter='\t')):
      if len(host) > 1:
        hosts[host[0]] = host[1]

merge_hosts(logfile)
for ip,name in hosts.items():
  print "%s\t%s" % (name,ip)

gpsp = GpsPoller()
gpsp.start()

try:
  while True:
    grovepi.digitalWrite(buzzer_pin, 0)
    time.sleep(3)
    text = ""

    text += ["0","-","~","+"][gpsd.fix.mode]
    text += datetime.datetime.now().strftime("%H:%M ")

    links = json.load(urllib2.urlopen('http://localhost:9090/links'))['links']
    sorted_links = sorted(links, key=lambda link: -link['linkQuality'])
    if len(links) > 0:
      setRGB(255,255,255)
      grovepi.digitalWrite(buzzer_pin, 1)
      time.sleep(0.01 + sorted_links[0]['linkQuality'])
      grovepi.digitalWrite(buzzer_pin, 0)
    else:
      setRGB(20,0,0)

    merge_hosts(logfile)
    merge_hosts(hostfile)

    for link in sorted_links:
      remoteIP = link['remoteIP']
      quality = link['linkQuality']
      name = hosts.get(remoteIP, remoteIP)
      text += "%s " % (name)
      with open(logfile, 'a') as log:
        status = "%s\t%s\t#\t%s\t%f" % (remoteIP, name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), quality)
        if gpsd.fix.mode > 1:
          status += "\t%f\t%f" % (gpsd.fix.latitude, gpsd.fix.longitude)
        print status
        status += "\n"
        log.write(status)
      os.system("sync")

    setText(text)

except (KeyboardInterrupt, SystemExit):
  gpsp.running = False
  gpsp.join()
