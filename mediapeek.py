#!/usr/bin/python

import re
import sys
import urllib2

def parse(file):
  result=[]
  entry=None
  for line in file:
    line = line.rstrip()
    headMatcher = re.match('^#EXTM3U$', line)
    valueMatcher = re.match( '^#([^\:]+):?(.*)$', line)
    if headMatcher is not None:
      pass
    elif valueMatcher is not None:
      entry={}
      entry['type']=valueMatcher.group(1)
      entry['params']=valueMatcher.group(2)
      result.append(entry)
    else:
      entry['data']=line
      entry={}
  return result 

response = urllib2.urlopen(sys.argv[2])
outputFileName = sys.argv[1]
master = parse(response)

def urlByRez(master):
  for entry in master:
    if re.match('.*RESOLUTION=960x540.*', entry['params']) is not None:
      return entry['data']

  return None

def download(outputFileName, child):
  with open(outputFileName, 'wb') as outfile:
    for entry in child:
      if entry['type'] == 'EXTINF':
        url = entry['data']
        print('downloading ' + url)
        fragment = urllib2.urlopen(url).read()
        outfile.write(fragment)

print(master)
childUrl = urlByRez(master)
child = parse(urllib2.urlopen(childUrl))
download(outputFileName, child)

