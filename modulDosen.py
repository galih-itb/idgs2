# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 11:20:58 2020

@author: galih
"""

from bs4 import BeautifulSoup
import requests
import json

def Data_Dosen():
    url = 'https://if.unikom.ac.id/id/penelitian/'
    # JIKA BUTUH PROXY #
    #proxies = {
    #"http": "http://user:pass@.itb.ac.id:8080",
    #"https": "http://user:pass@cache.itb.ac.id:8080",
    #}
    #page = requests.get(url,proxies=proxies)
    #print(req.text)
    ##############################
    page = requests.get(url)
    
    
    # TANPA PROXY =========================================================================
    # url = 'https://if.unikom.ac.id/id/penelitian/'
    # 
    #page = requests.get(url)
    # =============================================================================
    
    soup = BeautifulSoup(page.text, 'html.parser')
            
    data_nip = soup.findAll("td", {"class": "column-2"})
    data_nama = soup.findAll("td", {"class": "column-3"})
    data_GS = soup.findAll("td", {"class": "column-5"})
    
    
    # nip dosen
    dict_nip = []
    for data in data_nip:
        dict_nip.append(data.contents[0])
    
    # nama dosen
    dict_nama = []
    for data in data_nama:
        dict_nama.append(data.contents[0])
        
    # google scholar
    dict_GS = []
    for data in data_GS:
        GS = data.find('a', href=True)
        dict_GS.append(GS['href'])
    
    # dict_gabungan
    dict_gabungan = {}
    #jmlDosen = len(dict_nip)
    for i in range(len(dict_nip)):
        dict_gabungan[dict_nip[i]] = {"nama":dict_nama[i], "urlGS":dict_GS[i]}
    
    #print("Terdapat %s dosen" % jmlDosen)
    #print(dict_gabungan)
    return (dict_gabungan)

def NIP_NAMA(data_json):
    d = []
    for kunci in data_json:
        d.append(kunci + " " + data_json[kunci]["nama"])
    return d

def NIP_NAMA_DICT(data_json):
    d = {}
    for kunci in data_json:
        d[kunci] = data_json[kunci]["nama"]
    return d

def NAMA(data_json):
    d = []
    for kunci in data_json:
        d.append(data_json[kunci]["nama"])
    return d

def Data_Dosen_JSON(file_json):
    with open(file_json) as data_file:    
        return json.load(data_file)

def Tulis_Data_JSON(dataDosen, file_json):
    with open(file_json, 'w') as json_file:
        json.dump(dataDosen, json_file, sort_keys=True, indent=4)

# BARU #

# memunculkan data json dosen sesuai nip yang ditentukan
def DataDosen_NIP(data_json, nipCari):
    for i in range(len(data_json)):
        if data_json[i]["nip"]==str(nipCari):
            data = data_json[i]
            break
    return data

# memunculkan data json url sesuai nip yang ditentukan
def urlGS_NIP(data_json, nipCari, multi, indeks):
    #urlTarget = "https://scholar.google.co.id/citations?hl=en&user=" + idgs + "
    #               &cstart=" + str(awal) + "&pagesize=" + str(ukuran)
    #multi = False # multi halaman atau tidak
    data = None
    for i in range(len(data_json)):
        if data_json[i]["nip"]==str(nipCari):
            data = data_json[i]["urlGS"]
            if multi==1:
                awal = indeks * 100
                urlGS = data + "&cstart=" + str(awal) + "&pagesize=100"
                print("multi", urlGS)
            else:
                urlGS = data # bukan multi halaman
                print("single", urlGS)
            break
    return urlGS