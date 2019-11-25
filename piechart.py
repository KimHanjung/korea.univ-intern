from urllib.request import urlopen
from bs4 import BeautifulSoup
from operator import itemgetter
from collections import OrderedDict
import os, requests, zipfile, io, time 

def getCVE(name): # request result to iotcube and receive
    time.sleep(5)
    files = {'file': ("/home/hanjung/intern/hidx/hashmark_0_" + name + ".hidx", open("/home/hanjung/intern/hidx/hashmark_0_" + name + ".hidx", 'rb'))}
    headers = {'user-agent': 'your user-agent value'}
    response = requests.post("https://iotcube.net/api/wf1", files=files, headers=headers)
    return response

a = getCVE("linux_raspberrypi")
print(a.json())