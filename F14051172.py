#!/usr/bin/python
#-*- encoding: UTF-8 -*-

from collections import OrderedDict
from multiprocessing import Pool
import socket
import time

target_host = "140.116.245.151"
target_port = 2001

def seg(sentence):
    # create socket
    # AF_INET 代表使用標準 IPv4 位址或主機名稱
    # SOCK_STREAM 代表這會是一個 TCP client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client 建立連線
    client.connect((target_host, target_port))
    # 傳送資料給 target
    data = "seg@@" + sentence
    client.send(data.encode("utf-8"))
    
    # 回收結果信息
    data = bytes()
    while True:
        request = client.recv(8)
        if request:
            data += request
            begin = time.time()
        else:
            break

    WSResult = []
    response = data
    if(response is not None or response != ''):
        response = response.decode('utf-8').split()
        for resp in response:
            resp = resp.strip()
            resp = resp[0:len(resp)-1]
            temp = resp.split('(')
            word = temp[0]
            pos = temp[1]
            WSResult.append((word,pos))

    return WSResult

#####    Topic    #####
sentence = """
川普推特「專心當總統」　交棒2子就任前辭職
2016/12/13
商業大亨川普明年將成為美國總統，不過許多人質疑就任後會有利益衝突。
對此，川普在推特貼文表示，就任前將卸下公司所有的職務，「我的2個兒子和其他高層會負責接手。」
長子小唐納川普（Donald Trump Jr.）和次子艾瑞克川普（Eric Trump）目前都在川普集團擔任執行副主席一職。
"""

##########    extract the 5 types of entities    ##########    
#####   定義變數    #####
list_Nb=[]
list_Nd=[]
list_Nc=[]
list_Na=[]
list_VA=[]
list_VC_Long=[]
list_VC_Short=[]
tmp = seg(sentence)


#####   人名識別 Person Name List    #####
for i in range(0, len(seg(sentence))):
    if tmp[i][1] == 'Nb':
        list_Nb.append(tmp[i][0])

#####   時間識別 Time List    #####
i = 0
while i < len(seg(sentence)):
    change = False
    if tmp[i][1] == 'Nd':
        list_Nd.append(tmp[i][0])
    elif tmp[i][1] == 'Neu' and tmp[i+1][1] == 'FW':
        string = ''
        for j in range(i, len(seg(sentence))):
            if tmp[j][1] != 'Neu' and tmp[j][1] != 'FW':
                i = j
                change = True
                break
            else:
                string = string + tmp[j][0]
        list_Nd.append(string)
    if i > len(seg(sentence)):
        break
    elif change:
        continue
    else:
        i = i + 1

#####   地名識別 Location List    #####
for i in range(0, len(seg(sentence))):
    if tmp[i][1] == 'Nc':
        list_Nc.append(tmp[i][0])
        
#####   物件識別 Object List    #####
for i in range(0, len(seg(sentence))):
    if tmp[i][1] == 'Na':
        list_Na.append(tmp[i][0])
        
#####   完整事件 Complete Event List  精簡事件 Simple Event List   #####
for i in range(0, len(seg(sentence))):
    VCwithNA = False
    if tmp[i][1] == 'VA':
        list_VA.append(tmp[i][0])
    if tmp[i][1] == 'VC':
        for j in range(i+1, len(seg(sentence))):
            if tmp[j][1] == 'PERIODCATEGORY':
                break
            elif tmp[j][1] == 'Na':
                VCwithNA = True
                break
    if VCwithNA:
        for j in range(i, len(seg(sentence))):
            list_VC_Long.append(tmp[j][0])
            if tmp[j][1] == 'Na':
                break
    if VCwithNA:
        for j in range(i, len(seg(sentence))):
            if tmp[j][1] == 'VC':
                list_VC_Short.append(tmp[j][0])
            if tmp[j][1] == 'Na':
                list_VC_Short.append(tmp[j][0])
                break

#####   print out    #####
print("-----人名識別 Person Name List-----")
if len(list_Nb) != 0:
    for i in range(0,len(list_Nb)):
        print(list_Nb[i], end = ' ')
print('')
print('')
print("-----時間識別 Time List-----")
if len(list_Nd) != 0:
    for i in range(0,len(list_Nd)):
        print(list_Nd[i], end = ' ')
print('')
print('')
print("-----地名識別 Location List-----")
if len(list_Nc) != 0:
    for i in range(0,len(list_Nc)):
        print(list_Nc[i], end = ' ')
print('')
print('')
print("-----物件識別 Object List-----")
if len(list_Na) != 0:
    for i in range(0,len(list_Na)):
        print(list_Na[i], end = ' ')
print('')
print('')
print("-----完整事件 Complete Event List-----")
if len(list_VA) != 0:
    for i in range(0,len(list_VA)):
        print(list_VA[i], end = ' ')
print('')
if len(list_VC_Long) != 0:
    for i in range(0,len(list_VC_Long)):
        print(list_VC_Long[i], end = ' ')
print('')
print('')
print("-----精簡事件 Simple Event List-----")
if len(list_VA) != 0:
    for i in range(0,len(list_VA)):
        print(list_VA[i], end = ' ')
print('')
if len(list_VC_Short) != 0:
    for i in range(0,len(list_VC_Short)):
        print(list_VC_Short[i], end = ' ')
print('')
print('')

##########    Emotion Lexicon    ##########
#####    get data from file    #####
PosContent = []
with open('Positive.txt') as inFile:
    PosContent = inFile.read().splitlines()

NegContent = []
with open('Negative.txt') as inFile:
    NegContent = inFile.read().splitlines()

#####    search and print out    #####
Pos = 0
for i in range(0, len(seg(sentence))):
    if tmp[i][0] in PosContent:
        if Pos == 0:
            print('-----Positive Emotion-----')
            Pos = Pos + 1
        else:
            print(tmp[i][0], end = ' ')
            Pos = Pos + 1
if Pos == 0:
    print('-----Positive Emotion-----')
    print('')

Neg = 0
for i in range(0, len(seg(sentence))):
    if tmp[i][0] in NegContent:
        if Neg == 0:
            print('-----Negative Emotion-----')
            Neg = Neg + 1
        else:
            print(tmp[i][0], end = ' ')
            Neg = Neg + 1
if Neg == 0:
    print('-----Negative Emotion-----')
    print('')
    
    
