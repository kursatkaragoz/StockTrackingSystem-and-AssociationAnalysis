import datetime
from STS_Giris import Giris
from tkinter import *
import pymysql.cursors
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import base64
from PIL import Image, ImageTk
import csv
from optparse import OptionParser    # parse command-line parameters
from apriori import Apriori
from tkinter import filedialog
import fpdf
import unicodedata
from tkinter import font
from time import sleep
from threading import Thread


class AnaSayfa():
    def kapat(self):

        self.anapencere.destroy()
        from STS_Anasayfa import AnaSayfa

    def imageAdd(self,uzantı):
        img = PhotoImage(file = "StokTakipSistemi\\images\\"+uzantı+".png")
        return img

    def gerigel(self):
        self.kullaniciislemleri.destroy()

    def stokPage(self):

        import STS_Urunler
        a=STS_Urunler.YetkiliPencere()

    def müsteriPage(self):

        from STS_Müsteriler import Müsteriİslemleri
        b=Müsteriİslemleri()

    def alisverisPage(self):

        import STS_Satis
        c=STS_Satis.AlisVeris()

    # RAPORLAMA HİZMETLERİ KISMI

    def dizi_temizle(self):
        self.urun_id=[]
        self.urun_adi=[]
        self.musteri_id=[]
        self.musteri_adi=[]
        self.musteri_soyadi=[]
        self.urun_adet=[]
        self.birim_fiyat=[]
        self.toplam_fiyat=[]

    def listele_rapor(self,urun_adi=[],müsteri_id=[],müsteri_adi=[],müsteri_soyadi=[],urun_adet=[],birim_fiyat=[],toplam_fiyat=[]):
        self.listbox3.delete(0,END)
        boyut = len(urun_adi)
        for i in range(0,boyut):
            cıktı="{:<3d}  {:<13s}  {:7s}  {:<14s} {:<10s}  {:<6s}  {:<10s} {:<8s}".format((i+1), müsteri_id[i],müsteri_adi[i],müsteri_soyadi[i],urun_adi[i],urun_adet[i],birim_fiyat[i],toplam_fiyat[i])
            self.listbox3.insert(END,cıktı)
            if(i%2==1):
                self.listbox3.itemconfig(i,bg="red")

    def rapor_sorgula_gunluk(self):
        if(self.gunlukrapor.get()==1):
            self.aylikrapor.set(0)
            self.yillikrapor.set(0)
            self.haftalikrapor.set(0)
            self.dizi_temizle()
            with self.connection.cursor() as cursor:
                gunluk_sorgu ="SELECT * FROM sts_alisveris AS alisveris, sts_urunler AS urunler , sts_müsteri AS müsteriler WHERE \
                alisveris.sts_islem_tarih = CURDATE() and urunler.urun_id = alisveris.sts_urun_id and müsteriler.müsteri_id = alisveris.sts_müsteri_id "
                cursor.execute(gunluk_sorgu)
                for bilgi in cursor.fetchall():
                    self.urun_id.append(bilgi["urun_id"])
                    self.urun_adi.append(bilgi["urun_ad"])
                    self.musteri_id.append(bilgi["müsteri_id"])
                    self.musteri_adi.append(bilgi["müsteri_adi"])
                    self.musteri_soyadi.append(bilgi["müsteri_soyadi"])
                    self.urun_adet.append(bilgi["sts_urun_adet"])
                    self.birim_fiyat.append(bilgi["urun_fiyat"])
                    adet = int(bilgi["sts_urun_adet"])
                    birim = float(bilgi["urun_fiyat"])
                    toplamfiyat = adet * birim
                    toplamfiyat="%.2f" % toplamfiyat
                    self.toplam_fiyat.append(toplamfiyat)
            self.listele_rapor(self.urun_adi,self.musteri_id,self.musteri_adi,self.musteri_soyadi,self.urun_adet,self.birim_fiyat,self.toplam_fiyat)
    def rapor_sorgula_haftalik(self):
        if(self.haftalikrapor.get()==1):
            self.gunlukrapor.set(0)
            self.aylikrapor.set(0)
            self.yillikrapor.set(0)
            self.dizi_temizle()
            with self.connection.cursor() as cursor:
                haftaliksorgu ="SELECT * FROM sts_alisveris AS alisveris, sts_urunler AS urunler , sts_müsteri AS müsteriler WHERE \
                YEARWEEK(alisveris.sts_islem_tarih) = YEARWEEK(CURRENT_DATE()) and urunler.urun_id = alisveris.sts_urun_id and müsteriler.müsteri_id = alisveris.sts_müsteri_id "
                cursor.execute(haftaliksorgu)
                for bilgi in cursor.fetchall():
                    self.urun_id.append(bilgi["urun_id"])
                    self.urun_adi.append(bilgi["urun_ad"])
                    self.musteri_id.append(bilgi["müsteri_id"])
                    self.musteri_adi.append(bilgi["müsteri_adi"])
                    self.musteri_soyadi.append(bilgi["müsteri_soyadi"])
                    self.urun_adet.append(bilgi["sts_urun_adet"])
                    self.birim_fiyat.append(bilgi["urun_fiyat"])
                    adet = int(bilgi["sts_urun_adet"])
                    birim = float(bilgi["urun_fiyat"])
                    toplamfiyat = adet * birim
                    toplamfiyat="%.2f" % toplamfiyat
                    self.toplam_fiyat.append(toplamfiyat)
            self.listele_rapor(self.urun_adi,self.musteri_id,self.musteri_adi,self.musteri_soyadi,self.urun_adet,self.birim_fiyat,self.toplam_fiyat)


    def rapor_sorgula_aylik(self):
        if(self.aylikrapor.get()==1):
            self.gunlukrapor.set(0)
            self.yillikrapor.set(0)
            self.haftalikrapor.set(0)
            self.dizi_temizle()
            with self.connection.cursor() as cursor:
                ayliksorgu ="SELECT * FROM sts_alisveris AS alisveris, sts_urunler AS urunler , sts_müsteri AS müsteriler WHERE \
                alisveris.sts_islem_tarih >= DATE_SUB(CURDATE(),INTERVAL 1 MONTH) and urunler.urun_id = alisveris.sts_urun_id and müsteriler.müsteri_id = alisveris.sts_müsteri_id "
                cursor.execute(ayliksorgu)
                for bilgi in cursor.fetchall():
                    self.urun_id.append(bilgi["urun_id"])
                    self.urun_adi.append(bilgi["urun_ad"])
                    self.musteri_id.append(bilgi["müsteri_id"])
                    self.musteri_adi.append(bilgi["müsteri_adi"])
                    self.musteri_soyadi.append(bilgi["müsteri_soyadi"])
                    self.urun_adet.append(bilgi["sts_urun_adet"])
                    self.birim_fiyat.append(bilgi["urun_fiyat"])
                    adet = int(bilgi["sts_urun_adet"])
                    birim = float(bilgi["urun_fiyat"])
                    toplamfiyat = adet * birim
                    toplamfiyat="%.2f" % toplamfiyat
                    self.toplam_fiyat.append(toplamfiyat)
            self.listele_rapor(self.urun_adi,self.musteri_id,self.musteri_adi,self.musteri_soyadi,self.urun_adet,self.birim_fiyat,self.toplam_fiyat)

    def rapor_sorgula_yillik(self):
        if(self.yillikrapor.get()==1):
            self.gunlukrapor.set(0)
            self.aylikrapor.set(0)
            self.haftalikrapor.set(0)
            self.dizi_temizle()
            with self.connection.cursor() as cursor:
                yilliksorgu ="SELECT * FROM sts_alisveris AS alisveris, sts_urunler AS urunler , sts_müsteri AS müsteriler WHERE \
                alisveris.sts_islem_tarih >= DATE_SUB(CURDATE(),INTERVAL 1 YEAR) and urunler.urun_id = alisveris.sts_urun_id and müsteriler.müsteri_id = alisveris.sts_müsteri_id "
                cursor.execute(yilliksorgu)
                for bilgi in cursor.fetchall():
                    self.urun_id.append(bilgi["urun_id"])
                    self.urun_adi.append(bilgi["urun_ad"])
                    self.musteri_id.append(bilgi["müsteri_id"])
                    self.musteri_adi.append(bilgi["müsteri_adi"])
                    self.musteri_soyadi.append(bilgi["müsteri_soyadi"])
                    self.urun_adet.append(bilgi["sts_urun_adet"])
                    self.birim_fiyat.append(bilgi["urun_fiyat"])
                    adet = int(bilgi["sts_urun_adet"])
                    birim = float(bilgi["urun_fiyat"])
                    toplamfiyat = adet * birim
                    toplamfiyat="%.2f" % toplamfiyat
                    self.toplam_fiyat.append(toplamfiyat)
            self.listele_rapor(self.urun_adi,self.musteri_id,self.musteri_adi,self.musteri_soyadi,self.urun_adet,self.birim_fiyat,self.toplam_fiyat)

    def to_pdf(self):
        self.dizi1=[]
        self.sonuclar=[]
        tpfiyat=0.0

        if(self.urun_adi is not None):
            for fiyat in self.toplam_fiyat:
                tpfiyat = tpfiyat + float(fiyat)
            tpfiyat = "{%.2f}"% tpfiyat
            for i in range(0,len(self.urun_adi)):
                    self.dizi1.append(self.urun_id[i])
                    self.dizi1.append(self.urun_adi[i])
                    müsteriname = "{} {}".format(self.musteri_adi[i],self.musteri_soyadi[i])
                    self.dizi1.append(müsteriname)
                    self.dizi1.append(self.urun_adet[i])
                    self.dizi1.append(self.birim_fiyat[i])
                    self.dizi1.append(self.toplam_fiyat[i])
                    print(self.dizi1)
                    self.sonuclar.append(self.dizi1)
                    self.dizi1=[]
            print(self.sonuclar)

            f = filedialog.asksaveasfilename(initialdir="/", title="Select file", defaultextension=".pdf",filetypes=[('pdf file', '*.pdf')])
            tim = datetime.datetime.now()
            pdf = fpdf.FPDF(format='letter')
            pdf.add_page()
            pdf.set_font("Times", size=10)
            pdf.cell(350, 5, txt=str(tim), ln=1, align="C")
            if(self.gunlukrapor.get()==1):
                pdf.cell(200, 10, txt="Stok Takip Sistemi Gunluk Rapor", ln=1, align="C")
            if(self.haftalikrapor.get()==1):
                pdf.cell(200, 10, txt="Stok Takip Sistemi Haftalik Rapor", ln=1, align="C")
            if(self.aylikrapor.get()==1):
                pdf.cell(200, 10, txt="Stok Takip Sistemi Aylik Rapor", ln=1, align="C")
            if(self.yillikrapor.get()==1):
                pdf.cell(200, 10, txt="Stok Takip Sistemi Yillik Rapor", ln=1, align="C")

            baslik = """Urun Id           Urun Adi                  Musteri Adi        Urun Adet          Fiyat(B,Kg)       Fiyat(Toplam)"""
            baslik ="{:^28} {:^28} {:^28} {:^28} {:^28} {:^28} ".format("Urun Id","Urun Adi","Müsteri Adi","Urun Adet","Fiyat(B,Kg)","Fiyat(Toplam)")
            pdf.cell(180, 10, txt=baslik, ln=1, align="C")
            i=0
            col_width = pdf.w / 7.0
            row_height = pdf.font_size
            for row in self.sonuclar:
                for item in row:
                    item = str(unicodedata.normalize('NFKD',item).encode('ascii', 'ignore'))
                    item = item[2:len(item)-1]
                    pdf.cell(col_width, row_height*1,txt=item, border=1,align="C")
                pdf.ln(row_height*1)

            pdf.cell(200, 10, txt="Toplam Urun Satis Fiyati : {} TL,$,£".format(tpfiyat), ln=1, align="C")
            pdf.output(f)



    def Raporlama_Gui(self):
        self.connection = pymysql.connect(host='localhost',
                                                 user='root',
                                                 password='',
                                                 db='stoktakipsistemi',
                                                 charset='utf8mb4',
                                                 cursorclass=pymysql.cursors.DictCursor)
        raporlama_pencere = Toplevel()
        self.raporlama_pencere = raporlama_pencere;
        raporlama_pencere.title("Raporlama Hizmeti")
        raporlama_pencere.geometry("900x360+250+50")
        #raporlama_pencere.config(bg="black")
        #raporlama_pencere.resizable(0,0)
        canvas = Canvas(raporlama_pencere,width=900,height=360)
        myimage = PhotoImage(file = "StokTakipSistemi\\images\\arkaplan2.png")
        canvas.create_image(0,0,anchor=NW, image=myimage)

        geriButton = Button(canvas,text="Geri Gel",bg="red")
        geriButton.place(x=20,y=0)
        resimg=self.imageAdd("geri")
        geriButton.config(image=resimg,width="45", height="35",command=self.raporlama_pencere.destroy)

        baslık2="""    Müşteri İD               Müşteri Adi                 Ürün Adi       Adet     Birim Fiyat   Toplam Fiyat """
        baslik2 = Label(canvas,text=baslık2,width="66",fg="black",bg="gray",font=('Times',12))
        baslik2.place(x=20,y=75)

        self.scrollbar3 = Scrollbar(self.raporlama_pencere)
        self.listbox3 = Listbox(canvas,width="85",height="13",bg="black",fg="white",font=('consolas',10),yscrollcommand = self.scrollbar3.set)
        self.scrollbar3.pack(side=LEFT, fill=Y)
        self.scrollbar3.config(command=self.listbox3.yview)
        self.listbox3.place(x=20, y=100)

        self.gunlukrapor =IntVar()
        self.Check_id_button = Checkbutton(canvas , text="Günlük Veriler" , variable = self.gunlukrapor , onvalue = 1 , offvalue = 0 ,height = 1, width="12",bg="white",fg="black",font=("Times","10","bold italic"),command=self.rapor_sorgula_gunluk)
        self.Check_id_button.place(x=630,y=100)

        self.haftalikrapor =IntVar()
        self.Check_id2_button = Checkbutton(canvas , text="Haftalık Veriler" , variable = self.haftalikrapor , onvalue = 1 , offvalue = 0 ,height = 1, width="12",bg="white",fg="black",font=("Times","10","bold italic"),command=self.rapor_sorgula_haftalik)
        self.Check_id2_button.place(x=630,y=130)

        self.aylikrapor =IntVar()
        self.Check_id3_button = Checkbutton(canvas , text="Aylık Veriler " , variable = self.aylikrapor , onvalue = 1 , offvalue = 0 ,height = 1, width="12",bg="white",fg="black",font=("Times","10","bold italic"),command=self.rapor_sorgula_aylik)
        self.Check_id3_button.place(x=630,y=160)

        self.yillikrapor =IntVar()
        self.Check_id_button = Checkbutton(canvas , text="Yıllık Veriler  " , variable = self.yillikrapor , onvalue = 1 , offvalue = 0 ,height = 1, width="12",bg="white",fg="black",font=("Times","10","bold italic"),command=self.rapor_sorgula_yillik)
        self.Check_id_button.place(x=630,y=190)

        self.pdfsave = Button(canvas,text="Sonuçları Kaydet        ",width="196",height="24",bg="#fbf8f8",command=self.to_pdf)
        self.pdfsave.place(x=630,y=280)
        resimpdf=self.imageAdd("pdf")
        self.pdfsave.config(image=resimpdf,width="196", height="24",compound="right")

        canvas.pack()
        raporlama_pencere.mainloop()




    def kaydet_guncel(self,event=None):

        if(self.ad.get()=="" or self.soyad.get()=="" or self.sifre.get()=="" or self.posta.get()=="" or self.telefon.get()==""):
             messagebox.showinfo("Bos Alan","Bos Alanlari Doldurunuz")
        else:
            self.kn = self.kimlik.get()
            self.kn = int(self.kn)
            self.name = self.ad.get()
            self.surname = self.soyad.get()
            self.pas = self.sifre.get()
            self.tel = self.telefon.get()
            self.mail = self.posta.get()

            with self.connection.cursor() as cursor:
                cursor.execute ("UPDATE sts_yetkili SET yetkili_adi = '%s' , yetkili_soyadi = '%s' , yetkili_sifre = '%s' , yetkili_posta = '%s' , yetkili_cepno = '%s' WHERE yetkili_id = '%d'"\
                % (self.name , self.surname , self.pas , self.mail , self.tel , self.kn) )
                messagebox.showinfo("BAŞARI","Bilgileriniz Kaydedildi.")
                self.kullaniciislemleri.destroy()

######################################### ÇARK BUTONU  ADMİN İŞLEMLERİ BAŞLADI ############################################
    def kullanici_islemleri(self,event=None):

        self.connection = pymysql.connect(host='localhost',
                                                 user='root',
                                                 password='',
                                                 db='stoktakipsistemi',
                                                 charset='utf8mb4',
                                                 cursorclass=pymysql.cursors.DictCursor)
        kullaniciislemleri = Toplevel()
        self.kullaniciislemleri = kullaniciislemleri;
        kullaniciislemleri.title("Kullanıcı İslemleri")
        kullaniciislemleri.geometry("320x460+520+100")
        kullaniciislemleri.resizable(0,0)
        canvaskullanıcı = Canvas(kullaniciislemleri,width=350,height=480)
        myimage = PhotoImage(file = "StokTakipSistemi\\images\\anasayfa.png")
        canvaskullanıcı.create_image(0,0,anchor=NW, image=myimage)


        geriButton = Button(canvaskullanıcı,text="Geri Gel",command=self.gerigel)
        geriButton.place(x=140,y=20)
        resim1=self.imageAdd("geri")
        geriButton.config(image=resim1,width=50, height=25)


        kimliklb = Label(canvaskullanıcı,text="Kimlik No ",width=10)
        kimliklb.place(x=50,y=80)
        self.kimlik = Entry(canvaskullanıcı)
        self.kimlik.place(x=140,y=80)


        adlb = Label(canvaskullanıcı, text="Ad  ",width=10)
        adlb.place(x=50, y=120)
        self.ad = Entry(canvaskullanıcı)
        self.ad.place(x=140, y=120)

        soyadlb = Label(canvaskullanıcı, text="Soyad:   ",width=10)
        soyadlb.place(x=50, y=160)
        self.soyad = Entry(canvaskullanıcı)
        self.soyad.place(x=140, y=160)

        sifrelb = Label(canvaskullanıcı, text="Sifre  ",width=10)
        sifrelb.place(x=50, y=200)
        self.sifre = Entry(canvaskullanıcı,show="*")
        self.sifre.place(x=140, y=200)


        telefonlb = Label(canvaskullanıcı, text="Telefon   ",width=10)
        telefonlb.place(x=50, y=240)
        self.telefon = Entry(canvaskullanıcı)
        self.telefon.place(x=140, y=240)

        postalb = Label(canvaskullanıcı, text="E-Posta   ",width=10)
        postalb.place(x=50, y=280)
        self.posta = Entry(canvaskullanıcı)
        self.posta.place(x=140, y=280)

        self.kaydet = Button(canvaskullanıcı,text="Kaydet",command=self.kaydet_guncel)
        self.kaydet.place(x=110,y=320)
        resim=self.imageAdd("giris")
        self.kaydet.config(image =resim, width = 85 , height = 30,command=self.kaydet_guncel)
        kullaniciislemleri.bind('<Return>',self.kaydet_guncel)





        with self.connection.cursor() as cursor:
            bilgilerin="SELECT * FROM  `sts_yetkili` WHERE yetkili_posta= '%s'"% (self.kullaniciadi)
            sonuc=cursor.execute(bilgilerin)
            print(bilgilerin)
            if (sonuc==1):  ##sonuc 1 ise posta ile giriş yapılmıştırpostaya göre bilgilere ulaşılır
                for i in cursor.fetchall():
                    self.kimlikno = i["yetkili_id"]
                    self.isim = i["yetkili_adi"]
                    self.soyisim = i["yetkili_soyadi"]
                    self.password = i["yetkili_sifre"]
                    self.eposta = i["yetkili_posta"]
                    self.cepnumara = i["yetkili_cepno"]
            if(sonuc==0):   ###sonuc 0 ise id ile giriş yapılmıştır
                bilgilerin="SELECT * FROM  `sts_yetkili` WHERE yetkili_id= '%d'"% (int(self.kullaniciadi))
                cursor.execute(bilgilerin)
                for i in cursor.fetchall():
                    self.kimlikno = i["yetkili_id"]
                    self.isim = i["yetkili_adi"]
                    self.soyisim = i["yetkili_soyadi"]
                    self.password = i["yetkili_sifre"]
                    self.eposta = i["yetkili_posta"]
                    self.cepnumara = i["yetkili_cepno"]




        self.kimlik.insert(END,self.kimlikno)
        self.kimlik.configure(state="readonly")
        self.ad.insert(END,self.isim)
        self.soyad.insert(END,self.soyisim)
        self.sifre.insert(END,self.password)
        self.telefon.insert(END,self.cepnumara)
        self.posta.insert(END,self.eposta)

        canvaskullanıcı.pack()
        kullaniciislemleri.mainloop()


    def birliktelik(self):
        import apriori_gui
        apri_run = apriori_gui.Birliktelik()

    def dataset_import(self):
        self.listbox3.delete(0,"end")
        self.filename = filedialog.askopenfilename(initialdir="\\", title="Select file",
                                                  filetypes=[("CSV Files",".csv")])
        self.Degerler =[]
        self.liste=[]
        with open(self.filename, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                self.liste.append(row)
                for i in range (0,len(row)):
                    if (row[i] in self.Degerler) == False:
                            self.Degerler.append(row[i])
        print(self.Degerler)
        csvFile.close()

        for i in range(0,len(self.liste)):
            self.listbox3.insert(END,"{}. Müsteri: {}".format(i+1,self.liste[i]))

    def topdf(self):
        #try:
            b=0
            index=0
            if(self.sonuclar is not None):
                f = filedialog.asksaveasfilename(initialdir="/", title="Select file", defaultextension=".pdf",filetypes=[('pdf file', '*.pdf')])
                tim = datetime.datetime.now()
                pdf = fpdf.FPDF(format='letter')
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(350, 5, txt=str(tim), ln=1, align="C")
                pdf.cell(200, 10, txt="Birliktelik Analizi Raporu", ln=1, align="C")
                pdf.cell(50, 10, txt="Olusan Gruplamalar", ln=1, align="C")
                for index in range(0,len(self.itemtutucu)):
                    item = "{}".format(self.itemtutucu[index])
                    itemler = str(unicodedata.normalize('NFKD',item).encode('ascii', 'ignore'))
                    itemler = itemler[2:len(itemler)-1]
                    pdf.write(5,itemler)
                    pdf.ln()
                pdf.ln()
                pdf.cell(200, 10, txt="Gruplamalar Sonucu Olusan Tum Kurallar", ln=1, align="C")
                pdf.ln()
                for b in range(0,len(self.sonuclar)):
                    sonuc = "{}".format(self.sonuclar[b])
                    sonuclar = str(unicodedata.normalize('NFKD',sonuc).encode('ascii', 'ignore'))
                    sonuclar = sonuclar[2:len(sonuclar)-1]
                    pdf.write(5,sonuclar)
                    pdf.ln()
                pdf.output(f)
            else:
                return 0
        #except:
            #b=0

    def start_apriori(self):
        if(self.destek.get()=="" or self.guven.get()=="" or self.Degerler[0] == ""):
            messagebox.showwarning("Eksik Bilgi","Birliktelik Analizinin Yapılabilmesi için \nDestek ve Güven Ölçütleri Girilmelidir")
        else:

            self.dstk = float(self.destek.get())
            self.gvn = float(self.guven.get())
            self.sonuclar=[]
            self.itemtutucu=[]
            a=0
            for sayac in range(0,len(self.Degerler)):
                # Get two important parameters
                self.filePath = self.filename
                self.minSupp  = self.dstk
                self.minConf  = self.gvn
                deger = self.Degerler[sayac]
                self.rhs      = frozenset([deger])
                print("""Minimum Destek: {} \n Minimum Güven: {} \n İncelenen Ürün: {}\n""".\
                      format(self.minSupp,self.minConf, self.rhs))
                incelenen = """Minimum Destek: {} \n Minimum Güven: {} \n İncelenen Ürün: {}\n""".\
                      format(self.minSupp,self.minConf, self.rhs)
                self.listbox3.insert(END,incelenen)

                # Run and print
                objApriori = Apriori(self.minSupp, self.minConf)
                itemCountDict, freqSet = objApriori.fit(self.filePath)

                c=1
                for key, value in freqSet.items():
                    print('frequent {}-term set:'.format(key))
                    print('-'*20)
                    if(a==0):
                            self.itemtutucu.append("-------------------------------")
                            self.itemtutucu.append("-----{}'erli Gruplamalar-----".format(c))
                            self.itemtutucu.append("-------------------------------")
                            c=c+1
                    for itemset in value:
                        print(list(itemset))
                        if(a==0):

                            self.itemtutucu.append(list(itemset))
                a=1

                # Return rules with regard of `rhs`
                rules = objApriori.getSpecRules(self.rhs)
                print('-'*20)

                self.sonuclar.append('------------------------------------------')
                self.sonuclar.append('Oluşan Kurallar Bu Ürün için: {}'.format(list(self.rhs)))
                self.sonuclar.append('')
                for key, value in rules.items():
                    if(value > 0.5):
                        cıktı = '{} -> {}: {}'.format(list(key), list(self.rhs), value)
                        self.sonuclar.append(cıktı) ######### Ben değiştirdim

            for row in range(0,len(self.itemtutucu)):
                self.listbox3.insert(END,self.itemtutucu[row])

            print("SONUCLAR\n")
            self.listbox3.insert(END,"---------SONUCLAR----------")
            for i in range(0,len(self.sonuclar)):
                self.listbox3.insert(END,"{} {}".format(i+1,self.sonuclar[i]))
                print(self.sonuclar[i])

    def birliktelik_extra_gui(self):
        analiz_pencere = Toplevel()
        self.analiz_pencere = analiz_pencere;
        analiz_pencere.title("Yeni Birliktelik Analizi")
        analiz_pencere.geometry("900x360+250+50")
        #analiz_pencere.config(bg="black")
        #analiz_pencere.resizable(0,0)
        canvas = Canvas(analiz_pencere,width=900,height=360)
        myimage = PhotoImage(file = "StokTakipSistemi\\images\\arkaplan2.png")
        canvas.create_image(0,0,anchor=NW, image=myimage)

        geriButton = Button(canvas,text="Geri Gel",bg="red")
        geriButton.place(x=20,y=0)
        resimg=self.imageAdd("geri")
        geriButton.config(image=resimg,width="45", height="35",command=self.analiz_pencere.destroy)



        baslık2=" VERİ SETİ"
        baslik2 = Label(canvas,text=baslık2,width="62",fg="black",bg="gray",font=('Times,bold',12))
        baslik2.place(x=20,y=75)

        self.scrollbar3 = Scrollbar(self.analiz_pencere)
        self.listbox3 = Listbox(canvas,width="80",height="13",bg="black",fg="white",font=('consolas',10),yscrollcommand = self.scrollbar3.set)
        self.scrollbar3.pack(side=LEFT, fill=Y)
        self.scrollbar3.config(command=self.listbox3.yview)
        self.listbox3.place(x=20, y=100)

        self.dataset = Button(canvas,text="Veri Seti Yükle",width="27",bg="white",command=self.dataset_import)
        self.dataset.place(x=630,y=105)

        self.desteklabel = Label(canvas,text="Destek Eşik:",width="12")
        self.desteklabel.place(x=630,y=175)
        self.destek = Entry(canvas,width="12")
        self.destek.place(x=730,y=175)

        self.guvenlabel = Label(canvas,text="Güven Eşik:",width="12")
        self.guvenlabel.place(x=630,y=205)
        self.guven = Entry(canvas,width="12")
        self.guven.place(x=730,y=205)

        self.analiz = Button(canvas,text="Analize Başla    ", width="196", height="24",bg="#fbf8f8",command=self.start_apriori)
        self.analiz.place(x=630,y=245)
        resimanaliz=self.imageAdd("analiz")
        self.analiz.config(image=resimanaliz,width="196", height="24",compound="right")

        self.pdfsave = Button(canvas,text="Sonuçları Kaydet        ",width="196",height="24",bg="#fbf8f8",command=self.topdf)
        self.pdfsave.place(x=630,y=280)
        resimpdf=self.imageAdd("pdf")
        self.pdfsave.config(image=resimpdf,width="196", height="24",compound="right")



        canvas.pack()
        analiz_pencere.mainloop()

    def uyarilacaklar_sorgula(self):
        self.uyarilacaklar_id=[]
        self.uyarilacaklar_ad=[]
        self.uyarilacaklar_adet=[]
        with self.connection.cursor() as cursor:
            stok_uyarı="SELECT * FROM sts_urunler WHERE urun_adet < 11"
            d=cursor.execute(stok_uyarı)
            if(d >0):
                print("tmm")
            for kolon in cursor.fetchall():
                self.uyarilacaklar_id.append(kolon["urun_id"])
                self.uyarilacaklar_ad.append(kolon["urun_ad"])
                self.uyarilacaklar_adet.append(kolon["urun_adet"])
        print(self.uyarilacaklar_id)

    def uyarilacaklar_listele(self,ürünid=[],ürünad=[],ürünadet=[]):

        self.list_uyarilacaklar.delete(0,END)
        self.boyut = len(self.uyarilacaklar_id)
        for i in range(0,self.boyut):
            cıktı="{:<10d}  {:<15s}  {:<16s}  {:<16s} ".format((i+1), ürünid[i],ürünad[i],ürünadet[i])
            self.list_uyarilacaklar.insert(END,cıktı)
            #self.list_uyarilacaklar.itemconfig(0,bg="red")
            if(i%2==1):
                self.list_uyarilacaklar.itemconfig(i,bg="gray")

    def uyarilacak_guncelle(self,urunid,i,event=None):
        self.uyarilacakGUI.destroy()
        self.urunid_get = str(urunid)
        with self.connection.cursor() as cursor:
            uyarilacakid = "INSERT INTO sts_kayıt(uye_kullaniciadi,uye_sifre)\
                    VALUES('%s','%s')" % (self.urunid_get,'silinecek')
            cursor.execute(uyarilacakid)
        from STS_Urunler import YetkiliPencere
        urunguncellepage = YetkiliPencere()

    def uyarilacaklar_gui(self):
        if(self.uyarilacakadet !=0):
            uyarilacaklar = Toplevel()
            self.uyarilacaklar = uyarilacaklar
            self.uyarilacakGUI = uyarilacaklar
            uyarilacaklar.title("Stok Durumu Azalanlar")
            uyarilacaklar.geometry("600x460+400+60")
            uyarilacaklar.resizable(0,0)
            canvas = Canvas(uyarilacaklar,width=600,height=460)
            self.canvas = canvas
            myimage = PhotoImage(file = "StokTakipSistemi\\images\\arkaplan2.png")
            canvas.create_image(0,0,anchor=NW, image=myimage)
            kapatButton = Button(canvas,text="Kapat")
            kapatButton.place(x=265,y=7)
            resim2=self.imageAdd("kapat")
            kapatButton.config(image=resim2,width="45", height="35",command=self.anapencere.destroy)

            baslik="""           Ürün Kodu        Ürün Adı       Stok Durumu                             """
            self.baslik=Label(canvas,text=baslik,fg="black",bg="gray",font=('Times,bold',14))
            self.baslik.place(x=10,y=55)
            self.scrollbar = Scrollbar(self.anapencere)
            self.list_uyarilacaklar = Listbox(canvas,width="62",height="20",bg="white",selectbackground="red",fg="black",font=('consolas',"10"),yscrollcommand = self.scrollbar.set)
            self.scrollbar.pack(side=RIGHT, fill=Y)
            self.scrollbar.config(command=self.list_uyarilacaklar.yview)
            #self.list_uyarilacaklar.bind('<<ListboxSelect>>',self.listbox_select)
            self.list_uyarilacaklar.place(x=10, y=80)
            self.uyarilacaklar_sorgula()
            self.uyarilacaklar_listele(self.uyarilacaklar_id,self.uyarilacaklar_ad,self.uyarilacaklar_adet)
            a=82
            images_add=self.imageAdd("ekle")
            self.uyarilacakButton=[]
            for i in range(0,len(self.uyarilacaklar_id)):

                self.uyarilacakButton.append(Button(canvas,text="%d Stok Güncelle" % i))
                self.uyarilacakButton[i].place(x=450,y=a)
                self.uyarilacakButton[i].bind('<Button-1>', partial(self.uyarilacak_guncelle,self.uyarilacaklar_id[i],i))
                self.uyarilacakButton[i].config(image=images_add,width="108",height="7",compound="right")

                a=a+16

            canvas.pack()
            uyarilacaklar.mainloop()
        else:
            messagebox.showinfo("Uyarı","Ürün Stoklarında Problem Görülmemektedir.")

    def uyarilacak_thread(self,ne,time):
        self.uyarilacakadet=0

        self.connection3 = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='',
                                                     db='stoktakipsistemi',
                                                     charset='utf8mb4',
                                                     cursorclass=pymysql.cursors.DictCursor)
        #try:
        while True:
            count=0
            with self.connection3.cursor() as cursor3:
                stok_uyarı="SELECT urun_id FROM sts_urunler WHERE urun_adet < 11"
                cursor3.execute(stok_uyarı)
                for kolon in cursor3.fetchall():
                    count = count+1

                self.sonuc.set(str(count))
                self.uyarilacakadet = int(count)

            sleep(time)
        #except:
            #print("uyarılacaklarda kimse yok")



    def __init__(self):
        giris = Giris()
        kullanıcıadı = giris.k_adi
        self.giris_turu = giris.giris_turu
        self.kullaniciadi=kullanıcıadı

        self.connection = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='',
                                                     db='stoktakipsistemi',
                                                     charset='utf8mb4',
                                                     cursorclass=pymysql.cursors.DictCursor)

        self.uyarilacaklar=[]
        if(self.giris_turu=="Admin"):
            try:
                with self.connection.cursor() as cursor:
                    a=9
                    stok_uyarı="SELECT * FROM sts_urunler WHERE urun_adet < 11"
                    d=cursor.execute(stok_uyarı)
                    if(d >0):
                        print("tmm")
                    for kolon in cursor.fetchall():
                        self.uyarilacaklar.append(kolon["urun_id"])


                    print(self.uyarilacaklar)
            except:
                print("uyarılacaklarda kimse yok")

            anapencere = Tk()
            self.anapencere = anapencere
            anapencere.title("Ana Sayfa")
            anapencere.geometry("380x480+500+60")
            anapencere.resizable(0,0)
            canvas = Canvas(anapencere,width=380,height=480)
            self.canvas = canvas
            myimage = PhotoImage(file = "StokTakipSistemi\\images\\anasayfa.png")
            canvas.create_image(0,0,anchor=NW, image=myimage)

            menu = Menu(canvas)
            filemenu = Menu(menu,tearoff=0)
            menu.add_cascade(label="İşlemler", menu=filemenu)
            filemenu.add_command(label="Birliktelik Analizi",command=self.birliktelik)
            filemenu.add_command(label="Yeni Analiz",command=self.birliktelik_extra_gui)
            filemenu.add_command(label="Raporlama",command=self.Raporlama_Gui)
            filemenu.add_separator()
            kullanicimenu = Menu(menu,tearoff=0)
            menu.add_cascade(label="Kulanıcı İşlemleri...", menu=kullanicimenu)
            kullanicimenu.add_command(label="Bilgi Güncellemesi",command=self.kullanici_islemleri)

            kullanicimenu.add_separator()
            anapencere.config(menu=menu)

            sayi=len(self.uyarilacaklar)
            self.sonuc2=" {}".format(sayi)
            self.sonuc=StringVar()
            self.sonuc.set(self.sonuc2)
            uyari = Button(canvas,textvariable=self.sonuc,bg="white",command=self.uyarilacaklar_gui)
            uyari.place(x=328,y=0)
            resimuyari=self.imageAdd("uyarı")
            uyari.config(image=resimuyari,width="42",height="40",compound="top")

            kapatButton = Button(canvas,text="Kapat")
            kapatButton.place(x=165,y=20)
            resim2=self.imageAdd("kapat")
            kapatButton.config(image=resim2,width="45", height="35",command=self.kapat)

            self.hosgeldin = Label(canvas,text=self.kullaniciadi,width="25")
            self.hosgeldin.place(x=100, y=80)

            self.stok_islemleri = Button(canvas,text="Stok İşlemleri",width="24",height="5",command=self.stokPage,bg="gray",fg="white")
            self.stok_islemleri.place(x=85,y=120)
            resimstok=self.imageAdd("stok")
            self.stok_islemleri.config(image=resimstok,width="200",height="94",compound="top")
            self.stok_islemleri.configure(font=('Times',"12"))

            self.müsteri_islemleri = Button(canvas,text="Müşteri İşlemleri",width="24",height="4", command=self.müsteriPage,bg="gray",fg="white")
            self.müsteri_islemleri.place(x=85,y=235)
            resimmüsteri=self.imageAdd("müsteri")
            self.müsteri_islemleri.config(image=resimmüsteri,width="200", height="94",compound="top")
            self.müsteri_islemleri.configure(font=('Times',"12"))

            self.ürün_islemleri = Button(canvas,text="Ürün Satış İşlemleri",width="24",height="4",command=self.alisverisPage,bg="gray",fg="white")
            self.ürün_islemleri.place(x=85,y=350)
            resimsatıs=self.imageAdd("satıs")
            self.ürün_islemleri.config(image=resimsatıs,width="200", height="94",compound="top")
            self.ürün_islemleri.configure(font=('Times',"12"))

            uyarilacak_kontrol = Thread(target=self.uyarilacak_thread ,args=("Thread Uyarilacak",3))
            uyarilacak_kontrol.start()
            self.urunsayisi = self.sonuc2

            canvas.pack()
            anapencere.mainloop()
################################################################### MÜŞTERİ İŞLEMLERİ ###########################################################
        if(self.giris_turu=="Müsteri"):

            self.connection = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='',
                                                     db='stoktakipsistemi',
                                                     charset='utf8mb4',
                                                     cursorclass=pymysql.cursors.DictCursor)
            ### BURADA ÜRÜN İD'E ERİŞ DAHA SONRA ÜRÜN İD DEN SEPETTEKİ BİLGİLERİ ÇEK DURUM 0 OLANLARI 0'A EKLE
            #with self.connection.cursor() as cursor:

            try:
                with self.connection.cursor() as cursor:
                    kullanici_kim="SELECT müsteri_id FROM sts_müsteri WHERE müsteri_posta=%s"
                    d=cursor.execute(kullanici_kim,self.kullaniciadi)
                    if(d==1):
                        print("tmm")
                    for kolon in cursor.fetchall():
                        self.kullaniciadi=kolon["müsteri_id"]
            except:
                self.kullaniciadi=self.kullaniciadi
            self.sepet_sorgula()   ##sepetteki ürü sayıını bulmak için calıstırıldı
            anapencere = Tk()
            self.anapencere = anapencere;
            anapencere.title("Müşteri Ana Sayfa")
            anapencere.geometry("800x560+300+50")
            #anapencere.resizable(0,0)
            canvas = Canvas(anapencere,width=800,height=560)
            myimage = PhotoImage(file = "StokTakipSistemi\\images\\arkaplan2.png")
            canvas.create_image(0,0,anchor=NW, image=myimage)

            cark2 = Button(canvas,text=self.kullaniciadi,font=("Times","10"),bg="white",activebackground="white",command=self.müsteri_islemleri)
            cark2.place(x=0,y=0)
            resimcark2=self.imageAdd("cark")
            cark2.config(image=resimcark2,width="120",height="30",compound="left")



            kapatButton = Button(canvas,text="Kapat",bg="white")
            kapatButton.place(x=370,y=0)
            resim2=self.imageAdd("kapat")
            kapatButton.config(image=resim2,width="45", height="35",command=self.anapencere.destroy)


            self.sepet = Button(canvas,width="24",height="4",bg="white",activebackground="white",command=self.sepet_gui)
            self.sepet['text']="{}".format(self.toplam_urun)
            self.sepet.place(x=710,y=0)
            resimEkle=self.imageAdd("sepet")
            self.sepet.config(image=resimEkle,width="68", height="60",compound="top")

            self.resimlerMüsteri = Label(canvas,text="Ürün Görseli",width="30",height="12",bg="White",fg="black")
            self.resimlerMüsteri.place(x=590,y=95)
            self.resimlerMüsteri.config(width="25",height="12")

            baslik="""           Ürün Kodu        Ürün Adı       Stok Durumu        Birim Fiyatı    """
            self.baslik=Label(canvas,text=baslik,fg="black",bg="gray",font=('Times,bold',14))
            self.baslik.place(x=10,y=95)
            self.scrollbar = Scrollbar(self.anapencere)
            self.listbox = Listbox(canvas,width="80",height="27",bg="white",selectbackground="red",fg="black",font=('consolas',"10"),yscrollcommand = self.scrollbar.set,selectmode="multiple")
            self.scrollbar.pack(side=RIGHT, fill=Y)
            self.lastselectionList=[]
            self.idler=[]

            self.scrollbar.config(command=self.listbox.yview)
            self.listbox.bind('<<ListboxSelect>>',self.listbox_select)
            self.listbox.place(x=10, y=120)


            self.sepete_ekle = Button(canvas,text="Sepete Ekle",width="24",height="4",bg="white",command=self.sepet_add,activebackground ="white")
            self.sepete_ekle.place(x=590,y=400)
            sepetekle=self.imageAdd("sepeteekle")
            self.sepete_ekle.config(image=sepetekle,width="175", height="45",compound="right")


            #label=Label(canvas,text=self.kullaniciadi,width="50")
            #label.place(x=50,y=50)
            self.ürün_sorgula_classic()
            self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
            canvas.pack()
            anapencere.mainloop()

    pass


    def listele_sepet(self,ürünid=[],ürünad=[],ürünadet=[],ürünfiyat=[]):
        self.ürün_sorgula_classic()
        self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
        self.listbox_sepet.delete(0,END)
        self.boyut = len(self.sepet_urun_id)
        for i in range(0,self.boyut):
            cıktı="{:<10d}  {:<15s}  {:<16s}  {:<16s}   {:<13s}".format((i+1), ürünid[i],ürünad[i],ürünadet[i],ürünfiyat[i])
            self.listbox_sepet.insert(END,cıktı)
            #self.listbox_sepet.itemconfig(0,bg="red")
            if(i%2==1):
                self.listbox_sepet.itemconfig(i,bg="gray")

    def sepet_gui(self):
        if(self.toplam_urun !=0):
            self.lastselectionList2=[]
            del self.idler[:]
            self.lastselectionList = list(self.lastselectionList)
            del self.lastselectionList[:]
            self.lastselectionList = tuple(self.lastselectionList)
            sepetpencere = Toplevel()
            self.sepetpencere = sepetpencere;
            sepetpencere.title("Sepetim")
            sepetpencere.geometry("800x560+300+50")
            #sepetpencere.resizable(0,0)
            canvas3 = Canvas(sepetpencere,width=800,height=560)
            myimage = PhotoImage(file = "StokTakipSistemi\\images\\arkaplan2.png")
            canvas3.create_image(0,0,anchor=NW, image=myimage)
            self.buttons_add=[]
            self.buttons_delete=[]
            self.secilenler=[]   ### listboxda seçilen idleri tutar
            self.secilenler_adet=[]
            i=0
            a=35
            images_add=self.imageAdd("ekle")
            images_delete=self.imageAdd("image_delete")
            for i in range(0,len(self.sepet_urun_id)):

                self.buttons_add.append(Button(canvas3,text="%d" % i))
                self.buttons_add[i].place(x=580,y=a)
                self.buttons_add[i].bind('<Button-1>', partial(self.adet_artir,self.sepet_urun_id[i],i))
                self.buttons_add[i].bind("<B1-Motion>",partial(self.adet_artir,self.sepet_urun_id[i],i))
                self.buttons_add[i].config(image=images_add,width="11",height="7")

                self.buttons_delete.append(Button(canvas3,text="%d" % i))
                self.buttons_delete[i].place(x=610,y=a)
                self.buttons_delete[i].bind('<Button-1>', partial(self.adet_azalt,self.sepet_urun_id[i],i))
                self.buttons_delete[i].bind('<B1-Motion>', partial(self.adet_azalt,self.sepet_urun_id[i],i))
                self.buttons_delete[i].config(image=images_delete,width="11",height="7")
                a=a+16
            baslik="""           Ürün Kodu        Ürün Adı       Ürün Adet        Birim Fiyatı            Adet"""
            self.baslik2=Label(canvas3,text=baslik,fg="black",bg="gray",font=('Times,bold',14))
            self.baslik2.place(x=10,y=6)
            self.scrollbar2 = Scrollbar(self.sepetpencere)
            self.listbox_sepet = Listbox(canvas3,width="80",height="27",bg="white",selectbackground="red",fg="black",font=('consolas',"10"),yscrollcommand = self.scrollbar.set,selectmode="multiple")
            self.scrollbar2.pack(side=RIGHT, fill=Y)
            self.scrollbar2.config(command=self.listbox_sepet.yview)
            self.listbox_sepet.bind('<<ListboxSelect>>',self.listbox_sepet_select)
            self.listbox_sepet.place(x=10, y=33)

            self.sepetOnay =  Button(canvas3,text="Sepeti Onayla",width="24",height="4",bg="white",font=("Times,bold","7"),command=self.sepet_onayla)
            onay = self.imageAdd("onay")
            self.sepetOnay.config(image=onay,width="80",height="60",compound="top")
            self.sepetOnay.place(x=650,y=100)

            self.alldeleteButton= Button(canvas3,text="Tümünü İptal Et",width="24",height="4",bg="#fbf8f8",font=("Times,bold","7"),command=self.allDelete)
            kayıtsil=self.imageAdd("sil")
            self.alldeleteButton.config(image=kayıtsil,width="80", height="60",compound="top")
            self.alldeleteButton.place(x=650,y=300)


            self.selectdeleteButton= Button(canvas3,text="Seçili Ürünü İptal Et",width="24",height="4",bg="#fbf8f8",font=("Times,bold","7"),command=self.selectDelete)
            self.selectdeleteButton.config(image=kayıtsil,width="80", height="60",compound="top")
            self.selectdeleteButton.place(x=650,y=200)


            self.sepet_sorgula()
            self.listele_sepet(self.sepet_urun_id,self.sepet_urun_adi,self.sepet_urun_adet,self.sepet_urun_fiyat)
            self.listbox_sepet.selection_clear(0,END)
            canvas3.pack()
            self.sepetpencere.mainloop()
        else:
            return 0

    def allDelete(self):
        print(self.sepet_urun_id)
        if  (len(self.sepet_urun_id) != 0):
            cevap = messagebox.askquestion("Uyarı","Tüm ürünler sepetten çıkarılacaktır emin misiniz?")
            if(cevap=="yes"):
                with self.connection.cursor() as cursor:
                    for i in range(0,len(self.sepet_urun_id)):
                            adet=int(self.sepet_urun_adet[i])
                            urun_guncelle ="UPDATE `sts_urunler` SET `urun_adet`=CAST(`urun_adet` AS UNSIGNED INTEGER)+%d WHERE urun_id=%s"%(adet,self.sepet_urun_id[i])
                            cursor.execute(urun_guncelle)
                    allsil="DELETE FROM sts_alisveris WHERE sts_durum='0'"
                    cursor.execute(allsil)
                    self.listele_sepet(self.sepet_urun_id,self.sepet_urun_adi,self.sepet_urun_adet,self.sepet_urun_fiyat)
                    self.ürün_sorgula_classic()
                    self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
                    self.sepet_sorgula()
                    self.sepet['text']="{}".format(self.toplam_urun)
                    del self.secilenler[:]
                    self.sepetpencere.destroy()
            else:
                del self.secilenler[:]
                self.sepetpencere.destroy()
                self.sepet_gui()

        else:
            print("sepet bos")
    def sepet_onayla(self):
        print(self.kullaniciadi)
        print(type(self.kullaniciadi))
        with self.connection.cursor() as cursor:
            i=0
            for i in range(0,len(self.sepet_urun_id)):
                guncelle="UPDATE `sts_alisveris` SET `sts_durum`='1' WHERE `sts_müsteri_id`=%s"%self.kullaniciadi
                cursor.execute(guncelle)
            messagebox.showinfo("Başarı","Sepetiniz Onaylandı.")
            self.sepet_sorgula()
            self.listele_sepet(self.sepet_urun_id,self.sepet_urun_adi,self.sepet_urun_adet,self.sepet_urun_fiyat)
            self.sepet['text']="{}".format(self.toplam_urun)
            self.sepetpencere.destroy()
            self.sepet_gui()

    def selectDelete(self):
        if not self.secilenler:
            return 0
        else:
            cevap = messagebox.askquestion("Uyarı","Seçili ürünler sepetten çıkarılacaktır emin misiniz?")
            if(cevap=="yes"):
                with self.connection.cursor() as cursor:
                    for i in range(0,len(self.secilenler)):
                        sil="DELETE FROM sts_alisveris WHERE sts_urun_id=%s and sts_durum='0' "%self.secilenler[i]
                        cursor.execute(sil)
                        adet=int(self.secilenler_adet[i])
                        urun_guncelle ="UPDATE `sts_urunler` SET `urun_adet`=CAST(`urun_adet` AS UNSIGNED INTEGER)+%d WHERE urun_id=%s"%(adet,self.secilenler[i])
                        cursor.execute(urun_guncelle)
                    self.sepet_sorgula()
                    self.listele_sepet(self.sepet_urun_id,self.sepet_urun_adi,self.sepet_urun_adet,self.sepet_urun_fiyat)
                    self.ürün_sorgula_classic()
                    self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
                    self.sepet['text']="{}".format(self.toplam_urun)
                    self.listbox_sepet.selection_clear(0,"end")
                    del self.secilenler[:]
                    self.sepetpencere.destroy()
                    self.sepet_gui()
            else:
                self.sepetpencere.destroy()
                self.sepet_gui()
                del self.secilenler[:]

    def listbox_sepet_select(self,event=None):
     try:

        w = event.widget
        if self.lastselectionList2: #if not empty
        #compare last selectionlist with new list and extract the difference
            changedSelection2 = set(self.lastselectionList2).symmetric_difference(set(w.curselection()))
            self.lastselectionList2 = w.curselection()
        else:
        #if empty, assign current selection
            self.lastselectionList2 = w.curselection()
            changedSelection2 = w.curselection()
        #changedSelection2 should always be a set with only one entry, therefore we can convert it to a lst and extract first entry
        index = 0
        index = int(list(changedSelection2)[0])
        value = w.get(index)
        value = value.split()
        values = value[1]

        durum=False
        for i in self.secilenler:
            if(values==i):
                durum=True
                self.secilenler.remove(values)
                self.secilenler_adet.remove(value[3])
        if(durum==False):
            self.secilenler.append(values)
            self.secilenler_adet.append(value[3])
        print(self.secilenler)
        print(self.secilenler_adet)

     except :
            a=5


    def adet_artir(self,urunid,i,event=None):
        self.sepet_sorgula()
        with self.connection.cursor() as cursor:
            if(self.urunAdet[i]!="0"):

                alisveris_guncelle ="UPDATE `sts_alisveris` SET `sts_urun_adet`=CAST(`sts_urun_adet` AS UNSIGNED INTEGER)+1 WHERE sts_urun_id=%s and sts_durum='0'"%(urunid)
                cursor.execute(alisveris_guncelle)
                urun_guncelle ="UPDATE `sts_urunler` SET `urun_adet`=CAST(`urun_adet` AS UNSIGNED INTEGER)-1 WHERE urun_id=%s"%(urunid)
                cursor.execute(urun_guncelle)
                self.sepet_sorgula()
                self.listele_sepet(self.sepet_urun_id,self.sepet_urun_adi,self.sepet_urun_adet,self.sepet_urun_fiyat)
                self.sepet['text']="{}".format(self.toplam_urun)
            else:
                messagebox.showwarning("Stok Hatası","Stokta yeterli sayıda ürün bulunmamaktadır.")


    def adet_azalt(self,urunid,i,event=None):
        self.sepet_sorgula()
        print("kalan ürün: {}".format(self.sepet_urun_adet[i]))
        with self.connection.cursor() as cursor:
            if(self.sepet_urun_adet[i]=='1'):
                sil = "DELETE FROM sts_alisveris WHERE sts_durum = '0' and sts_urun_id= %s "%urunid
                cursor.execute(sil)
                self.sepet_sorgula()
                self.listele_sepet(self.sepet_urun_id,self.sepet_urun_adi,self.sepet_urun_adet,self.sepet_urun_fiyat)
                self.sepet['text']="{}".format(self.toplam_urun)
                #self.buttons_add[i].destroy()   ## Aşağıdaki iki buton yerine bunlarda kullanılabilir
                #self.buttons_delete[i].destroy()
                self.sepetpencere.destroy()
                self.sepet_gui()
            else:
                alisveris_guncelle ="UPDATE `sts_alisveris` SET `sts_urun_adet`=CAST(`sts_urun_adet` AS UNSIGNED INTEGER)-1 WHERE sts_urun_id=%s and sts_durum='0'"%(urunid)
                cursor.execute(alisveris_guncelle)
                urun_guncelle ="UPDATE `sts_urunler` SET `urun_adet`=CAST(`urun_adet` AS UNSIGNED INTEGER)+1 WHERE urun_id=%s"%(urunid)
                cursor.execute(urun_guncelle)
                self.sepet_sorgula()
                self.listele_sepet(self.sepet_urun_id,self.sepet_urun_adi,self.sepet_urun_adet,self.sepet_urun_fiyat)
                self.sepet['text']="{}".format(self.toplam_urun)




    def müsteri_islemleri(self,event=None):
        self.connection = pymysql.connect(host='localhost',
                                                 user='root',
                                                 password='',
                                                 db='stoktakipsistemi',
                                                 charset='utf8mb4',
                                                 cursorclass=pymysql.cursors.DictCursor)
        müsteriislemleri = Toplevel()
        self.müsteriislemleri = müsteriislemleri;
        müsteriislemleri.title("Müşteri İslemleri")
        müsteriislemleri.geometry("330x480+500+100")
        müsteriislemleri.resizable(0,0)
        canvaskullanıcı = Canvas(müsteriislemleri,width=350,height=480)
        myimage = PhotoImage(file = "C:\\Users\\Kürşad\\Desktop\\StokTakipSistemi\\images\\anasayfa.png")
        canvaskullanıcı.create_image(0,0,anchor=NW, image=myimage)

        kapatButton = Button(canvaskullanıcı,text="Kapat")
        kapatButton.place(x=145,y=20)
        resim2=self.imageAdd("kapat")
        kapatButton.config(image=resim2,width="45", height="35",command=self.müsteriislemleri.destroy)


        kimliklb = Label(canvaskullanıcı,text="Kimlik No ",width=10)
        kimliklb.place(x=50,y=80)
        self.kimlik_müsteri = Entry(canvaskullanıcı)
        self.kimlik_müsteri.place(x=140,y=80)


        adlb = Label(canvaskullanıcı, text="Ad  ",width=10)
        adlb.place(x=50, y=120)
        self.ad_müsteri = Entry(canvaskullanıcı)
        self.ad_müsteri.place(x=140, y=120)

        soyadlb = Label(canvaskullanıcı, text="Soyad:   ",width=10)
        soyadlb.place(x=50, y=160)
        self.soyad_müsteri = Entry(canvaskullanıcı)
        self.soyad_müsteri.place(x=140, y=160)

        sifrelb = Label(canvaskullanıcı, text="Sifre  ",width=10)
        sifrelb.place(x=50, y=200)
        self.sifre_müsteri = Entry(canvaskullanıcı,show="*")
        self.sifre_müsteri.place(x=140, y=200)


        telefonlb = Label(canvaskullanıcı, text="Telefon   ",width=10)
        telefonlb.place(x=50, y=240)
        self.telefon_müsteri = Entry(canvaskullanıcı)
        self.telefon_müsteri.place(x=140, y=240)

        postalb = Label(canvaskullanıcı, text="E-Posta   ",width=10)
        postalb.place(x=50, y=280)
        self.posta_müsteri = Entry(canvaskullanıcı)
        self.posta_müsteri.place(x=140, y=280)

        adreslb = Label(canvaskullanıcı, text="Adres   ",width=10)
        adreslb.place(x=50, y=320)
        self.adres_müsteri = Text(canvaskullanıcı,width=15,height=3)
        self.adres_müsteri.place(x=140, y=320)

        self.kaydet_müsteri = Button(canvaskullanıcı,text="Kaydet",command=self.kaydet_guncel_müsteri)
        self.kaydet_müsteri.place(x=115,y=390)
        resim=self.imageAdd("giris")
        self.kaydet_müsteri.config(image =resim, width = 85 , height = 30)
        müsteriislemleri.bind('<Return>', self.kaydet_guncel_müsteri)


        with self.connection.cursor() as cursor:
            bilgilerin="SELECT * FROM  `sts_müsteri` WHERE müsteri_posta= '%s'"% (self.kullaniciadi)
            sonuc=cursor.execute(bilgilerin)
            print(bilgilerin)
            if (sonuc==1):  ##sonuc 1 ise posta ile giriş yapılmıştır postaya göre bilgilere ulaşılır
                for i in cursor.fetchall():
                    self.kimlikno = i["müsteri_id"]
                    self.isim = i["müsteri_adi"]
                    self.soyisim = i["müsteri_soyadi"]
                    self.password = i["müsteri_sifre"]
                    self.eposta = i["müsteri_posta"]
                    self.cepnumara = i["müsteri_cepno"]
                    self.adres=i["müsteri_adres"]
            if(sonuc==0):   ###sonuc 0 ise id ile giriş yapılmıştır
                bilgilerin="SELECT * FROM  `sts_müsteri` WHERE müsteri_id= '%s'"%self.kullaniciadi
                cursor.execute(bilgilerin)
                for i in cursor.fetchall():
                    self.kimlikno = i["müsteri_id"]
                    self.isim = i["müsteri_adi"]
                    self.soyisim = i["müsteri_soyadi"]
                    self.password = i["müsteri_sifre"]
                    self.eposta = i["müsteri_posta"]
                    self.cepnumara = i["müsteri_cepno"]
                    self.adres=i["müsteri_adres"]

        self.kimlik_müsteri.insert(END,self.kimlikno)
        self.kimlik_müsteri.configure(state="readonly")
        self.ad_müsteri.insert(END,self.isim)
        self.soyad_müsteri.insert(END,self.soyisim)
        self.sifre_müsteri.insert(END,self.password)
        self.telefon_müsteri.insert(END,self.cepnumara)
        self.posta_müsteri.insert(END,self.eposta)
        self.adres_müsteri.insert("end",self.adres)

        canvaskullanıcı.pack()
        müsteriislemleri.mainloop()

    def kaydet_guncel_müsteri(self,event=None):
        if(self.ad_müsteri.get()=="" or self.soyad_müsteri.get()=="" or self.sifre_müsteri.get()==""\
         or self.posta_müsteri.get()=="" or self.telefon_müsteri.get()=="" or self.adres_müsteri.get("1.0",'end-1c')==""):
             messagebox.showinfo("Bos Alan","Bos Alanlari Doldurunuz")
        else:
            self.kn = self.kimlik_müsteri.get()
            self.name = self.ad_müsteri.get()
            self.surname = self.soyad_müsteri.get()
            self.pas = self.sifre_müsteri.get()
            self.tel = self.telefon_müsteri.get()
            self.mail = self.posta_müsteri.get()
            self.adres=self.adres_müsteri.get("1.0","end-1c")

            with self.connection.cursor() as cursor:
                basarı=cursor.execute ("UPDATE sts_müsteri SET müsteri_adi = '%s' , müsteri_soyadi = '%s' , müsteri_sifre = '%s' , müsteri_posta = '%s' , müsteri_cepno = '%s', müsteri_adres = '%s' WHERE müsteri_id = '%s'"\
                % (self.name , self.surname , self.pas , self.mail , self.tel, self.adres, self.kn) )

            if(basarı >0):
                messagebox.showinfo("BAŞARI","Bilgileriniz Kaydedildi.")



    def listbox_select(self,event=None):
     try:
        w2 = event.widget
        if self.lastselectionList: #if not empty
            print(type(self.lastselectionList))
        #compare last selectionlist with new list and extract the difference
            changedSelection = set(self.lastselectionList).symmetric_difference(set(w2.curselection()))
            self.lastselectionList = w2.curselection()
        else:
        #if empty, assign current selection
            self.lastselectionList = w2.curselection()
            changedSelection = w2.curselection()
        #changedSelection should always be a set with only one entry, therefore we can convert it to a lst and extract first entry

        index = int(list(changedSelection)[0])
        value = w2.get(index)
        value = value.split()
        value = value[1]
        durum=False
        for i in self.idler:
            if(value==i):
                durum=True
                self.idler.remove(value)
        if(durum==False):
            self.idler.append(value)
        print(self.idler)
        id_end = self.idler[len(self.idler)-1]
        with self.connection.cursor() as cursor:
            sql1="SELECT urun_goruntu FROM sts_urunler WHERE urun_id = %s"%id_end
            sorgu1 = cursor.execute(sql1)
            for i in cursor.fetchall():
                imj = i["urun_goruntu"]
        try:
            img=ImageTk.PhotoImage(Image.open("StokTakipSistemi\\images\\KameraKayit\\"+id_end+".png"))
            self.resimlerMüsteri.config(image=img,width="180",height="180")
            self.anapencere.mainloop()
        except:
            yol="StokTakipSistemi\\images\\KameraKayit\\"+id_end+".png"
            imj = base64.b64decode(imj)
            with open(yol,'wb') as file:
                file.write(imj)
                img = ImageTk.PhotoImage(Image.open(yol))
                self.resimlerMüsteri.config(image=img,width="180",height="180")
                self.anapencere.mainloop()
     except :
            a=5

    def sepet_sorgula(self):

        self.sepet_urun_id=[]
        self.sepet_urun_adi=[]
        self.sepet_urun_adet=[]
        self.sepet_urun_fiyat=[]
        self.urunAdet=[]
        self.toplam_urun=0

        with self.connection.cursor() as cursor:
            sepetSorgu="select * from sts_alisveris AS alisveris, sts_urunler AS urunler WHERE \
             alisveris.sts_durum='0' and alisveris.sts_urun_id = urunler.urun_id and sts_müsteri_id=%s" %self.kullaniciadi
            cursor.execute(sepetSorgu)
            for kolon in cursor.fetchall():
                self.sepet_urun_id.append(kolon["sts_urun_id"])
                self.sepet_urun_adi.append(kolon["urun_ad"])
                self.sepet_urun_adet.append(kolon["sts_urun_adet"])
                self.sepet_urun_fiyat.append(kolon["urun_fiyat"])
                self.urunAdet.append(kolon["urun_adet"])
        for i in range(0,len(self.sepet_urun_adet)):
            self.toplam_urun = self.toplam_urun + int(self.sepet_urun_adet[i])
        print(self.toplam_urun)


    def sepet_add(self):
        self.sepet_sorgula()   ######## ürünün toplam adeti bulundu
        trh = datetime.datetime.now()
        self.trh = "{}-{}-{}".format(trh.year,trh.month,trh.day)


        with self.connection.cursor() as cursor:
            for y in range (0,len(self.idler)):
                if(self.idler[y] in self.sepet_urun_id):
                    alisveris_guncelle ="UPDATE `sts_alisveris` SET `sts_urun_adet`=CAST(`sts_urun_adet` AS UNSIGNED INTEGER)+1 WHERE sts_urun_id=%s"%(self.idler[y])
                    cursor.execute(alisveris_guncelle)
                    urun_guncelle ="UPDATE `sts_urunler` SET `urun_adet`=CAST(`urun_adet` AS UNSIGNED INTEGER)-1 WHERE urun_id=%s"%(self.idler[y])
                    cursor.execute(urun_guncelle)
                    self.sepet_sorgula()
                    self.sepet['text']="{}".format(self.toplam_urun)
                    self.ürün_sorgula_classic()
                    self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
                    self.lastselectionList = list(self.lastselectionList)
                    del self.lastselectionList[:]
                    self.lastselectionList = tuple(self.lastselectionList)



                else:
                    durum="0"  ## durumun 0 olması alisverisin tamamlanmamış yani haala sepette olduğunu gösterir.Burada durum 1
                    adet=1
                    satıs_query = "INSERT INTO sts_alisveris(sts_urun_id,sts_müsteri_id,sts_urun_adet,sts_islem_tarih,sts_durum)\
                VALUES('%s','%s','%s','%s','%s')" % (self.idler[y],self.kullaniciadi,adet,self.trh,durum)
                    cursor.execute(satıs_query)
                    urun_guncelle ="UPDATE `sts_urunler` SET `urun_adet`=CAST(`urun_adet` AS UNSIGNED INTEGER)-1 WHERE urun_id=%s"%(self.idler[y])
                    cursor.execute(urun_guncelle)
                    self.listbox.update()
                    self.sepet_sorgula()
                    self.sepet['text']="{}".format(self.toplam_urun)
                    self.ürün_sorgula_classic()
                    self.listele(self.urun_id,self.urun_ad,self.urun_adet,self.urun_tarih,self.urun_fiyat)
                    self.lastselectionList = list(self.lastselectionList)   ## tuple önce listboxa dönüşür sonra temizlenir sonra tekrar tuple olur
                    del self.lastselectionList[:]    # bunu yapmamızın sebebi listboxda seçilen öğelere sepete girdiğimizde sabit kalıyor.
                    self.lastselectionList = tuple(self.lastselectionList) # tekrar ürünlere döndüğümüzde seçim işleminde hata oluşmuyor

        del self.idler[:]



    def ürün_sorgula_classic(self):
        self.urun_id=[]
        self.urun_ad=[]
        self.urun_adet=[]
        self.urun_tarih=[]
        self.urun_fiyat=[]
        self.urun_resim=[]
        with self.connection.cursor() as cursor:
            sorguClassic = "SELECT * FROM `sts_urunler` WHERE CAST(`urun_adet` AS UNSIGNED INTEGER)>0"
            cursor.execute(sorguClassic)
            for kolon in cursor.fetchall():
                self.urun_id.append(kolon["urun_id"])
                self.urun_ad.append(kolon["urun_ad"])
                self.urun_adet.append(kolon["urun_adet"])
                self.urun_tarih.append(kolon["urun_tarih"])
                self.urun_fiyat.append(kolon["urun_fiyat"])

    def listele(self,ürünid=[],ürünad=[],ürünadet=[],ürüntarih=[],ürünfiyat=[]):
        self.listbox.delete(0,END)
        self.boyut = len(ürünid)
        for i in range(0,self.boyut):
            cıktı="{:<10d}  {:<15s}  {:<16s}  {:<16s}   {:<13s}".format((i+1), ürünid[i],ürünad[i],ürünadet[i],ürünfiyat[i])
            self.listbox.insert(END,cıktı)
            #self.listbox.itemconfig(0,bg="red")
            if(i%2==1):
                self.listbox.itemconfig(i,bg="gray")

anasayfa=AnaSayfa()
