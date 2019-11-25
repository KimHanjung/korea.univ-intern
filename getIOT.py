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

########################################################################################################################################################
global links 
links = []


f = open("links_cpp.txt", "r")

#get the links which used on hashing.py
for i in f:
    translation_table = dict.fromkeys(map(ord, '\n'), None)
    i = i.translate(translation_table)
    links.append(i)

f.close()
    
print("------------------------------------------")
location = []
sourcePath = "/home/hanjung/intern/files/"


for i in links: # scrapping repos at github search api 
    print(i)

hcnt=0
f = open("IOTCUBE_2.txt", "w")

odd = 0

for i in links:         
    odd += 1
    if (odd <= 150):
            hcnt+= 1
            print(hcnt)
    elif (odd <= 300): # odd%4==0 : IOTCUBE_1 / odd%4==1 : IOTCUBE_2 / odd%4==2 : IOTCUBE_3 / odd%4==2 : IOTCUBE_4
        source = sourcePath + i.split('/')[4]
        name = i.split('/')[4]
        context = getCVE(name)
        context = context.json()        
        f.write(str(context) + '\n')
        hcnt +=1
        print(hcnt)
    else:
            break

f.close()
