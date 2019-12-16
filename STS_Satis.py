from tkinter import *
import pymysql.cursors
from tkinter import ttk
from tkinter import messagebox
import sys
import re
import base64
from PIL import Image, ImageTk
from tkinter import filedialog
import datetime


class AlisVeris():

    def imageAdd(self,uzantı):
        img = PhotoImage(file = "StokTakipSistemi\\images\\"+uzantı+".png")
        return img
    def gerigel(self):
        sys.exit
        self.alisveris_pencere.destroy()

    def alisveris_sorgulaca_classic(self):
        self.sts_urun_id=[]
        self.sts_urun_adi=[]
        self.sts_islem_id=[]
        self.sts_müsteri_adi=[]
        self.sts_müsteri_soyadi=[]
        self.sts_urun_adet=[]
        self.sts_islem_tarihi=[]
        with self.connection.cursor() as cursor:
            sorguKarisik ="SELECT * FROM sts_urunler AS urunler,sts_alisveris AS alisveris, sts_müsteri AS müsteri WHERE\
             urunler.urun_id = alisveris.sts_urun_id and müsteri.müsteri_id = alisveris.sts_müsteri_id and alisveris.sts_durum='1'"
            cursor.execute(sorguKarisik)
            for kolon in cursor.fetchall():
                self.sts_urun_id.append(kolon["urun_id"])
                self.sts_urun_adi.append(kolon["urun_ad"])
                self.sts_islem_id.append(kolon["sts_islem_id"])
                self.sts_müsteri_adi.append(kolon["müsteri_adi"])
                self.sts_müsteri_soyadi.append(kolon["müsteri_soyadi"])
                self.sts_urun_adet.append(kolon["sts_urun_adet"])
                self.sts_islem_tarihi.append(kolon["sts_islem_tarih"])

    def listele_alisveris(self,urun_id=[],urun_adi=[],islem_id=[],müsteri_adi=[],müsteri_soyadi=[],urun_adet=[],islem_tarihi=[]):
        self.listbox2.delete(0,END)
        boyut = len(urun_id)
        for i in range(0,boyut):
            cıktı="{:<3d}  {:<10d}  {:<7s}  {:<12s}  {:<8s}  {:<8s}  {:<6s}  {:<10s}".format((i+1), islem_id[i],müsteri_adi[i],müsteri_soyadi[i],urun_id[i],urun_adi[i],urun_adet[i],str(islem_tarihi[i]))
            self.listbox2.insert(END,cıktı)
            if(i%2==1):
                self.listbox2.itemconfig(i,bg="green")



    def ürün_sorgula_classic(self):
        self.urun_id=[]
        self.urun_ad=[]
        self.urun_adet=[]
        self.urun_tarih=[]
        self.urun_fiyat=[]
        self.urun_resim=[]
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

    def listele(self,ürünid=[],ürünad=[],ürünadet=[],ürüntarih=[],ürünfiyat=[]):
        self.listbox.delete(0,END)
        self.boyut = len(ürünid)
        for i in range(0,self.boyut):
            cıktı="{:<5d}  {:<10s}  {:<13s}  {:<13s}  {:<19s}  {:<19s}".format((i+1), ürünid[i],ürünad[i],ürünadet[i],str(ürüntarih[i]),ürünfiyat[i])
            self.listbox.insert(END,cıktı)


            if(i%2==1):
                self.listbox.itemconfig(i,bg="red")

    def listbox_select(self,event):
     try:
        widget=event.widget
        selection = widget.curselection()
        picked=widget.get(selection[0])
        SiraNo= picked.split()
        self.urunid= SiraNo[1]
        self.Urunadet = SiraNo[3]
        self.adet_update(self.Urunadet)
        print(self.Urunadet)

        with self.connection.cursor() as cursor:
            sql1="SELECT  urun_id, urun_ad, urun_adet, urun_tarih, urun_fiyat, urun_goruntu FROM sts_urunler WHERE urun_id = %s"%self.urunid
            sorgu1 = cursor.execute(sql1)
            for i in cursor.fetchall():
                no=i["urun_id"]
                self.ad=i["urun_ad"]
                adet=i["urun_adet"]
                tarih=i["urun_tarih"]
                fiyat=i["urun_fiyat"]
                imj = i["urun_goruntu"]

        try:
            img=ImageTk.PhotoImage(Image.open("StokTakipSistemi\\images\\KameraKayit\\"+no+".png"))
            self.resimler.config(image=img,width="180",height="180")
            self.alisveris_pencere.mainloop()
        except:
            yol="StokTakipSistemi\\images\\KameraKayit\\"+no+".png"
            imj = base64.b64decode(imj)
            with open(yol,'wb') as file:
                file.write(imj)
                img = ImageTk.PhotoImage(Image.open(yol))
                self.resimler.config(image=img,width="180",height="180")
                self.alisveris_pencere.mainloop()
     except :
        a=5
    def listbox2_select(self,event):
     try:
        widget=event.widget
        selection = widget.curselection()
        picked=widget.get(selection[0])
        SiraNo= picked.split()
        self.urunid2= SiraNo[4]
        self.islemid=SiraNo[1]
        self.sira = SiraNo[0]
        print(self.islemid)

        try:
            img=ImageTk.PhotoImage(Image.open("StokTakipSistemi\\images\\KameraKayit\\"+self.urunid2+".png"))
            self.resimler2.config(image=img,width="180",height="180")
            self.alisveris_pencere.mainloop()
        except:
            yol="StokTakipSistemi\\images\\KameraKayit\\"+self.urunid2+".png"
            imj = base64.b64decode(imj)
            with open(yol,'wb') as file:
                file.write(imj)
                img = ImageTk.PhotoImage(Image.open(yol))
                self.resimler2.config(image=img,width="180",height="180")
                self.alisveris_pencere.mainloop()
     except :
        a=5
    def adet_update(self,uzunluk,event=None):
        self.varsayılan.set("Adet...")
        self.adetler =[]
        uzunluk=uzunluk
        uzunluk=int(uzunluk)
        for i in range(1,uzunluk+1):
            self.adetler.append(i)
        self.adet["values"] = self.adetler

    def satısYap(self):
        if(self.adet.get()!="Adet..." and self.müsteriler.get()!="Müsteriler..." and self.urunid!=None):
            adet = self.adet.get()
            müsteriid = self.müsteriler.get().split(",")
            müsteriid = müsteriid[1]
            urunid=self.urunid
            trh = datetime.datetime.now()
            durum="1"
            self.trh = "{}-{}-{}".format(trh.year,trh.month,trh.day)
            with self.connection.cursor() as cursor:
                try:
                    satıs_query = "INSERT INTO sts_alisveris(sts_urun_id,sts_müsteri_id,sts_urun_adet,sts_islem_tarih,sts_durum)\
                    VALUES('%s','%s','%s','%s','%s')" % (urunid,müsteriid,adet,self.trh,durum)
                    sorgu1=cursor.execute(satıs_query)
                    if(sorgu1==1):
                        adet=int(adet)
                        urun_guncelle ="UPDATE `sts_urunler` SET `urun_adet`=CAST(`urun_adet` AS UNSIGNED INTEGER)-%d WHERE urun_id=%s"%(adet,urunid)
                        cursor.execute(urun_guncelle)
                        messagebox.showinfo("Başarı","Ürün Satışı Gerçekleşti")
                        self.ürün_sorgula_classic()
                        self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
                        self.alisveris_sorgulaca_classic()
                        self.listele_alisveris(self.sts_urun_id,self.sts_urun_adi,self.sts_islem_id,self.sts_müsteri_adi,self.sts_müsteri_soyadi,self.sts_urun_adet,self.sts_islem_tarihi)
                    else:
                        return 0
                except:
                    messagebox.showerror("hata","satışta Beklenmeyen hata olustu")


        else:
            messagebox.showerror("Satıs Hatasi","Ürün Satışı yapmak için:\nÜrünü seçip, gerekli bilgileri giriniz")

    def allDelete(self):
        cevap = messagebox.askquestion("Uyarı","Tüm kayıtlar silinecek emin misiniz?")
        if(cevap=="yes"):
            with self.connection.cursor() as cursor:
                allsil="DELETE FROM sts_alisveris"
                cursor.execute(allsil)
                self.alisveris_sorgulaca_classic()
                self.listele_alisveris(self.sts_urun_id,self.sts_urun_adi,self.sts_islem_id,self.sts_müsteri_adi,self.sts_müsteri_soyadi,self.sts_urun_adet,self.sts_islem_tarihi)

        else:
            return 0

    def selectDelete(self):
         cevap = messagebox.askquestion("Uyarı","{} numaralı satış kaydı silinecektir, emin misiniz?".format(self.islemid))
         if(cevap=="yes"):
            with self.connection.cursor() as cursor:
                sil="DELETE FROM sts_alisveris WHERE sts_islem_id=%d"%int(self.islemid)
                cursor.execute(sil)
                self.alisveris_sorgulaca_classic()
                self.listele_alisveris(self.sts_urun_id,self.sts_urun_adi,self.sts_islem_id,self.sts_müsteri_adi,self.sts_müsteri_soyadi,self.sts_urun_adet,self.sts_islem_tarihi)

         else:
            return 0




    def __init__(self):
        self.lastselectionList = []
        self.connection = pymysql.connect(host='localhost',
                                                 user='root',
                                                 password='',
                                                 db='stoktakipsistemi',
                                                 charset='utf8mb4',
                                                 cursorclass=pymysql.cursors.DictCursor)

        with self.connection.cursor() as cursor:
            sql1="SELECT  * FROM sts_müsteri "
            sorgu1 = cursor.execute(sql1)
            self.Müsteriler_id = []
            self.Müsteriler_ad = []
            for i in cursor.fetchall():
                self.Müsteriler_id.append(i["müsteri_id"])
                self.Müsteriler_ad.append(i["müsteri_adi"])
        Müsteriler = []
        for i in range(len(self.Müsteriler_id)):
            Müsteriler.append("{},{}".format(self.Müsteriler_ad[i],self.Müsteriler_id[i]))

        alisveris_pencere = Toplevel()
        self.alisveris_pencere = alisveris_pencere;
        alisveris_pencere.title("Satış İşlemleri")
        alisveris_pencere.geometry("1000x560+180+50")
        #alisveris_pencere.config(bg="black")
        #alisveris_pencere.resizable(0,0)
        canvas = Canvas(alisveris_pencere,width=1000,height=560)
        myimage = PhotoImage(file = "StokTakipSistemi\\images\\arkaplan2.png")
        canvas.create_image(0,0,anchor=NW, image=myimage)

        geriButton = Button(canvas,text="Geri Gel",bg="white")
        geriButton.place(x=20,y=0)
        resimg=self.imageAdd("geri")
        geriButton.config(image=resimg,width="45", height="35",command=self.gerigel)



        baslık1 = """    Ürün İd     Ürün Ad      Ürün Adet      Ürün Tarih    Ürün Birim Fiyat"""
        baslik = Label(canvas,text=baslık1,fg="black",bg="gray",font=('Times,bold',14))
        baslik.place(x=20,y=65)
        self.scrollbar = Scrollbar(self.alisveris_pencere)
        self.listbox = Listbox(canvas,width="80",height="12",selectbackground="white",selectforeground="black",bg="black",fg="white",font=('consolas',10),yscrollcommand = self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.bind('<<ListboxSelect>>',self.listbox_select)
        self.listbox.place(x=20, y=90)



        self.resimler = Label(canvas,text="Ürün Görseli",width="25",height="12",bg="White",fg="black")
        self.resimler.place(x=770,y=90)
        self.resimler.config(width="25",height="12")

        varsayılan2 = StringVar()
        varsayılan2.set("Müsteri...")
        self.müsteriler= ttk.Combobox(canvas, textvariable=varsayılan2, state='readonly' ,width = 16)
        self.müsteriler.place(x=620,y=100)
        self.müsteriler['values'] = Müsteriler


        self.varsayılan = StringVar()
        self.varsayılan.set("Adet...")
        self.adet= ttk.Combobox(canvas, textvariable=self.varsayılan, state='readonly' ,width = 16)
        self.adet.place(x=620,y=150)


        self.satısyap = Button(canvas,text="Satış Yap",width="24",height="4",bg="#fbf8f8",font=("Times,bold","7"),command=self.satısYap)
        resimEkle=self.imageAdd("ekle")
        self.satısyap.config(image=resimEkle,width="80", height="60",compound="top")
        self.satısyap.place(x=630,y=200)

        baslık2="""   İslem No             Müşteri Adi                Ürün İD      Ürün Adi   Adet      İşlem Tarihi """
        baslik2 = Label(canvas,text=baslık2,fg="black",bg="gray",font=('Times,bold',12))
        baslik2.place(x=20,y=295)


        self.scrollbar2 = Scrollbar(self.alisveris_pencere)
        self.listbox2 = Listbox(canvas,width="80",height="12",bg="black",fg="white",font=('consolas',10),yscrollcommand = self.scrollbar.set)
        self.scrollbar2.pack(side=LEFT, fill=Y)
        self.scrollbar2.config(command=self.listbox2.yview)
        self.listbox2.bind('<<ListboxSelect>>',self.listbox2_select)
        self.listbox2.place(x=20, y=320)

        self.resimler2 = Label(canvas,text="Ürün Görseli",width="25",height="12",bg="White",fg="black")
        self.resimler2.place(x=770,y=320)
        self.resimler2.config(width="25",height="12")

        self.ürün_sorgula_classic()
        self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)

        self.alldeleteButton= Button(canvas,text="Tüm Kaydı Sil",width="24",height="4",bg="#fbf8f8",font=("Times,bold","7"),command=self.allDelete)
        kayıtsil=self.imageAdd("sil")
        self.alldeleteButton.config(image=kayıtsil,width="80", height="60",compound="top")
        self.alldeleteButton.place(x=630,y=320)


        self.selectdeleteButton= Button(canvas,text="Seçili Kaydı Sil",width="24",height="4",bg="#fbf8f8",font=("Times,bold","7"),command=self.selectDelete)
        self.selectdeleteButton.config(image=kayıtsil,width="80", height="60",compound="top")
        self.selectdeleteButton.place(x=630,y=440)

        self.alisveris_sorgulaca_classic()
        self.listele_alisveris(self.sts_urun_id,self.sts_urun_adi,self.sts_islem_id,self.sts_müsteri_adi,self.sts_müsteri_soyadi,self.sts_urun_adet,self.sts_islem_tarihi)



        canvas.pack()
        alisveris_pencere.mainloop()