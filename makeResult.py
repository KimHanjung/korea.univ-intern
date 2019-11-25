from operator import itemgetter
from collections import OrderedDict
from matplotlib import font_manager, rc, style
import requests, io, json
import matplotlib.pyplot as plt
import numpy as np

links = []
sourcePath = "/home/hanjung/intern/files/"

f = open("links_cpp.txt", "r")

#get the links which used on hashing.py
for i in f:
    translation_table = dict.fromkeys(map(ord, '\n'), None)
    i = i.translate(translation_table)
    links.append(i)

f.close()


result = [] # results of info from iotcuber
opensource = []

hcnt=0


f_1 = open("IOTCUBE_1.txt", "r")
f_2 = open("IOTCUBE_2.txt", "r")

odd = 0

for i in links: 
    odd += 1
    if (odd <= 300):
        source = sourcePath + i.split('/')[4]
        name = i.split('/')[4]
        opensource.append({'name':name})

for r in f_1:
    r = r.replace('\'', '\"')
    result.append(json.loads(r))

odd = 0

for r in f_2:
    r = r.replace('\'', '\"')
    result.append(json.loads(r))

f_1.close()
f_2.close()

cwe_list = {}
cve_list = {}
cve_high = []
cve_middle = []
cve_low = []
index = 0

for js in result: # processing the result
    count = js[0]['total_cve']
    opensource[index]["high"] = {}
    opensource[index]["middle"] = {}
    opensource[index]["low"] = {}
    num_cve = 0
    for j in range(1,count+1):
        cve = js[j]['cveid']
        cwe = js[j]['cwe']
        cvss = float(js[j]['cvss'])
        if cvss < 4:
            vul = "low"
            cve_low.append(cve)
            cve = "l_" + cve
        elif cvss < 7:
            vul = "middle"
            cve_middle.append(cve)
            cve = "m_" + cve
        else:
            vul = "high"
            cve_high.append(cve)
            cve = "h_" + cve

        if cve not in opensource[index][vul]:
            opensource[index][vul][cve] = 1
            num_cve += 1
        else:
            opensource[index][vul][cve] += 1

        if cwe not in cwe_list:
            cwe_list[cwe] = [cve]
        else:
            if cve not in cwe_list[cwe]:
                cwe_list[cwe].append(cve)

        if cve not in cve_list:
            cve_list[cve] = [1, opensource[index]['name']]
        else:
            if opensource[index]['name'] not in cve_list[cve]:
                cve_list[cve][0] += 1
                cve_list[cve].append(opensource[index]['name'])
        
    cve_high = list(dict.fromkeys(cve_high))
    cve_middle = list(dict.fromkeys(cve_middle))
    cve_low = list(dict.fromkeys(cve_low))

    opensource[index]['total_cve'] = num_cve
    index += 1

# make the result file
opensource = sorted(opensource, key=itemgetter("total_cve"), reverse = True) 
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
f = open('opensource_cpp.txt', 'w')
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
f = open('cve_list_cpp.txt', 'w')
f.write(c_text)
f.close()
