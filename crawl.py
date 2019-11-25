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
    time.sleep(5)
    params = (
        ('page', page),
        ('q', 'language:c++'),
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

def getCVE(name): # request result to iotcube and receive
    time.sleep(10)
    files = {'file': ("/home/hanjung/intern/hidx/hashmark_0_" + name + ".hidx", open("/home/hanjung/intern/hidx/hashmark_0_" + name + ".hidx", 'rb'))}
    headers = {'user-agent': 'your user-agent value'}
    response = requests.post("https://iotcube.net/api/wf1", files=files, headers=headers)
    return response

########################################################################################################################################################
global links 
links = []

for page in range(1,11):
    ready(page)
    
location = []
sourcePath = "/home/hanjung/intern/files/"


for i in links: # scrapping repos at github search api 
    print(i)

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
            if "freebsd" not in name:
                os.system("./hmark_3.1.0_linux_x64 -c " + source + " OFF")
                print(name + " Is not here")
            opensource.append({'name':name})
            result.append(getCVE(name))
        os.system("rm -rf files/" + name)
    else:
        os.system("rm -rf files/" + name)
        hcnt+=1
        opensource.append({'name':name})
        result.append(getCVE(name))

cve_list = {}
index = 0
for i in result: # processing the 
    js = i.json()
    count = js[0]['total_cve']
    opensource[index]["high"] = {}
    opensource[index]["middle"] = {}
    opensource[index]["low"] = {}
    num_cve = 0
    for j in range(1,count+1):
        cve = js[j]['cveid']
        cvss = float(js[j]['cvss'])
        if cvss < 4:
            vul = "low"
        elif cvss < 7:
            vul = "middle"
        else:
            vul = "high"

        if cve not in opensource[index][vul]:
            opensource[index][vul][cve] = 1
            num_cve += 1
        else:
            opensource[index][vul][cve] += 1

        if cve not in cve_list:
            cve_list[cve] = [1, opensource[index]['name']]
        else:
            #cve_list[cve][0] += 1
            if opensource[index]['name'] not in cve_list[cve]:
                cve_list[cve][0] += 1
                cve_list[cve].append(opensource[index]['name'])
        
    opensource[index]['total_cve'] = num_cve
    index += 1


# make the result file
opensource = sorted(opensource, key=itemgetter('total_cve'), reverse = True) 
o_text = ''
for element in opensource:
    o_text += "open source: " + element['name'] + "\n" + "\t" + "detected CVEs : " + str(element['total_cve']) + "\n"
    for vul in element:
        if vul in ('name', 'total_cve'):
            continue
        o_text += "\t[" + vul + "]\n"
        for cve in element[vul]:
            o_text += "\t\t" + cve + " : " + str(element[vul][cve]) + "\n"
    o_text += "\n"
f = open('opensource.txt', 'w')
f.write(o_text)
f.close()


cve_list = dict(OrderedDict(sorted(cve_list.items(), key=lambda kv: kv[1][0], reverse = True)))
c_text = ''
for element in cve_list:
    c_text += element + "\n"
    for source in cve_list[element]:
        if type(source) == int:
            temp = "\t  ->" + "appearance : " + str(source) + "\n"
        else:
            c_text += "\t" + source + "\n"
    c_text += temp
    c_text += "\n"
f = open('cve_list.txt', 'w')
f.write(c_text)
f.close()
 
print(len(links))
