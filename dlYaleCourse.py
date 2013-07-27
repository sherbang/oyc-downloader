#!/usr/bin/python
import httplib
import re
import sys

sessions_page = sys.argv[1]

oyc = 'oyc.yale.edu'; 
openmedia = 'openmedia.yale.edu'

def readPage(domain, pageURL, headers=None):
    cxn = httplib.HTTPConnection(domain)
    if headers: 
        cxn.request('GET', pageURL, headers=headers)
    else:
        cxn.request('GET', pageURL)
    resp = cxn.getresponse()
    cxn.close();
    page = resp.read()
    return page

course = readPage(oyc, sessions_page)
lectureURLs = re.findall("href=\"(.*lecture.*)\"", course)

for lectureURL in lectureURLs:
    lecture = readPage(oyc, lectureURL)
    mp3URLs = re.findall("href=\"([^\"]*?mp3)\"", lecture)
    for mp3FullURL in mp3URLs:
        print mp3FullURL
        if(re.match(".*yale\.edu.*", mp3FullURL) == None):
            print "Not downloading"
            continue
        m = re.match(".*file=.*/(.*?\.mp3)", mp3FullURL)
        mp3FileName =  m.group(1)
        
        m = re.match(".*yale.edu(/.*?\.mp3)", mp3FullURL)
        mp3URL =  m.group(1)
        print "reading %s" % mp3URL
        headers = {'Referer':"http://" + oyc + lectureURL}
        mp3 = readPage(openmedia, mp3URL, headers)
        mp3File = file(mp3FileName, "w")
        mp3File.write(mp3)
        print "writing to  %s" % mp3FileName
