from urllib.request import urlopen
from bs4 import BeautifulSoup
from operator import itemgetter
from collections import OrderedDict
import os, requests, zipfile, io, time 

def checkFile(path):
    test = os.popen("ls " + path).read()
    global files
    files = []
    tmp =''
    for c in test:
        if c=='\n':
            files.append(tmp)
            tmp = ''
        else:
            tmp+=c

def ready(page):
    time.sleep(10)
    params = (
        ('page', page),
        ('q', 'language:c'),
        ('sort', 'stars'),
        ('order', 'desc'),
    )

    response_git = requests.get('https://api.github.com/search/repositories', params=params)
    response_git = response_git.json()

    response_git = response_git["items"]
    for element in response_git:
        links.append(element["html_url"])

def crawling(path): # cloning the git of repos
    time.sleep(10)
    name = path.split('/')[-1]
    html_crawl = urlopen(path + "/releases/latest")  

    bsObject = BeautifulSoup(html_crawl, "html.parser")
    linking = bsObject.find('div', {"class":"repository-content"}).find('h3')

    #if name not in files:
    if linking != None:
        os.system("git clone " + path + ".git files/" + name)
    else:
        linking = bsObject.find("div", {"class":"d-block py-1 py-md-2 Box-body px-2"})
        if linking != None:
            linking = linking.find('a')['href']
        else:
            linking = bsObject.find("a", {"class":"muted-link", "rel":"nofollow"})['href']

        linking = "https://github.com" + linking
        r = requests.get(linking)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall("files/" + name)
        
########################################################################################################################################################
global links 
links = []

for page in range(1,35):
    ready(page)
    
location = []
sourcePath = "/home/hanjung/intern/files/"

f = open("links_c.txt", "w")

for i in links: # scrapping repos at github search api 
    print(i)
    f.write(i + '\n')

f.close()

result = [] # results of info from iotcube
opensource = []

checkFile("/home/hanjung/intern/hidx/")
hcnt=0

for i in links: 
    source = sourcePath + i.split('/')[4]
    name = i.split('/')[4]
    if ("hashmark_0_" + name + ".hidx") not in files:
        crawling(i)
        check = os.popen("find " + source + " -name \"*.c\"").read()
        check += os.popen("find " + source + " -name \"*.cpp\"").read()
        check += os.popen("find " + source + " -name \"*.cc\"").read()
        check += os.popen("find " + source + " -name \"*.c++\"").read()
        if(len(check)!=0):
            os.system("./hmark_3.1.0_linux_x64 -c " + source + " OFF")
        os.system("rm -rf files/" + name)
    else:
        os.system("rm -rf files/" + name)
