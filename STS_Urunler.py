from tkinter import *
import pymysql.cursors
from tkinter import ttk
from tkinter import messagebox
import base64
import sys
import datetime
import cv2
import os
from PIL import Image, ImageTk
from tkinter import filedialog
from time import sleep
from threading import Thread
import random


class YetkiliPencere():

    def imageAdd(self,uzantı):
        img = PhotoImage(file = "StokTakipSistemi\\images\\"+uzantı+".png")
        return img


    def sayi_kontrol(self,kontrol,event=None):
        try:
            operatörler="!'^+%&/()=?<>,+-*_#$½{[]\|}~;:."
            sayi=self.kontrol.get()
            if((sayi[len(sayi)-1].isalpha()==True) or (sayi[len(sayi)-1] in operatörler)):
                    self.urunAdet.delete(len(sayi)-1,"end")
        except:
            print("tm")

    def fiyat_kontrol(self,kontrol2,event=None):
        try:
            operatörler="!'^+%&/()=?<>,+-*_#$½{[]\|}~;:"
            sayi=self.kontrol2.get()
            if(self.urunFiyat.get() == "."):
                self.urunFiyat.delete(len(sayi)-1,"end")
            if((sayi[len(sayi)-1].isalpha()==True) or (sayi[len(sayi)-1] in operatörler)):
                    self.urunFiyat.delete(len(sayi)-1,"end")
        except:
            print("tm")

    def listbox_select(self,event):
     try:
        widget=event.widget
        selection = widget.curselection()
        picked=widget.get(selection[0])
        SiraNo= picked.split(" ")
        if((int(SiraNo[0])>99) and (int(SiraNo[0])<1000)):
            self.silinecek_id = SiraNo[4]
        if((int(SiraNo[0])<99) and (int(SiraNo[0])>9)):
            self.silinecek_id = SiraNo[5]
        else:
            self.silinecek_id = SiraNo[6]

        with self.connection.cursor() as cursor:
            sql1="SELECT  urun_id, urun_ad, urun_adet, urun_tarih, urun_fiyat, urun_goruntu FROM sts_urunler WHERE urun_id = %s"%self.silinecek_id
            sorgu1 = cursor.execute(sql1)
            for i in cursor.fetchall():
                no=i["urun_id"]
                self.ad=i["urun_ad"]
                adet=i["urun_adet"]
                tarih=i["urun_tarih"]
                fiyat=i["urun_fiyat"]
                imj = i["urun_goruntu"]
        self.urunNo.config(state="normal")
        self.urunNo.delete(0,"end")
        self.urunNo.insert("end",no)
        self.urunNo.config(state="readonly")
        self.urunAd.delete(0,"end")
        self.urunAd.insert("end",self.ad)
        self.urunAdet.delete(0,"end")

        self.urunAdet.insert("end",adet)
        self.urunTarih.config(state="normal")
        self.urunTarih.delete(0,"end")
        self.urunTarih.insert("end",tarih)
        self.urunTarih.config(state="normal")
        self.urunFiyat.delete(0,"end")
        self.urunFiyat.insert("end",fiyat)
        self.img=True
        try:
            #img = PhotoImage(file = "C:\\Users\\Kürşad\\Desktop\\StokTakipSistemi\\images\\KameraKayit\\"+no+".png")
            img=ImageTk.PhotoImage(Image.open("StokTakipSistemi\\images\\KameraKayit\\"+no+".png"))
            self.resimler.config(image=img,width="180",height="180")
            self.yetkili_pencere.mainloop()
        except:
            yol="StokTakipSistemi\\images\\KameraKayit\\"+no+".png"
            imj = base64.b64decode(imj)
            with open(yol,'wb') as file:
                file.write(imj)
                img = ImageTk.PhotoImage(Image.open(yol))
                self.resimler.config(image=img,width="180",height="180")
                self.yetkili_pencere.mainloop()
     except:
        print(1)
############################## ARAMA OLACAKLAR'DA   açılışta entry basılacak metin ayarlanır.   ARAMAS OLACAKLARDA arama işlemi yapılır
    global firstclick
    firstclick=True

    def arama_olacaklar(self,event=None):
        self.firstclick=True
        self.event = event
        if self.firstclick: # if this is the first time they clicked it
            self.firstclick = False
            self.urunArama.delete(0, "end")


    def aramas_olacaklar(self,sv,event=None):
        if(self.sv.get()!=None and self.sv.get()!="Ürün, id veya ad..."):
            self.id_ad = self.sv.get()
            with self.connection.cursor() as cursor:
                #try:
                    sql = "SELECT * FROM sts_urunler WHERE urun_ad like  %s"
                    value=("%"+self.id_ad+"%")
                    sorgu1 = cursor.execute(sql,value)
                    if(sorgu1 >0 ):
                        print("ad bulundu")
                        self.dizileribosalt()
                        for i in cursor.fetchall():
                            self.urun_id.append(i["urun_id"])
                            self.urun_ad.append(i["urun_ad"])
                            self.urun_adet.append(i["urun_adet"])
                            self.urun_tarih.append(i["urun_tarih"])
                            self.urun_fiyat.append(i["urun_fiyat"])
                            self.urun_resim.append(i["urun_goruntu"])
                        self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
                    else:
                        self.dizileribosalt()
                        self.ürün_sorgula_classic()
                        self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)


                    if(sorgu1==0):
                        sql="SELECT  * FROM sts_urunler WHERE urun_id like %s"
                        value=("%"+self.id_ad+"%")
                        sorgu1 = cursor.execute(sql,value)
                        if(sorgu1>0):
                            print("id bulundu")
                            self.dizileribosalt()
                            for i in cursor.fetchall():
                                self.urun_id.append(i["urun_id"])
                                self.urun_ad.append(i["urun_ad"])
                                self.urun_adet.append(i["urun_adet"])
                                self.urun_tarih.append(i["urun_tarih"])
                                self.urun_fiyat.append(i["urun_fiyat"])
                                self.urun_resim.append(i["urun_goruntu"])
                            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
                        else:
                            self.dizileribosalt()
                            self.ürün_sorgula_classic()
                            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)

                #except:
                    #print("beklenmeyen hata")

########################      Kullanıcıdan Gelecek Giriş Widgetlerini Temizleme İşlemi ################
    def clear_widget(self,event=None):
        self.urunNo.config(state="normal")
        self.urunNo.delete(0,"end")
        self.urunAd.delete(0,"end")
        self.urunAdet.delete(0,"end")
        self.urunFiyat.delete(0,"end")
        self.urunTarih.delete(0,"end")
        self.urunTarih.insert(0,self.trh)
        self.urunTarih.config(state="normal")
        varsayılan=self.imageAdd("siyah")
        self.resimler.config(image='',width="30",height="12")

        self.img=FALSE
        self.yetkili_pencere.mainloop()

######################## Ürün Görselini KAMERA Kullanarak oluşturma işlemi #########3

    def resimCek(self,event=None):

     #try:
        if(self.urunNo.get()==""):
            messagebox.showinfo("Eksik Bilgi","Önce Ürün İD giriniz")
        else:
            self.resim_turu=""
            camera = cv2.VideoCapture(0)
            while True:
                return_value,image = camera.read()
                gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                cv2.imshow('image',gray)
                yenidenboyutlandır = cv2.resize(image,(180,180))
                key = cv2.waitKey(1) & 0xFF

                if (key == ord('s') or key == 13):

                    yol =  'StokTakipSistemi/images/KameraKayit/'
                    ret=cv2.imwrite(os.path.join(yol,self.urunNo.get()+".png"),yenidenboyutlandır)
                    self.filepatch2="StokTakipSistemi/images/KameraKayit/"+self.urunNo.get()+".png"
                    break

                if (key == ord("q") or key == 27):
                    cv2.destroyAllWindows()
                    break
            camera.release()
            cv2.destroyAllWindows()
            self.resim_turu="camera"
            upload_photo = ImageTk.PhotoImage(Image.open(self.filepatch2))
            self.resimler.config(image=upload_photo,width="180",height="180")
            self.img=TRUE
            self.yetkili_pencere.mainloop()

     #except:
       # messagebox.showwarning("uyarı","gecici süre kamera hizmeti devre dışıdır.")


####################################   Ürün Görselini Bilgisayardan seçme işlemi #############3

    def resimSec(self,event=None):
        if(self.urunNo.get()!=""):
            self.resim_turu=""
            self.filepatch = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=[('all files', '.*'),
               ('image files', '.png;.jpg'),
               ('image files!', '*.png;*.jpg')])

            if(self.filepatch!=""):
                print(self.filepatch)
                self.resim_turu="upload"
                #upload_photo = ImageTk.PhotoImage(Image.open(self.filepatch))
                upload_photo = Image.open(self.filepatch)
                upload_photo = upload_photo.resize((180,180), Image.ANTIALIAS)
                upload_photo.save(self.filepatch)
                upload_photo = ImageTk.PhotoImage(Image.open(self.filepatch))
               # print(type(upload_photo))
                self.resimler.config(image=upload_photo,width="180",height="180")

            ###### OKUNAN FOTOGRAF KENDİ DOSYAMIZA KOPYALANIYOR ########
                with open(self.filepatch, 'rb') as f:
                    photo = f.read()
                photo = base64.b64encode(photo)
                photo = base64.b64decode(photo)
                yol ="StokTakipSistemi\\images\\KameraKayit\\"+self.urunNo.get()+".png"
                with open(yol,'wb') as file:
                    file.write(photo)
                self.img=TRUE
                self.yetkili_pencere.mainloop()
        else:
            messagebox.showwarning("Uyarı","Önce ürüne ait İD'i giriniz")
            #print("Hata var")


    def urunGuncelle(self):
        self.resim_turu=""
        if(self.img==FALSE or  self.urunNo.get()=="" or self.urunAd.get()=="" or self.urunAdet.get()=="" or self.urunTarih.get()=="" or self.urunFiyat.get()==""):
                messagebox.showwarning("Eksik Bilgi","Güncellemek istediğiniz ürünün bilgilerini eksiksiz giriniz")
        else:

            urunid=self.urunNo.get()
            if(self.resim_turu=="upload"):
                print("tmm")
                with open(self.filepatch, 'rb') as f:
                        photo = f.read()
                        self.resim = base64.b64encode(photo)
            elif(self.resim_turu=="camera"):
                with open(self.filepatch2, 'rb') as f:
                    photo = f.read()
                    self.resim = base64.b64encode(photo)
            else:
                print("resim türsüz")
                with open("StokTakipSistemi\\images\\KameraKayit\\"+urunid+".png", 'rb') as f:
                    photo = f.read()
                self.resim=base64.b64encode(photo)
            guncelle="UPDATE sts_urunler SET urun_ad = %s, urun_adet = %s, urun_tarih=%s, urun_fiyat = %s, urun_goruntu = %s WHERE urun_id = %s "
            val=(self.urunAd.get(),self.urunAdet.get(),self.urunTarih.get(),self.urunFiyat.get(),self.resim,urunid)
            with self.connection.cursor() as cursor:
                cursor.execute(guncelle,val)
            messagebox.showinfo("BAŞARI","Ürün güncelleştirme işlemi tamamlandı")
            self.ürün_sorgula_classic()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
            self.clear_widget()
    ###########################################CHECK BOXLARIN KONTROLÜ#############################
    def listeleme_id(self):
        if(self.checkid.get()==0):
            self.ürün_sorgula_classic()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
        else:
            self.checkad.set(0)
            self.checkadet.set(0)
            self.checktarih.set(0)
            self.checkfiyat.set(0)
            self.ürün_sorgula_id()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
    def listeleme_ad(self):
        if(self.checkad.get()==0):
            self.ürün_sorgula_classic()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
        else:
            self.checkid.set(0)
            self.checkadet.set(0)
            self.checktarih.set(0)
            self.checkfiyat.set(0)
            self.ürün_sorgula_ad()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
    def listeleme_adet(self):
        if(self.checkadet.get()==0):
            self.ürün_sorgula_classic()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
        else:
            self.checkad.set(0)
            self.checkid.set(0)
            self.checktarih.set(0)
            self.checkfiyat.set(0)
            self.ürün_sorgula_adet()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
    def listeleme_tarih(self):
        if(self.checktarih.get()==0):
            self.ürün_sorgula_classic()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
        else:
            self.checkad.set(0)
            self.checkadet.set(0)
            self.checkid.set(0)
            self.checkfiyat.set(0)
            self.ürün_sorgula_tarih()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
    def listeleme_fiyat(self):
        if(self.checkfiyat.get()==0):
            self.ürün_sorgula_classic()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
        else:
            self.checkad.set(0)
            self.checkadet.set(0)
            self.checktarih.set(0)
            self.checkid.set(0)
            self.ürün_sorgula_fiyat()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)

#############################  ÜRÜN EKLEME ################################
    def urunEkle(self):
        if(self.img==FALSE or  self.urunNo.get()=="" or self.urunAd.get()=="" or self.urunAdet.get()=="" or self.urunTarih.get()=="" or self.urunFiyat.get()==""):
            messagebox.showwarning("Eksik Bilgi","Ürün Eklemek için Eksik Bilgileri Giriniz")
        else:
            with self.connection.cursor() as cursor:
                sql1="SELECT  urun_id, urun_ad, urun_adet, urun_tarih, urun_fiyat, urun_goruntu FROM sts_urunler WHERE urun_id = %s"%self.urunNo.get()
                sorgu1 = cursor.execute(sql1)
                if(sorgu1==1):
                    for i in cursor.fetchall():
                        no=i["urun_id"]
                        ad=i["urun_ad"]
                        adet=i["urun_adet"]
                        tarih=i["urun_tarih"]
                        fiyat=i["urun_fiyat"]
                        image = i["urun_goruntu"]
                    messagebox.showerror("Ekleme Hatası","""Eklemek istediğiniz ürün sisteme zaten kayıtlıdır""")
                    self.urunNo.config(state="readonly")
                    self.urunAd.delete(0,"end")
                    self.urunAd.insert(0,ad)
                    self.urunAdet.delete(0,"end")
                    self.urunAdet.insert(0,adet)
                    self.urunTarih.delete(0,"end")
                    self.urunTarih.insert(0,tarih)
                    self.urunFiyat.delete(0,"end")
                    self.urunFiyat.insert(0,fiyat)
                    image = base64.b64decode(image)
                    yol="StokTakipSistemi/images/KameraKayit/"+self.urunNo.get()+".png"
                    with open(yol,'wb') as file:
                        file.write(image)
                    foto = ImageTk.PhotoImage(Image.open(yol))
                    self.resimler.config(image=foto,width="180",height="180")
                    self.yetkili_pencere.mainloop()

                else:
                    if(self.resim_turu=="upload"):
                        with open(self.filepatch, 'rb') as f:
                            photo = f.read()
                            self.resim = base64.b64encode(photo)
                    if(self.resim_turu=="camera"):
                        with open(self.filepatch2, 'rb') as f:
                            photo = f.read()
                            self.resim = base64.b64encode(photo)



                    ürünEkle = "insert into sts_urunler(urun_id, urun_ad ,urun_adet ,urun_tarih ,urun_fiyat ,urun_goruntu) \
                    VALUES(%s,%s,%s,%s,%s,%s)"
                    vals=(self.urunNo.get(),self.urunAd.get(),self.urunAdet.get(),self.urunTarih.get(),self.urunFiyat.get(),self.resim)
                    sorgu=cursor.execute(ürünEkle,vals)
                    if(sorgu==1):
                        self.ürün_sorgula_classic()
                        self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
                        messagebox.showinfo("Sorgu Başarı","Ekleme İşlemi Başarılı")
                        self.clear_widget()


                    else:
                        messagebox.showwarning("BAKIM","Upload Photo geçiçi süre devre dışıdır")

    ################### ÜRÜN SİLME İŞLEMİ #########################

    def urunSil(self):   # ürün alışveriş işlemlerinde kayıtlı mı değil mi kontrol et kayıtlı ise onuda sil
        if(self.urunNo.get() != ""):
            self.silinecek_id = self.urunNo.get()
            with self.connection.cursor() as cursor:
                urun_varmi= "select * from sts_urunler where urun_id = %s"%self.silinecek_id
                var = cursor.execute(urun_varmi)
                for i in cursor.fetchall():
                        isim=i["urun_ad"]
                if(var==1):
                    cevap = messagebox.askquestion("Uyarı","{} numaralı {} ürünü silinecek emin misiniz?".format(self.silinecek_id,isim))
                    if(cevap=="yes"):
                        silme = "DELETE FROM sts_urunler WHERE urun_id= %s"
                        cursor.execute(silme,self.silinecek_id)
                        self.ürün_sorgula_classic()
                        self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
                        self.clear_widget()
                    else:
                        return 0
                else:
                    messagebox.showerror("Tanımsız Ürün İD","{} numaralı ürün kayıtlarda tanımlı değildir !!!".format(self.urunNo.get()))
        else:
            messagebox.showwarning("Tanımsız Ürün İd","""  Ürün silmek için İD giriniz
             veya
   Silmek istediğiniz ürünü seçiniz""")

   ########################################## Ürün Güncelleme İşlemi #######################################



#############################################  ÜRÜNLER  CLASSİC,İD,AD,TARİH,FİYAT,ADET'E GÖRE SORGULAMA###################
    def dizileribosalt(self):
        del self.urun_id[:]
        del self.urun_ad[:]
        del self.urun_adet[:]
        del self.urun_tarih[:]
        del self.urun_fiyat[:]

    def ürün_sorgula_id(self):
        with self.connection.cursor() as cursor:
            sorguClassic = "SELECT * FROM `sts_urunler` ORDER BY CAST(`urun_id` AS UNSIGNED INTEGER) ASC"
            cursor.execute(sorguClassic)
            self.dizileribosalt()
            print("dizi : {}".format(self.urun_id))
            for kolon in cursor.fetchall():

                self.urun_id.append(kolon["urun_id"])
                self.urun_ad.append(kolon["urun_ad"])
                self.urun_adet.append(kolon["urun_adet"])
                self.urun_tarih.append(kolon["urun_tarih"])
                self.urun_fiyat.append(kolon["urun_fiyat"])
                #self.urun_goruntu.append(kolon["urun_goruntu"])
    def ürün_sorgula_ad(self):
        with self.connection.cursor() as cursor:
            sorguClassic = "SELECT * FROM `sts_urunler` ORDER BY `urun_ad` ASC"
            cursor.execute(sorguClassic)
            self.dizileribosalt()
            for kolon in cursor.fetchall():

                self.urun_id.append(kolon["urun_id"])
                self.urun_ad.append(kolon["urun_ad"])
                self.urun_adet.append(kolon["urun_adet"])
                self.urun_tarih.append(kolon["urun_tarih"])
                self.urun_fiyat.append(kolon["urun_fiyat"])
                #self.urun_goruntu.append(kolon["urun_goruntu"])
    def ürün_sorgula_adet(self):
        with self.connection.cursor() as cursor:
            sorguClassic = "SELECT * FROM `sts_urunler` ORDER BY CAST(`urun_adet` AS UNSIGNED INTEGER) ASC"
            cursor.execute(sorguClassic)
            self.dizileribosalt()
            print("dizi : {}".format(self.urun_id))
            for kolon in cursor.fetchall():

                self.urun_id.append(kolon["urun_id"])
                self.urun_ad.append(kolon["urun_ad"])
                self.urun_adet.append(kolon["urun_adet"])
                self.urun_tarih.append(kolon["urun_tarih"])
                self.urun_fiyat.append(kolon["urun_fiyat"])
                #self.urun_goruntu.append(kolon["urun_goruntu"])
    def ürün_sorgula_tarih(self):
        with self.connection.cursor() as cursor:
            sorguClassic = "SELECT * FROM `sts_urunler` ORDER BY `urun_tarih` ASC"
            cursor.execute(sorguClassic)
            self.dizileribosalt()
            print("dizi : {}".format(self.urun_id))
            for kolon in cursor.fetchall():

                self.urun_id.append(kolon["urun_id"])
                self.urun_ad.append(kolon["urun_ad"])
                self.urun_adet.append(kolon["urun_adet"])
                self.urun_tarih.append(kolon["urun_tarih"])
                self.urun_fiyat.append(kolon["urun_fiyat"])
                #self.urun_goruntu.append(kolon["urun_goruntu"])
    def ürün_sorgula_fiyat(self):
        with self.connection.cursor() as cursor:
            sorguClassic = "SELECT * FROM `sts_urunler` ORDER BY CAST(`urun_fiyat` AS UNSIGNED INTEGER) ASC"
            cursor.execute(sorguClassic)
            self.dizileribosalt()
            print("dizi : {}".format(self.urun_id))
            for kolon in cursor.fetchall():

                self.urun_id.append(kolon["urun_id"])
                self.urun_ad.append(kolon["urun_ad"])
                self.urun_adet.append(kolon["urun_adet"])
                self.urun_tarih.append(kolon["urun_tarih"])
                self.urun_fiyat.append(kolon["urun_fiyat"])
                #self.urun_goruntu.append(kolon["urun_goruntu"])

    def ürün_sorgula_classic(self):
        self.urun_id=[]
        self.urun_ad=[]
        self.urun_adet=[]
        self.urun_tarih=[]
        self.urun_fiyat=[]
        self.urun_resim=[]
        self.firstadet=0
        with self.connection.cursor() as cursor:
            sorguClassic = "SELECT * FROM `sts_urunler`"
            cursor.execute(sorguClassic)
            for kolon in cursor.fetchall():
                self.urun_id.append(kolon["urun_id"])
                self.urun_ad.append(kolon["urun_ad"])
                self.urun_adet.append(kolon["urun_adet"])
                self.urun_tarih.append(kolon["urun_tarih"])
                self.urun_fiyat.append(kolon["urun_fiyat"])
                #self.urun_goruntu.append(kolon["urun_goruntu"])
                self.firstadet = self.firstadet + int(kolon["urun_adet"])
        print("bu")
        print(self.firstadet)
        print("bu")

    def thread_fonksiyon(self,ne,time):
        try:
            self.connectiontwo = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='',
                                                     db='stoktakipsistemi',
                                                     charset='utf8mb4',
                                                     cursorclass=pymysql.cursors.DictCursor)

            while True:
                self.adet = 0
                with self.connectiontwo.cursor() as cursor2:
                    adetSorgu = "SELECT urun_adet FROM `sts_urunler`"
                    cursor2.execute(adetSorgu)
                    for kolon in cursor2.fetchall():
                        self.adet = self.adet + int(kolon["urun_adet"])
                if self.adet != self.firstadet:
                   self.metin.set("Güncel Değil")
                   self.durum.config(bg="red")
                else:
                    self.metin.set("Güncel")
                    self.durum.config(bg="green")

                sleep(time)
        except:
                print("config hatası")


    # Otomatik İd oluşturmak için sorgu
    def oto_id_olustur(self):
        self.allId=[]
        with self.connection.cursor() as cursor:
            sorguid = "SELECT urun_id FROM `sts_urunler`"
            cursor.execute(sorguid)
            for kolon in cursor.fetchall():
                self.allId.append(kolon["urun_id"])
        aralik = range(10000000000,99999999999)
        sayi = random.sample(aralik,1)
        oto_id=str(sayi[0])
        if oto_id in self.allId:
            sayi = random.sample(aralik,1)
            oto_id=str(sayi[0])
        self.urunNo.delete(0,END)
        self.urunNo.insert(END,oto_id)




####################### ANA LİSTELEME FONKSİYONU ################

    def listele(self,ürünid=[],ürünad=[],ürünadet=[],ürüntarih=[],ürünfiyat=[]):
        self.listbox.delete(0,END)
        self.boyut = len(ürünid)
        for i in range(0,self.boyut):
            cıktı="{:<5d}  {:<10s}  {:<13s}  {:<13s}  {:<19s}  {:<19s}".format((i+1), ürünid[i],ürünad[i],ürünadet[i],str(ürüntarih[i]),ürünfiyat[i])
            self.listbox.insert(END,cıktı)
            #self.listbox.itemconfig(0,bg="red")
            if(i%2==1):
                self.listbox.itemconfig(i,bg="red")

    def yenile_fonksiyon(self):
        if(self.checkid.get()==1):
            self.ürün_sorgula_classic()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
        elif(self.checkad.get()==1):
            self.ürün_sorgula_ad()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
        elif(self.checkadet.get()==1):
            self.ürün_sorgula_adet()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
        elif(self.checktarih.get()==1):
            self.ürün_sorgula_tarih()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
        elif(self.checkfiyat.get()==1):
            self.ürün_sorgula_fiyat()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
        else:
            self.ürün_sorgula_classic()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)

############# YAPILANDIRICI ##########
    def __init__(self):

        self.connection = pymysql.connect(host='localhost',
                                                 user='root',
                                                 password='',
                                                 db='stoktakipsistemi',
                                                 charset='utf8mb4',
                                                 cursorclass=pymysql.cursors.DictCursor)

        # Uyarilacaklar kısmından  herhangi bir urunid gösterilecekse kontrol edilir

        yetkili_pencere = Toplevel()
        self.yetkili_pencere = yetkili_pencere;
        yetkili_pencere.title("Stok İşlemleri")
        yetkili_pencere.geometry("780x620+300+30")
        #yetkili_pencere.tk_setPalette("white")
        yetkili_pencere.resizable(0,0)
        canvas = Canvas(yetkili_pencere,width=780,height=620)
        myimage = PhotoImage(file = "StokTakipSistemi\\images\\arkaplan2.png")
        canvas.create_image(0,0,anchor=NW, image=myimage)

        geriButton = Button(canvas,text="Geri Gel",bg="white")
        geriButton.place(x=150,y=0)
        resimg=self.imageAdd("geri")
        geriButton.config(image=resimg,width="45", height="35",command=self.yetkili_pencere.destroy)


        temizleButton = Button(canvas,text="Temizle",command=self.clear_widget)
        temizleButton.place(x=0,y=0)
        resim3=self.imageAdd("temizleme")
        temizleButton.config(image=resim3,width="35", height="20")


        urunNolabel = Label(canvas, text="Ürün Id")
        urunNolabel.place(x=20, y=60)
        self.urunNo = Entry(canvas,width=22,cursor="bottom_side")
        self.urunNo.place(x=140,y=60)

        otoId = Button(canvas,width="6",height="1",command=self.oto_id_olustur)
        otoId.place(x=280,y=60)
        resimoto = self.imageAdd("refresh2")
        otoId.config(image=resimoto,width="15",height="15")


        urunAdLabel = Label(canvas, text="Ürün Adi")
        urunAdLabel.place(x=20 , y=90)
        self.urunAd = Entry(canvas, width=22,cursor="bottom_side")
        self.urunAd.place(x=140 , y=90)

        urunAdetLabel = Label(canvas,text="Ürün Adet")
        urunAdetLabel.place(x=20, y=120)
        self.kontrol=StringVar()
        self.kontrol.trace("w", lambda name, index, mode, kontrol=self.kontrol:self.sayi_kontrol(self.kontrol))
        self.urunAdet = Entry(canvas,width=22,textvariable=self.kontrol,cursor="bottom_side")
        self.urunAdet.place(x=140,y=120)

        urunTarih = Label(canvas,text="Ürün Tarihi")
        urunTarih.place(x=20 ,y=150)
        self.urunTarih = Entry(canvas, width=22,cursor="bottom_side")
        self.urunTarih.place(x=140 , y=150)

        urunFiyatLabel = Label(canvas,text="Ürün Birim Fiyat")
        urunFiyatLabel.place(x=20,y=180)
        self.kontrol2 = StringVar()
        self.kontrol2.trace("w", lambda name, index, mode, kontrol2=self.kontrol2:self.fiyat_kontrol(self.kontrol2))
        self.urunFiyat = Entry(canvas,width=22,textvariable=self.kontrol2,cursor="bottom_side")
        self.urunFiyat.place(x=140, y=180)

        urunResimLabel = Label(canvas,text="Ürün Görseli")
        urunResimLabel.place(x=20, y=215)
        self.urunKameraButton = Button (canvas,text="Kamera",width=8)
        self.urunKameraButton.place(x=140,y=210)
        resimKamera=self.imageAdd("kamera")
        self.urunKameraButton.config(image=resimKamera,width="65", height="25" , compound="none",command=self.resimCek)

        self.urunSecButton = Button(canvas,text=" Sec",width=8)
        self.urunSecButton.place (x=210,y=210)
        resimDosya=self.imageAdd("dosya")
        self.urunSecButton.config(image=resimDosya,width="65", height="25" ,compound="none",command=self.resimSec)

        #upload_photo = PhotoImage(file="C:\\Users\\Kürşad\\Desktop\\StokTakipSistemi\\images\\deneme.png")
        #upload_photo = ImageTk.PhotoImage(Image.open("C:\\Users\\Kürşad\\Desktop\\StokTakipSistemi\\images\\deneme.png"))
        self.resimler = Label(canvas,text="Ürün Görseli",width="30",height="12",bg="White",fg="black")
        self.resimler.place(x=500,y=60)
        self.resimler.config(width="25",height="12")
        self.img=FALSE


        self.urun_Ekle = Button(canvas,text="Ekle",width="24",height="4",bg="#fbf8f8",command=self.urunEkle)
        self.urun_Ekle.place(x=20,y=260)
        resimEkle=self.imageAdd("ekle")
        self.urun_Ekle.config(image=resimEkle,width="70", height="60",compound="top")

        self.urun_Sil = Button(canvas,text="Sil",width="24",height="4",bg="#fbf8f8",command=self.urunSil)
        self.urun_Sil.place(x=110,y=260)
        resimSil=self.imageAdd("sil")
        self.urun_Sil.config(image=resimSil,width="70", height="60",compound="top")

        self.urun_Guncelle = Button(canvas,text="Güncelle",width="24",height="4",bg="#fbf8f8",command=self.urunGuncelle)
        self.urun_Guncelle.place(x=205,y=260)
        resimGüncelle=self.imageAdd("güncelle")
        self.urun_Guncelle.config(image=resimGüncelle,width="70", height="60",compound="top")


        arama = Label(canvas,text="Ürün Arama :",fg="red")
        arama.config(font=("Times", "14", "bold italic"))
        arama.place(x=310 , y=280)
        self.sv = StringVar()
        self.sv.trace("w", lambda name, index, mode, sv=self.sv:self.aramas_olacaklar(self.sv))
        self.urunArama = Entry(canvas,width="22",textvariable=self.sv,cursor="bottom_side")
        self.urunArama.place(x=450,y=285)
        self.urunArama.insert(0,"Ürün, id veya ad...")
        self.urunArama.bind('<Button-1>', self.arama_olacaklar)

        self.metin = StringVar()
        img=self.imageAdd("refresh2")
        self.yenile = Button(canvas,text="",width=13,height=15,command=self.yenile_fonksiyon)
        self.yenile.config(image=img,width=13)
        self.yenile.place(x=640,y=285)
        self.durum=Label(canvas,textvariable=self.metin,bg="green")
        self.durum.place(x=660,y=285)
        self.metin.set("Liste Güncel")


        self.checkid =IntVar()
        self.Check_id_button = Checkbutton(canvas , text="İD" , variable = self.checkid , onvalue = 1 , offvalue = 0 ,height = 1, width="5",bg="white",fg="black",font=("Times","16","bold italic"),command=self.listeleme_id)
        self.Check_id_button.place(x=60,y=340)

        self.checkad =IntVar()
        self.Check_ad_button = Checkbutton(canvas , text="AD" , variable = self.checkad , onvalue = 1 , offvalue = 0 ,height = 1, width="8",bg="white",fg="black",font=("Times","16","bold italic"),command=self.listeleme_ad)
        self.Check_ad_button.place(x=140,y=340)

        self.checkadet =IntVar()
        self.Check_adet_button = Checkbutton(canvas , text="Adet" , variable = self.checkadet , onvalue = 1 , offvalue = 0 ,height = 1, width="8",bg="white",fg="black",font=("Times","16","bold italic"),command=self.listeleme_adet )
        self.Check_adet_button.place(x=270,y=340)

        self.checktarih =IntVar()
        self.Check_id_tarih = Checkbutton(canvas , text="Eklenme Tarihi" , variable = self.checktarih , onvalue = 1 , offvalue = 0 ,height = 1, width="13",bg="white",fg="black",font=("Times","16","bold italic"),command=self.listeleme_tarih )
        self.Check_id_tarih.place(x=390,y=340)

        self.checkfiyat =IntVar()
        self.Check_fiyat_button = Checkbutton(canvas , text="Birim Fiyat" , variable = self.checkfiyat , onvalue = 1 , offvalue = 0 ,height = 1, width="9",bg="white",fg="black",font=("Times","16","bold italic"),command=self.listeleme_fiyat )
        self.Check_fiyat_button.place(x=580,y=340)



        self.scrollbar = Scrollbar(self.yetkili_pencere)
        self.listbox = Listbox(canvas,width="80",height="12",bg="black",fg="white",font='consolas',yscrollcommand = self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.bind('<<ListboxSelect>>',self.listbox_select)
        self.listbox.place(x=20, y=370)

        # oldugumuz gün bastırılıyor
        trh = datetime.datetime.now()
        self.trh = "{}-{}-{}".format(trh.year,trh.month,trh.day)
        self.urunTarih.insert(0,self.trh)
        self.ürün_sorgula_classic()
        self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)

        degisiklik_kontrol = Thread(target=self.thread_fonksiyon ,args=("calisti",1))
        degisiklik_kontrol.start()


        self.uyarilacakid=[]
        with self.connection.cursor() as cursor:
            sorgu = "SELECT * FROM sts_kayıt"
            uyarilacak_kisi=cursor.execute(sorgu)
            if uyarilacak_kisi > 1:
                for kolon in cursor.fetchall():
                    self.uyarilacakid.append(kolon["uye_kullaniciadi"])
                uyarilacakid = self.uyarilacakid[len(self.uyarilacakid)-1]
                sorgu2 = "DELETE FROM sts_kayıt where uye_kullaniciadi = %s"
                cursor.execute(sorgu2,uyarilacakid)
                sorgu3 = "select * from sts_urunler where urun_id = %s"
                cursor.execute(sorgu3,uyarilacakid)
                for uyarilacak in cursor.fetchall():
                    urunad=uyarilacak["urun_ad"]
                    urunadet=uyarilacak["urun_adet"]
                    uruntarih=str(uyarilacak["urun_tarih"])
                    urunfiyat=uyarilacak["urun_fiyat"]
                self.urunNo.insert(END,uyarilacakid)
                self.urunNo.config(state="readonly")
                self.urunAd.insert(END,urunad)
                self.urunAdet.config(background="red",foreground="white")
                self.urunAdet.insert(END,urunadet)
                self.urunTarih.delete(0,"end")
                self.urunTarih.insert(END,uruntarih)
                self.urunFiyat.insert(END,urunfiyat)
                self.resim_turu="upload"
                self.img = True
                self.filepatch="StokTakipSistemi\\images\\KameraKayit\\"+uyarilacakid+".png"

            else:
                a=5

        canvas.pack()
        yetkili_pencere.mainloop()


