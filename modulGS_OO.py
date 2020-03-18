# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 23:25:08 2020

@author: galih
"""

class GS_Scraper():
    def __init__(self, soup):
        self.soup = soup
    
    def ID_GS(self):
        idGS = self.soup.findAll(attrs={"name" : "user"})
        get_val = None
        for item in idGS:
            get_val = item["value"]
        return get_val

    def NamaAkun(self):
        nama = self.soup.find(id='gsc_prf_in')
        if nama == None:
            return ""
        else:
            return nama.contents[0]
    
    def NamaAfiliasi(self):
        nama = self.soup.find("div",{"class":"gsc_prf_il"})
        if nama == None:
            return ""
        else:
            return nama.contents[0]
        #return nama.contents[0]
    
    def JumlahDokumen(self):
        cek_baris = self.soup.findAll("tr", {"class": "gsc_a_tr"})
        return len(cek_baris)
    
    def SemuaDokumen(self, idxHalaman):
        barisAll = self.soup.findAll("tr", class_="gsc_a_tr")
        #dictDokumen = {}
        listDok = []
        idxTambahan = idxHalaman * 100
        for i in range(len(barisAll)):
            baris = barisAll[i].findAll("td") # data baris <td> (ada 3 buah data per <td>)
            # <td> 1 ada 3 buah data juga
            # ada tag "a" berisi judul dokumen, <div> pertama berisi Penulis, 
            # dan <div> kedua berisi venue
            # 1.1 : judul dokumen
            judul = baris[0].find("a", class_="gsc_a_at").text
            # 1.2 : penulis
            penulis = baris[0].findAll("div", class_="gs_gray")[0].text
            # 1.3 : venue
            venue = baris[0].findAll("div", class_="gs_gray")[1].text
            # 2.1 : jumlah sitasi
            strSitasi = baris[1].find("a", class_="gsc_a_ac gs_ibl")
            if strSitasi == None:
                jmlSitasi = 0
            else:
                jmlSitasi = 0 if strSitasi.text == '' else int(strSitasi.text) # isi 0 jika kosong
            # 3.1 : tahun dokumen
            strTahun = baris[2].find("span", class_="gsc_a_h gsc_a_hc gs_ibl").text
            tahun = 0 if strTahun == '' else int(strTahun)
            
            # masukkan semua data ke dictionary
            #dictDokumen[i+idxTambahan] = {"judul":judul, "penulis":penulis, "venue":venue, \
            #                  "sitasi":jmlSitasi, "tahun":tahun}
            listDok.append({"id":i+idxTambahan, "judul":judul, "penulis":penulis, "venue":venue, \
                            "jmlSitasi":jmlSitasi, "tahun":tahun})
        
        return listDok

    def SitasiTahunanV2(self):
        dict_sitasi = {}
        jml_tahun_diambil = 10
        
        # data tahun
        data_tahun = self.soup.findAll("span", {"class": "gsc_g_t"})
        list_tahun = []
        for i in data_tahun:
            list_tahun.append(i.contents[0])
        print("jml tahun =", len(data_tahun))
        # data sitasi
        data_sitasi = self.soup.findAll("span", {"class": "gsc_g_al"})
        list_sitasi = []
        for j in data_sitasi:
            list_sitasi.append(j.contents[0])
        print("jml sitasi tahun =", len(data_sitasi))
#        if len(data_tahun)>len(data_sitasi): # kasus bu Kania, jml tahun > jml sitasi
#            if len(data_sitasi)>=jml_tahun_diambil:
#                print("satu")
#                list_tahun_baru = list_tahun[len(list_tahun)-jml_tahun_diambil:len(list_tahun)]
#                list_sitasi_baru = list_sitasi[len(list_sitasi)-jml_tahun_diambil:len(list_sitasi)]
#            else:
#                print("dua")
#                jml_tahun_diambil=len(data_sitasi)
#                list_tahun_baru = list_tahun[len(list_tahun)-jml_tahun_diambil:len(list_tahun)]
#                list_sitasi_baru = list_sitasi[len(list_sitasi)-jml_tahun_diambil:len(list_sitasi)]
        
        if len(data_tahun)>len(data_sitasi): # kasus bu Kania, jml tahun > jml sitasi   
            if len(data_sitasi)<=jml_tahun_diambil:
                jml_tahun_diambil = len(data_sitasi)                
                print("satu")
            else:
                print("dua")
            print("Jml tahun:", len(data_tahun))
            print("Jml sitasi:", len(data_sitasi))
            print("Jml X:", jml_tahun_diambil)
            #jml_tahun_diambil=len(data_sitasi)
            list_tahun_baru = list_tahun[len(list_tahun)-jml_tahun_diambil:len(list_tahun)]
            list_sitasi_baru = list_sitasi[len(list_sitasi)-jml_tahun_diambil:len(list_sitasi)]
        else : # jml sitasi = jml tahun
            if len(data_sitasi)>jml_tahun_diambil: # jml sitasi > 10
                list_tahun_baru = list_tahun[len(list_tahun)-jml_tahun_diambil:len(list_tahun)]
                list_sitasi_baru = list_sitasi[len(list_sitasi)-jml_tahun_diambil:len(list_sitasi)]
            else:
                list_tahun_baru = list_tahun
                list_sitasi_baru = list_sitasi
            
        for i in range(len(list_sitasi_baru)):
            tahun = list_tahun_baru[i]
            sitasi = list_sitasi_baru[i]
            dict_sitasi[tahun] = sitasi
        
        print(dict_sitasi)
        return dict_sitasi
    
    def SitasiTahunanLama(self):
        # data tahun
        data_tahun = self.soup.findAll("span", {"class": "gsc_g_t"})
        dict_tahun = []
        for i in data_tahun:
            dict_tahun.append(i.contents[0])
        
        # data sitasi
        data_sitasi = self.soup.findAll("span", {"class": "gsc_g_al"})
        dict_sitasi = []
        for j in data_sitasi:
            dict_sitasi.append(j.contents[0])
            
        sitasi_all = {}
        for x in range(len(dict_sitasi)):
            sitasi_all[dict_tahun[x]] = dict_sitasi[x]
            
    
    def Daftar_Subject(self):
        subject = self.soup.find(class_="gsc_prf_il", id="gsc_prf_int")
        subject_item = subject.find_all('a')
        
        dict_subject = []
        for item_s in subject_item:
            it = item_s.contents[0]
            dict_subject.append(it)
            
        return dict_subject

    def Daftar_Subject_Rapi(self):
        # menggabung isi list dalam sebuah string dimana setiap item dipisah tanda koma
        subject = ", ".join(self.Daftar_Subject())
        return subject
    
    def Daftar_Sitasi(self):
        data_sitasi = self.soup.findAll("td", {"class": "gsc_rsb_std"})
        return data_sitasi

    def Daftar_Sitasi_Bersih(self):
        data_sitasi = self.Daftar_Sitasi()
        dict_sitasi = {}
        if len(data_sitasi)>0: 
            dict_sitasi["all_sitasi"] = data_sitasi[0].string
            dict_sitasi["2015_sitasi"] = data_sitasi[1].string
            dict_sitasi["all_hIndex"] = data_sitasi[2].string
            dict_sitasi["2015_hIndex"] = data_sitasi[3].string
            dict_sitasi["all_i10index"] = data_sitasi[4].string
            dict_sitasi["2015_i10index"] = data_sitasi[5].string
        #print(dict_sitasi)
        return dict_sitasi
    
    def Daftar_Co_AuthorsV2(self):
        # tag DIV untuk co-authors
        urlGoogle = "https://scholar.google.com"
        data_all = self.soup.findAll("div", {"class": "gsc_rsb_aa"})
        
        daftar_co = []
        for i in range(len(data_all)):
            data_baris_profil = data_all[i].findAll("a")
            data_baris_afiliasi = data_all[i].find("span",{"class":"gsc_rsb_a_ext"})
            nama = data_baris_profil[0].text
            url = urlGoogle + data_baris_profil[0]["href"]
            #print(url)
            #url_encoded = urllib.parse.quote(url)
            afiliasi = data_baris_afiliasi.text
            daftar_co.append({"nama":nama, "url":url, "afiliasi":afiliasi})
        #print(daftar_co)
        return daftar_co
    
    def Daftar_Co_Authors(self):
        data_co = self.soup.findAll("span", {"class": "gsc_rsb_a_desc"})
        data_co_aff = self.soup.findAll("span", {"class": "gsc_rsb_a_ext"})
        
        dict_co = {}
        j=0
        for item_co in data_co:
            it_co = item_co.contents[0].string
            dict_co[it_co] = ""
            j+=1
            #print(it_co)
        
        k=0
        kk=0
        dict_co_aff = []
        for item_co_aff in data_co_aff:
            it_co = item_co_aff.contents[0].string
            #dict_co[it_co] = ""
            if k % 2 == 0:
                dict_co_aff.append(it_co)
                kk+=1
                #print(dict_co)
            k+=1
        
        xx=0
        for x in dict_co:
            dict_co[x] = dict_co_aff[xx]
            xx+=1
        
        return dict_co

    def Daftar_Co_Authors_Rapi(self):
        dict_co = self.Daftar_Co_Authors()
        #print(GS.Daftar_Co_Authors(soup))
        for a,b in dict_co.items():
            print("%s (%s)" % (a,b))

#Profil GS (selain dokumen)
#
#- ID
#- Nama
#- Afiliasi
#- Subject (area penelitian)
#- Co-Authors
#- Sitasi Total
#- Sitasi Tahunan
#- Jumlah dokumen
    def Profil_Lengkap(self):
        idgs = self.ID_GS()
        nama = self.NamaAkun()
        afiliasi = self.NamaAfiliasi()
        subject = self.Daftar_Subject_Rapi()
        co_authors = self.Daftar_Co_AuthorsV2()
        sitasi_total = self.Daftar_Sitasi_Bersih()
        sitasi_tahunan = self.SitasiTahunanV2()
        #print(co_authors)
        lstProfil = []
        lstProfil.append({"idgs":idgs,
                          "nama":nama,
                          "afiliasi":afiliasi,
                          "subject":subject,
                          "co_authors":co_authors,
                          "sitasi_total":sitasi_total,
                          "sitasi_tahunan":sitasi_tahunan})
        #print(lstProfil)
        return lstProfil
#---------------------------------------------------------


# mengambil ID GS dari URL
def ID_GS_URL(url):
    pos_user = url.find("user=") #39
    pos_hl = url.find("&hl") #56
    awal_id = pos_user + 5
    if pos_hl == -1 : # tidak ada &hl
        idgs = url[awal_id:]
    else:
        panjang = pos_hl - awal_id
        idgs = url[awal_id:awal_id+panjang]
    return idgs

# menentukan URL berdasarkan ID. hal/indeks dapat diisi:0,1,2,dst
def URL_GS(idgs,hal):
    ukuran = 100

    if hal==-1:
        urlTarget = "https://scholar.google.co.id/citations?hl=en&user=" + idgs
    else:
        awal = hal*100
        urlTarget = "https://scholar.google.co.id/citations?hl=en&user=" + idgs + "&cstart=" + str(awal) + "&pagesize=" + str(ukuran)
    return urlTarget