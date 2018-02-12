import cv2
import urllib2
import numpy as np
import sys
host = "192.168.1.85:8080"
if len(sys.argv)>1:
    host = sys.argv[1]
hoststr = 'http://' + host + '/?action=stream'
print 'Streaming ' + hoststr

print 'Print Esc to quit'
stream=urllib2.urlopen(hoststr)
bytes=''
while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        #flags = 1 for color image
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),flags=1)
        print i
        cv2.imshow("xiaorun",i)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    exit(0)