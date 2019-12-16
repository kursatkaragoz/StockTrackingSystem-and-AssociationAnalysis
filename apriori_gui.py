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
import time
import csv
from optparse import OptionParser    # parse command-line parameters
from apriori import Apriori
from termcolor import colored
import fpdf
import unicodedata


class Birliktelik():

    def imageAdd(self,uzantı):
        img = PhotoImage(file = "StokTakipSistemi\\images\\"+uzantı+".png")
        return img
    def gerigel(self):
        sys.exit
        self.alisveris_pencere.destroy()


    def alisveris_sorgulaca_classic(self):
        self.sts_urun_id=[]
        self.sts_urun_adi=[]
        self.sts_müsteri_id=[]
        self.sts_müsteri_adi=[]
        self.sts_müsteri_soyadi=[]
        self.sts_urun_adet=[]
        self.sts_islem_tarihi=[]
        with self.connection.cursor() as cursor:
            sorguKarisik ="SELECT * FROM sts_urunler AS urunler,sts_alisveris AS alisveris, sts_müsteri AS müsteri WHERE\
             urunler.urun_id = alisveris.sts_urun_id and müsteri.müsteri_id = alisveris.sts_müsteri_id"
            cursor.execute(sorguKarisik)
            for kolon in cursor.fetchall():
                self.sts_urun_id.append(kolon["urun_id"])
                self.sts_urun_adi.append(kolon["urun_ad"])
                self.sts_müsteri_id.append(kolon["müsteri_id"])
                self.sts_müsteri_adi.append(kolon["müsteri_adi"])
                self.sts_müsteri_soyadi.append(kolon["müsteri_soyadi"])
                self.sts_urun_adet.append(kolon["sts_urun_adet"])
                self.sts_islem_tarihi.append(kolon["sts_islem_tarih"])

    def alisveris_filtrele(self):

        self.listbox2.delete(0,END)
        del self.sts_urun_id[:]
        del self.sts_urun_adi[:]
        del self.sts_müsteri_id[:]
        del self.sts_müsteri_adi[:]
        del self.sts_müsteri_soyadi[:]
        del self.sts_urun_adet[:]
        del self.sts_islem_tarihi[:]
        #self.trhbaslangic =datetime.date(self.tarih1.get())
        #self.trhson=datetime.date(self.tarih2.get())
        self.trhbaslangic = self.tarih1.get()
        self.trhson = self.tarih2.get()
        print(self.trhbaslangic)
        print(self.trhson)
        with self.connection.cursor() as cursor:
            sorguKarisik ="SELECT * FROM sts_urunler AS urunler,sts_alisveris AS alisveris, sts_müsteri AS müsteri WHERE\
             urunler.urun_id = alisveris.sts_urun_id and müsteri.müsteri_id = alisveris.sts_müsteri_id and \
             alisveris.sts_islem_tarih >= '%s' and alisveris.sts_islem_tarih <= '%s'"%\
             (self.trhbaslangic,self.trhson)
            print(sorguKarisik)
            cursor.execute(sorguKarisik)
            for kolon in cursor.fetchall():
                self.sts_urun_id.append(kolon["urun_id"])
                self.sts_urun_adi.append(kolon["urun_ad"])
                self.sts_müsteri_id.append(kolon["müsteri_id"])
                self.sts_müsteri_adi.append(kolon["müsteri_adi"])
                self.sts_müsteri_soyadi.append(kolon["müsteri_soyadi"])
                self.sts_urun_adet.append(kolon["sts_urun_adet"])
                self.sts_islem_tarihi.append(kolon["sts_islem_tarih"])

        self.listele_alisveris(self.sts_urun_id,self.sts_urun_adi,self.sts_müsteri_id,self.sts_müsteri_adi,self.sts_müsteri_soyadi,self.sts_urun_adet,self.sts_islem_tarihi)

    def dataset_changed(self):
        self.satis_urun_ad=[]
        self.sonuc=[]
        urunler=""
        self.sts_müsteri_id = sorted(set(self.sts_müsteri_id), key=self.sts_müsteri_id.index)
        with self.connection.cursor() as cursor:
            for i in range(0,len(self.sts_müsteri_id)):
                sorgu="SELECT * FROM sts_alisveris AS alisveris, sts_urunler AS urunler WHERE alisveris.sts_müsteri_id = %s and alisveris.sts_urun_id = urunler.urun_id "%self.sts_müsteri_id[i]
                cursor.execute(sorgu)

                for kolon2 in cursor.fetchall():
                    urunler ="{},{}".format(str(urunler),kolon2["urun_ad"])

                urunler = urunler[1:len(urunler)]
                print(urunler)
                self.sonuc.append(str(urunler))
                urunler=""
        with open('dataset.csv', 'w',newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            for j in range(0,len(self.sonuc)):
                spamwriter.writerow([self.sonuc[j]])
        pass

        self.listbox2.insert(END," ")
        self.listbox2.insert(END,"Dönüştürülmüş Veri Seti")
        self.listbox2.insert(END," ")
        for k in range(0,len(self.sonuc)):
            self.listbox2.insert(END,"{} {}".format(k+1,self.sonuc[k]))

        selected_indices = self.listbox2.curselection()


    def listele_alisveris(self,urun_id=[],urun_adi=[],müsteri_id=[],müsteri_adi=[],müsteri_soyadi=[],urun_adet=[],islem_tarihi=[]):
        self.listbox2.delete(0,END)
        boyut = len(urun_id)
        for i in range(0,boyut):
            cıktı="{:<3d}  {:<13s}  {:<7s}  {:<12s}  {:<8s}  {:<8s}  {:<6s}  {:<10s}".format((i+1), müsteri_id[i],müsteri_adi[i],müsteri_soyadi[i],urun_id[i],urun_adi[i],urun_adet[i],str(islem_tarihi[i]))
            self.listbox2.insert(END,cıktı)
            if(i%2==1):
                self.listbox2.itemconfig(i,bg="green")
    def sifirla(self):
        self.listbox2.delete(0,END)
        del self.sts_urun_id[:]
        del self.sts_urun_adi[:]
        del self.sts_müsteri_id[:]
        del self.sts_müsteri_adi[:]
        del self.sts_müsteri_soyadi[:]
        del self.sts_urun_adet[:]
        del self.sts_islem_tarihi[:]
        self.tarih1.delete(0,END)
        self.tarih2.delete(0,END)
        self.tarih1.insert("end",self.trh)
        self.tarih2.insert("end",self.trh)
        self.alisveris_sorgulaca_classic()
        self.listele_alisveris(self.sts_urun_id,self.sts_urun_adi,self.sts_müsteri_id,self.sts_müsteri_adi,self.sts_müsteri_soyadi,self.sts_urun_adet,self.sts_islem_tarihi)

    def start_apriori(self):

        if(self.destek.get()=="" or self.guven.get()==""):
            messagebox.showwarning("Eksik Bilgi","Birliktelik Analizinin Yapılabilmesi için \nDestek ve Güven Ölçütleri Girilmelidir")
        else:
            self.dstk = float(self.destek.get())
            self.gvn = float(self.guven.get())

            self.Degerler =[]
            with open('dataset.csv', 'r') as csvFile:
                reader = csv.reader(csvFile)
                for row in reader:
                    for i in range (0,len(row)):
                        if (row[i] in self.Degerler) == False:
                            self.Degerler.append(row[i])
                    #print(row)

            csvFile.close()
            self.sonuclar=[]
            self.itemtutucu=[]
            a=0
            for sayac in range(0,len(self.Degerler)):
                # Get two important parameters
                self.filePath = "dataset.csv"
                self.minSupp  = self.dstk
                self.minConf  = self.gvn
                deger = self.Degerler[sayac]
                self.rhs      = frozenset([deger])
                print("""Minimum Destek: {} \n Minimum Güven: {} \n İncelenen Ürün: {}\n""".\
                      format(self.minSupp,self.minConf, self.rhs))
                incelenen = """Minimum Destek: {} \n Minimum Güven: {} \n İncelenen Ürün: {}\n""".\
                      format(self.minSupp,self.minConf, self.rhs)
                self.listbox2.insert(END,incelenen)

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
                self.listbox2.insert(END,self.itemtutucu[row])

            print("SONUCLAR\n")
            self.listbox2.insert(END,"---------SONUCLAR----------")
            for i in range(0,len(self.sonuclar)):
                self.listbox2.insert(END,"{} {}".format(i+1,self.sonuclar[i]))
                print(self.sonuclar[i])

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
        alisveris_pencere.title("Birliktelik Analizi")
        alisveris_pencere.geometry("900x360+250+50")
        #alisveris_pencere.config(bg="black")
        #alisveris_pencere.resizable(0,0)
        canvas = Canvas(alisveris_pencere,width=900,height=360)
        myimage = PhotoImage(file = "StokTakipSistemi\\images\\arkaplan2.png")
        canvas.create_image(0,0,anchor=NW, image=myimage)

        geriButton = Button(canvas,text="Geri Gel",bg="white")
        geriButton.place(x=20,y=0)
        resimg=self.imageAdd("geri")
        geriButton.config(image=resimg,width="45", height="35",command=self.gerigel)



        baslık2="""   Müşteri İD                 Müşteri Adi               Ürün İD    Ürün Adi   Adet   İşlem Tarihi """
        baslik2 = Label(canvas,text=baslık2,fg="black",bg="gray",font=('Times,bold',12))
        baslik2.place(x=20,y=75)

        self.scrollbar2 = Scrollbar(self.alisveris_pencere)
        self.listbox2 = Listbox(canvas,width="80",height="13",bg="black",fg="white",font=('consolas',10),yscrollcommand = self.scrollbar2.set)
        self.scrollbar2.pack(side=LEFT, fill=Y)
        self.scrollbar2.config(command=self.listbox2.yview)
        self.listbox2.place(x=20, y=100)



        trh = datetime.datetime.now()
        self.trh = "{}-{}-{}".format(trh.year,trh.month,trh.day)

        self.tarih1 = Entry(canvas,width="15")
        self.tarih1.place(x=630, y=75)
        self.tarih1.insert("end",self.trh)

        self.tarih2 = Entry(canvas,width="15")
        self.tarih2.place(x=730, y=75)
        self.tarih2.insert("end",self.trh)

        self.filtrele = Button(canvas,text="Filtrele",width="12",command=self.alisveris_filtrele)
        self.filtrele.place(x=630,y=105)

        self.sifirla = Button(canvas,text="Sıfırla",width="12",command=self.sifirla)
        self.sifirla.place(x=730,y=105)

        self.dataset = Button(canvas,text="Veri Setine Dönüştür",width="26",command=self.dataset_changed)
        self.dataset.place(x=630,y=135)

        self.desteklabel = Label(canvas,text="Destek Eşik:",width="12")
        self.desteklabel.place(x=630,y=185)
        self.destek = Entry(canvas,width="12")
        self.destek.place(x=730,y=185)

        self.guvenlabel = Label(canvas,text="Güven Eşik:",width="12")
        self.guvenlabel.place(x=630,y=215)
        self.guven = Entry(canvas,width="12")
        self.guven.place(x=730,y=215)

        self.analiz = Button(canvas,text="Analize Başla    ", width="196", height="24",bg="#fbf8f8",command=self.start_apriori)
        self.analiz.place(x=630,y=245)
        resimanaliz=self.imageAdd("analiz")
        self.analiz.config(image=resimanaliz,width="196", height="24",compound="right")

        self.pdfsave = Button(canvas,text="Sonuçları Kaydet        ",width="196",height="24",bg="#fbf8f8",command=self.topdf)
        self.pdfsave.place(x=630,y=280)
        resimpdf=self.imageAdd("pdf")
        self.pdfsave.config(image=resimpdf,width="196", height="24",compound="right")




        self.alisveris_sorgulaca_classic()
        self.listele_alisveris(self.sts_urun_id,self.sts_urun_adi,self.sts_müsteri_id,self.sts_müsteri_adi,self.sts_müsteri_soyadi,self.sts_urun_adet,self.sts_islem_tarihi)



        canvas.pack()
        alisveris_pencere.mainloop()