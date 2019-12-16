from tkinter import *
import pymysql.cursors
from tkinter import ttk
from tkinter import messagebox
import sys
from PIL import Image, ImageTk
from tkinter import filedialog
import smtplib


class Müsteriİslemleri():


    def imageAdd(self,uzantı):
        img = PhotoImage(file = "StokTakipSistemi\\images\\"+uzantı+".png")
        return img


    global firstclick
    firstclick=True
    def arama_olacaklar(self,event=None):
        self.firstclick=True
        self.event = event
        if self.firstclick: # if this is the first time they clicked it
            self.firstclick = False
            self.müsteriArama.delete(0, "end")

    def aramas_olacaklar(self,sv,event=None):
        if(self.sv.get()!=None and self.sv.get()!="Müsteri, id veya ad..."):
            self.id_ad = self.sv.get()
            with self.connection.cursor() as cursor:
                try:
                    sql = "SELECT * FROM sts_müsteri WHERE müsteri_adi like %s"
                    sorgu1 = cursor.execute(sql,"%"+self.id_ad+"%")
                    if(sorgu1 >0 ):
                        print("ad bulundu")
                        self.dizileribosalt()
                        for i in cursor.fetchall():
                            self.müsteri_id.append(i["müsteri_id"])
                            self.müsteri_ad.append(i["müsteri_adi"])
                            self.müsteri_soyad.append(i["müsteri_soyadi"])
                            self.müsteri_tel.append(i["müsteri_cepno"])
                            self.müsteri_posta.append(i["müsteri_posta"])
                            self.müsteri_adres.append(i["müsteri_adres"])
                        self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)
                    else:
                        self.dizileribosalt()
                        self.müsteri_sorgula_classic()
                        self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)


                    if(sorgu1==0):
                        sql="SELECT  * FROM sts_müsteri WHERE müsteri_id like %s"
                        sorgu1 = cursor.execute(sql,"%"+self.id_ad+"%")
                        if(sorgu1>0):
                            print("id bulundu")
                            self.dizileribosalt()
                            for i in cursor.fetchall():
                                self.müsteri_id.append(i["müsteri_id"])
                                self.müsteri_ad.append(i["müsteri_adi"])
                                self.müsteri_soyad.append(i["müsteri_soyadi"])
                                self.müsteri_tel.append(i["müsteri_cepno"])
                                self.müsteri_posta.append(i["müsteri_posta"])
                                self.müsteri_adres.append(i["müsteri_adres"])
                            self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)
                        else:
                            self.dizileribosalt()
                            self.müsteri_sorgula_classic()
                            self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)

                except:
                    print("beklenmeyen hata")


    def müsteriEkle(self):

        if(self.müsteriNo.get() != "" and self.müsteriAd.get() !="" and self.müsteriSoyad.get()!= "" and self.müsteriTelefon.get()!="" and self.müsteriPosta.get()!="" and self.müsteriAdres.get("1.0",'end-1c')!=""):
            try:
                with self.connection.cursor() as cursor:
                    müsteri_varmi= "SELECT * FROM sts_müsteri WHERE müsteri_id = %s"%self.müsteriNo.get()
                    var = cursor.execute(müsteri_varmi)
                    print(var)
                    if(var==1):
                        messagebox.showinfo("Müsteri Ekleme Hatası","Eklenmek istenen müsteri sisteme zaten kayıtlıdır.")
                        for i in cursor.fetchall():
                                no=i["müsteri_id"]
                                ad=i["müsteri_adi"]
                                soyad = i["müsteri_soyadi"]
                                tel = i["müsteri_cepno"]
                                posta = i["müsteri_posta"]
                                adres = i["müsteri_adres"]
                        self.clear_widget()
                        self.müsteriNo.insert(END,no)
                        self.müsteriNo.config(state="readonly")
                        self.müsteriAdres.insert("1.0",adres)
                        self.müsteriAd.insert(END,ad)
                        self.müsteriSoyad.insert(END,soyad)
                        self.müsteriTelefon.insert(END,tel)
                        self.müsteriPosta.insert(END,posta)
                    else:
                        self.mail_gonder(self.müsteriPosta.get())
                        yazdir="INSERT INTO sts_müsteri(müsteri_id, \
                   müsteri_adi, müsteri_soyadi, müsteri_sifre , müsteri_posta,müsteri_cepno,müsteri_adres) \
                   VALUES ('%s', '%s', '%s', '%s' , '%s','%s' ,'%s'  )" % \
                   (self.müsteriNo.get(),self.müsteriAd.get(),self.müsteriSoyad.get(),self.gecicisifre,self.müsteriPosta.get(),self.müsteriTelefon.get(),self.müsteriAdres.get("1.0",'end-1c'))
                        cursor.execute(yazdir)
                        messagebox.showinfo("BAŞARI","Kayıt İşlemi Gerçekleştirildi")
                        self.müsteri_sorgula_classic()
                        self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)
                        self.clear_widget()
            except:
               messagebox.showwarning("Posta Hatası","Geçerli Bir Posta Adresini Giriniz \n Şifreniz posta üzerinden oluşturulacaktır")
        else:
            messagebox.showwarning("Eksik Bilgi","Eksik Bilgileri Doldurunuz")
    def müsteriSil(self):
        if(self.müsteriNo.get() != ""):
            self.silinecek_id = self.müsteriNo.get()
            with self.connection.cursor() as cursor:
                müsteri_varmi= "select * from sts_müsteri where müsteri_id = %s"%self.silinecek_id
                var = cursor.execute(müsteri_varmi)
                for i in cursor.fetchall():
                        isim=i["müsteri_adi"]
                if(var==1):
                    cevap = messagebox.askquestion("Uyarı","{} numaralı {} isimli müşteri silinecek emin misiniz?".format(self.silinecek_id,isim))
                    if(cevap=="yes"):
                        silme = "DELETE FROM sts_müsteri WHERE müsteri_id= %s"
                        cursor.execute(silme,self.silinecek_id)
                        self.müsteri_sorgula_classic()
                        self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)
                        self.clear_widget()
                    else:
                        return 0
                else:
                    messagebox.showerror("Tanımsız Ürün İD","{} numaralı ürün kayıtlarda tanımlı değildir !!!".format(self.müsteriNo.get()))
        else:
            messagebox.showwarning("Tanımsız Ürün İd","""  Ürün silmek için İD giriniz
             veya
   Silmek istediğiniz ürünü seçiniz""")
    def müsteriGuncelle(self):
        if(self.müsteriNo.get() != "" and self.müsteriAd.get() !="" and self.müsteriSoyad.get()!= "" and self.müsteriTelefon.get()!="" and self.müsteriPosta.get()!="" and self.müsteriAdres.get("1.0",'end-1c')!=""):
            self.güncellenecekid = self.müsteriNo.get()
            with self.connection.cursor() as cursor:
                müsteri_varmi= "select * from sts_müsteri where müsteri_id = %s"%self.güncellenecekid
                var = cursor.execute(müsteri_varmi)
                for i in cursor.fetchall():
                        isim=i["müsteri_adi"]
                if(var==1):
                    guncelle="UPDATE sts_müsteri SET müsteri_adi = %s, müsteri_soyadi = %s, müsteri_cepno=%s, müsteri_posta = %s, müsteri_adres = %s WHERE müsteri_id = %s"
                    val=(self.müsteriAd.get(),self.müsteriSoyad.get(),self.müsteriTelefon.get(),self.müsteriPosta.get(),self.müsteriAdres.get("1.0",'end-1c'),self.müsteriNo.get())
                    with self.connection.cursor() as cursor:
                        cursor.execute(guncelle,val)
                    messagebox.showinfo("BAŞARI","Ürün güncelleştirme işlemi tamamlandı")
                    self.müsteri_sorgula_classic()
                    self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)
                    self.clear_widget()
                else:
                    messagebox.showwarning("Bilinmeyen Müşteri","Güncellenmek istenen müşteri kayıtlarda bulunmamaktadır.")
        else:
            messagebox.showerror("Eksik Bilgi","Müşteri güncellemek için eksik bilgileri doldurunuz")

    def dizileribosalt(self):
        del self.müsteri_id[:]
        del self.müsteri_ad[:]
        del self.müsteri_soyad[:]
        del self.müsteri_tel[:]
        del self.müsteri_posta[:]
        del self.müsteri_adres[:]

    def müsteri_sorgula_id(self):
        with self.connection.cursor() as cursor:
            sorgulaid = "SELECT * FROM `sts_müsteri` ORDER BY CAST(`müsteri_id` AS UNSIGNED INTEGER) ASC"
            cursor.execute(sorgulaid)
            self.dizileribosalt()
            for kolon in cursor.fetchall():

                self.müsteri_id.append(kolon["müsteri_id"])
                self.müsteri_ad.append(kolon["müsteri_adi"])
                self.müsteri_soyad.append(kolon["müsteri_soyadi"])
                self.müsteri_tel.append(kolon["müsteri_cepno"])
                self.müsteri_posta.append(kolon["müsteri_posta"])
                self.müsteri_adres.append(kolon["müsteri_adres"])
    def müsteri_sorgula_ad(self):
        with self.connection.cursor() as cursor:
            sorguClassic = "SELECT * FROM `sts_müsteri` ORDER BY `müsteri_adi` ASC"
            cursor.execute(sorguClassic)
            self.dizileribosalt()
            for kolon in cursor.fetchall():

                self.müsteri_id.append(kolon["müsteri_id"])
                self.müsteri_ad.append(kolon["müsteri_adi"])
                self.müsteri_soyad.append(kolon["müsteri_soyadi"])
                self.müsteri_tel.append(kolon["müsteri_cepno"])
                self.müsteri_posta.append(kolon["müsteri_posta"])
                self.müsteri_adres.append(kolon["müsteri_adres"])
    def müsteri_sorgula_soyad(self):
        with self.connection.cursor() as cursor:
            sorguClassic = "SELECT * FROM `sts_müsteri` ORDER BY `müsteri_soyadi` ASC"
            cursor.execute(sorguClassic)
            self.dizileribosalt()
            for kolon in cursor.fetchall():

                self.müsteri_id.append(kolon["müsteri_id"])
                self.müsteri_ad.append(kolon["müsteri_adi"])
                self.müsteri_soyad.append(kolon["müsteri_soyadi"])
                self.müsteri_tel.append(kolon["müsteri_cepno"])
                self.müsteri_posta.append(kolon["müsteri_posta"])
                self.müsteri_adres.append(kolon["müsteri_adres"])
    def müsteri_sorgula_posta(self):
        with self.connection.cursor() as cursor:
            sorgulamüsteri = "SELECT * FROM `sts_müsteri` ORDER BY `müsteri_posta` ASC"
            cursor.execute(sorgulamüsteri)
            self.dizileribosalt()
            for kolon in cursor.fetchall():

                self.müsteri_id.append(kolon["müsteri_id"])
                self.müsteri_ad.append(kolon["müsteri_adi"])
                self.müsteri_soyad.append(kolon["müsteri_soyadi"])
                self.müsteri_tel.append(kolon["müsteri_cepno"])
                self.müsteri_posta.append(kolon["müsteri_posta"])
                self.müsteri_adres.append(kolon["müsteri_adres"])
    def müsteri_sorgula_adres(self):
        with self.connection.cursor() as cursor:
            sorgulamüsteri = "SELECT * FROM `sts_müsteri` ORDER BY `müsteri_adres` ASC"
            cursor.execute(sorgulamüsteri)
            self.dizileribosalt()
            for kolon in cursor.fetchall():

                self.müsteri_id.append(kolon["müsteri_id"])
                self.müsteri_ad.append(kolon["müsteri_adi"])
                self.müsteri_soyad.append(kolon["müsteri_soyadi"])
                self.müsteri_tel.append(kolon["müsteri_cepno"])
                self.müsteri_posta.append(kolon["müsteri_posta"])
                self.müsteri_adres.append(kolon["müsteri_adres"])


    def müsteri_sorgula_classic(self):
        self.müsteri_id=[]
        self.müsteri_ad=[]
        self.müsteri_soyad=[]
        self.müsteri_tel=[]
        self.müsteri_posta=[]
        self.müsteri_adres=[]
        with self.connection.cursor() as cursor:
            sorguClassic = "SELECT * FROM `sts_müsteri`"
            cursor.execute(sorguClassic)
            for kolon in cursor.fetchall():
                self.müsteri_id.append(kolon["müsteri_id"])
                self.müsteri_ad.append(kolon["müsteri_adi"])
                self.müsteri_soyad.append(kolon["müsteri_soyadi"])
                self.müsteri_posta.append(kolon["müsteri_posta"])
                self.müsteri_tel.append(kolon["müsteri_cepno"])
                self.müsteri_adres.append(kolon["müsteri_adres"])

    def listele(self,müsteriid=[],müsteriad=[],müsterisoyad=[],müsteriposta=[],müsteritel=[],müsteriadres=[]):
        self.listbox.delete(0,END)
        self.boyut = len(müsteriid)
        for i in range(0,self.boyut):
            cıktı="{:<5d}  {:<13s}  {:<8s}  {:<8s}  {:<30s}  {:<10s}  {:<10s}".format((i+1), müsteriid[i],müsteriad[i],müsterisoyad[i],müsteriposta[i],müsteritel[i],müsteriadres[i])
            self.listbox.insert(END,cıktı)
            if(i%2==1):
                self.listbox.itemconfig(i,bg="red")
    def listele_id(self,müsteriid=[],müsteriad=[],müsterisoyad=[],müsteriposta=[],müsteritel=[],müsteriadres=[]):
        if(self.checkid.get()==0):
            self.müsteri_sorgula_classic()
            self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)
        else:
            self.checkad.set(0)
            self.checksoyad.set(0)
            self.checkposta.set(0)
            self.checkadres.set(0)
            self.müsteri_sorgula_id()
            self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)

    def listele_ad(self,müsteriid=[],müsteriad=[],müsterisoyad=[],müsteriposta=[],müsteritel=[],müsteriadres=[]):
        if(self.checkad.get()==0):
            self.müsteri_sorgula_classic()
            self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)
        else:
            self.checkid.set(0)
            self.checksoyad.set(0)
            self.checkposta.set(0)
            self.checkadres.set(0)
            self.müsteri_sorgula_ad()
            self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)

    def listele_soyad(self,müsteriid=[],müsteriad=[],müsterisoyad=[],müsteriposta=[],müsteritel=[],müsteriadres=[]):
        if(self.checksoyad.get()==0):
            self.müsteri_sorgula_classic()
            self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)
        else:
            self.checkid.set(0)
            self.checkad.set(0)
            self.checkposta.set(0)
            self.checkadres.set(0)
            self.müsteri_sorgula_soyad()
            self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)

    def listele_posta(self,müsteriid=[],müsteriad=[],müsterisoyad=[],müsteriposta=[],müsteritel=[],müsteriadres=[]):
        if(self.checkposta.get()==0):
            self.müsteri_sorgula_classic()
            self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)
        else:
            self.checkid.set(0)
            self.checkad.set(0)
            self.checksoyad.set(0)
            self.checkadres.set(0)
            self.müsteri_sorgula_posta()
            self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)
    def listele_adres(self,müsteriid=[],müsteriad=[],müsterisoyad=[],müsteriposta=[],müsteritel=[],müsteriadres=[]):
        if(self.checkadres.get()==0):
            self.müsteri_sorgula_classic()
            self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)
        else:
            self.checkid.set(0)
            self.checkad.set(0)
            self.checkposta.set(0)
            self.checksoyad.set(0)
            self.müsteri_sorgula_adres()
            self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)

    def clear_widget(self,event=None):
        self.müsteriNo.config(state="normal")
        self.müsteriNo.delete(0,"end")
        self.müsteriAd.delete(0,"end")
        self.müsteriSoyad.delete(0,"end")
        self.müsteriTelefon.delete(0,"end")
        self.müsteriPosta.delete(0,"end")
        self.müsteriAdres.delete("1.0","end")

    def mail_gonder(self,posta):
	# DOLDURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
        self.gecicisifre = "NoneNone"
        # Hesap bilgilerimiz
   //     self.kullanıcı="MAİL ADRESİ GİR"
 //       self.kullanıcı_sifresi = 'MAİL ADRESİNİN ŞİFRESİNİ GİR'
        self.alıcı = posta         # alıcının mail adresi
        konu = "Gecici Sifreniz"
        msj = """Merhaba,
        Gecici Sifreniz: {}""".format(self.gecicisifre)
        email_text = """
        From: {}
        To: {}
        Subject: {}
        {}
        """ .format(self.kullanıcı,self.alıcı, konu, msj)

        server = smtplib.SMTP('smtp.gmail.com:587')   #servere bağlanmak için gerekli host ve portu belirttik
        server.starttls() #serveri TLS(bütün bağlantı şifreli olucak bilgiler korunucak) bağlantısı ile başlattık
        server.login(self.kullanıcı, self.kullanıcı_sifresi)   # Gmail SMTP server'ına giriş yaptık
        server.sendmail(self.kullanıcı, self.alıcı, email_text) # Mail'imizi gönderdik
        server.close()     # SMTP serverimizi kapattık

    def id_kontrol(self,kontrol,event=None):
        try:
            operatörler="!'^+%&/()=?<>,+-*_#$½{[]\|}~;:."
            sayi=self.kontrol1.get()
            if((sayi[len(sayi)-1].isalpha()==True) or (sayi[len(sayi)-1] in operatörler)):
                    self.müsteriNo.delete(len(sayi)-1,"end")
        except:
            print("tm")

    def listbox_select(self,event):
        #try:
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
                sql1="SELECT  * FROM sts_müsteri WHERE müsteri_id = %s"%self.silinecek_id
                sorgu1 = cursor.execute(sql1)
                for i in cursor.fetchall():
                    no=i["müsteri_id"]
                    ad=i["müsteri_adi"]
                    soyad=i["müsteri_soyadi"]
                    posta=i["müsteri_posta"]
                    tel=i["müsteri_cepno"]
                    adres = i["müsteri_adres"]
            self.müsteriNo.config(state="normal")
            self.müsteriNo.delete(0,"end")
            self.müsteriNo.insert("end",no)
            self.müsteriNo.config(state="readonly")
            self.müsteriAd.delete(0,"end")
            self.müsteriAd.insert("end",ad)
            self.müsteriSoyad.delete(0,"end")
            self.müsteriSoyad.insert("end",soyad)
            self.müsteriPosta.delete(0,"end")
            self.müsteriPosta.insert("end",posta)

            self.müsteriTelefon.delete(0,"end")
            self.müsteriTelefon.insert("end",tel)

            self.müsteriAdres.delete("1.0","end")
            self.müsteriAdres.insert("end",adres)

        #except:
            #print(1)



    def __init__(self):

        self.connection = pymysql.connect(host='localhost',
                                                 user='root',
                                                 password='',
                                                 db='stoktakipsistemi',
                                                 charset='utf8mb4',
                                                 cursorclass=pymysql.cursors.DictCursor)

        müsteri_pencere = Toplevel()
        self.müsteri_pencere = müsteri_pencere;
        müsteri_pencere.title("Müşteri İşlemleri")
        müsteri_pencere.geometry("780x560+300+30")
        #müsteri_pencere.resizable(0,0)
        canvas = Canvas(müsteri_pencere,width=780,height=560)
        myimage = PhotoImage(file = "StokTakipSistemi\\images\\arkaplan2.png")
        canvas.create_image(0,0,anchor=NW, image=myimage)

        geriButton = Button(canvas,text="Geri Gel")
        geriButton.place(x=150,y=0)
        resimg=self.imageAdd("geri")
        geriButton.config(image=resimg,width="45", height="33",command=self.müsteri_pencere.destroy,bg="white")



        temizleButton = Button(canvas,text="Temizle",command=self.clear_widget,bg="white")
        temizleButton.place(x=0,y=0)
        resim3=self.imageAdd("temizleme")
        temizleButton.config(image=resim3,width="35", height="20")


        müsteriNolabel = Label(canvas, text="Müşteri No")
        müsteriNolabel.place(x=20, y=50)
        self.kontrol1=StringVar()
        self.kontrol1.trace("w", lambda name, index, mode, kontrol=self.kontrol1:self.id_kontrol(self.kontrol1))
        self.müsteriNo = Entry(canvas,width=22,textvariable=self.kontrol1)
        self.müsteriNo.place(x=140,y=50)

        müsteriAdLabel = Label(canvas, text="Müşteri Ad")
        müsteriAdLabel.place(x=20 , y=80)
        self.müsteriAd = Entry(canvas, width=22)
        self.müsteriAd.place(x=140 , y=80)

        müsteriSoyadLabel = Label(canvas,text="Müşteri Soyad")
        müsteriSoyadLabel.place(x=20, y=110)
        self.müsteriSoyad = Entry(canvas,width=22)
        self.müsteriSoyad.place(x=140,y=110)

        müsteriTelefonLabel = Label(canvas,text="Müşteri Tel.")
        müsteriTelefonLabel.place(x=20 ,y=140)
        self.müsteriTelefon = Entry(canvas, width=22)
        self.müsteriTelefon.place(x=140 , y=140)

        müsteripostaLabel = Label(canvas,text="Müşteri E-Posta")
        müsteripostaLabel.place(x=20,y=170)
        self.müsteriPosta = Entry(canvas,width=22)
        self.müsteriPosta.place(x=140, y=170)

        adreslb = Label(canvas, text="Müşteri Adres   ")
        adreslb.place(x=20, y=200)
        self.müsteriAdres = Text(canvas,width=17,height=2)
        self.müsteriAdres.place(x=140, y=200)



        self.müsteri_Ekle = Button(canvas,text="Ekle",width="24",height="4",bg="#fbf8f8",command=self.müsteriEkle)
        self.müsteri_Ekle.place(x=320,y=50)
        resimEkle=self.imageAdd("ekle")
        self.müsteri_Ekle.config(image=resimEkle,width="70", height="60",compound="top")

        self.müsteri_Sil = Button(canvas,text="Sil",width="24",height="4",bg="#fbf8f8",command=self.müsteriSil)
        self.müsteri_Sil.place(x=430,y=50)
        resimSil=self.imageAdd("sil")
        self.müsteri_Sil.config(image=resimSil,width="70", height="60",compound="top")

        self.müsteri_Guncelle = Button(canvas,text="Güncelle",width="24",height="4",bg="#fbf8f8",command=self.müsteriGuncelle)
        self.müsteri_Guncelle.place(x=545,y=50)
        resimGüncelle=self.imageAdd("güncelle")
        self.müsteri_Guncelle.config(image=resimGüncelle,width="70", height="60",compound="top")


        arama = Label(canvas,text="Müsteri Arama :",fg="red")
        arama.config(font=("Times", "14", "bold italic"))
        arama.place(x=315 , y=160)
        self.sv = StringVar()
        self.sv.trace("w", lambda name, index, mode, sv=self.sv:self.aramas_olacaklar(self.sv))
        self.müsteriArama = Entry(canvas,width="22",textvariable=self.sv)
        self.müsteriArama.place(x=455,y=165)
        self.müsteriArama.insert(0,"Müsteri, id veya ad...")
        self.müsteriArama.bind('<Button-1>', self.arama_olacaklar)


        self.checkid =IntVar()
        self.Check_id_button = Checkbutton(canvas , text="İD" , variable = self.checkid , onvalue = 1 , offvalue = 0 ,height = 1, width="8",bg="white",fg="black",font=("Times","12","bold italic"),command=self.listele_id)
        self.Check_id_button.place(x=40,y=260)

        self.checkad =IntVar()
        self.Check_ad_button = Checkbutton(canvas , text="AD" , variable = self.checkad , onvalue = 1 , offvalue = 0 ,height = 1, width="6",bg="white",fg="black",font=("Times","12","bold italic"),command=self.listele_ad)
        self.Check_ad_button.place(x=140,y=260)

        self.checksoyad =IntVar()
        self.Check_soyad_button = Checkbutton(canvas , text="Soyad" , variable = self.checksoyad , onvalue = 1 , offvalue = 0 ,height = 1, width="6",bg="white",fg="black",font=("Times","12","bold italic"),command=self.listele_soyad )
        self.Check_soyad_button.place(x=225,y=260)

        self.checkposta =IntVar()
        self.Check_posta_button = Checkbutton(canvas , text="E-Posta Adresi" , variable = self.checkposta , onvalue = 1 , offvalue = 0 ,height = 1, width="18",bg="white",fg="black",font=("Times","12","bold italic"),command=self.listele_posta)
        self.Check_posta_button.place(x=300,y=260)

        telefonbaslik = Label(canvas, text="Tel", width="14",height="1", bg="white",fg="black",font=("Times","12","bold italic"))
        telefonbaslik.place(x=490,y=260)

        self.checkadres =IntVar()
        self.Check_adres_button = Checkbutton(canvas , text="Adres" , variable = self.checkadres , onvalue = 1 , offvalue = 0 ,height = 1, width="8",bg="white",fg="black",font=("Times","12","bold italic"),command=self.listele_adres)
        self.Check_adres_button.place(x=600,y=260)



        self.scrollbar = Scrollbar(self.müsteri_pencere)
        self.listbox = Listbox(canvas,width="100",height="12",bg="black",fg="white",font=('consolas',10),yscrollcommand = self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.bind('<<ListboxSelect>>',self.listbox_select)
        self.listbox.place(x=20, y=290)

        self.müsteri_sorgula_classic()
        self.listele(self.müsteri_id,self.müsteri_ad,self.müsteri_soyad,self.müsteri_posta,self.müsteri_tel,self.müsteri_adres)



        canvas.pack()
        müsteri_pencere.mainloop()
