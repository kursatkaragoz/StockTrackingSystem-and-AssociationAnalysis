from tkinter import *
import pymysql.cursors
from tkinter import ttk
from tkinter import messagebox
import random
import smtplib


class Giris():


    def imageAdd(self,uzantı):
        img = PhotoImage(file = "StokTakipSistemi\\images\\"+uzantı+".png")
        return img
    def kayitol_yonlen(self):

        self.pencere.destroy()
        from STS_KayitOl import kayitol
        kayitolac = kayitol()
    def kapat(self):
        self.pencere.destroy()
        sys.exit()



    global firstclick
    firstclick=True
    def on_entry_click(self,event=None):

            global firstclick

            if firstclick: # if this is the first time they clicked it
                firstclick = False
                self.kullanici_adi.delete(0, "end")

    def bosluk_kullanici_kontrol(self,kontrol,event=None):
        try:
            operatörler="' '"
            sayi=self.kontrol1.get()
            if(sayi[len(sayi)-1] in operatörler):
                    self.kullanici_adi.delete(len(sayi)-1,"end")
        except:
            print("tm")
    def bosluk_sifre_kontrol(self,kontrol,event=None):
        try:
            operatörler="' '"
            sayi=self.kontrol2.get()
            if(sayi[len(sayi)-1] in operatörler):
                    self.sifre.delete(len(sayi)-1,"end")
        except:
            print("tm")


    def __init__(self):


        pencere = Tk()
        self.pencere = pencere
        pencere.title("Kullanıcı Giriş Sayfası")
        pencere.geometry("360x250+500+100")
        pencere.resizable(0,0)
        canvas = Canvas(pencere,width=360,height=250)


        myimage = PhotoImage(file = "StokTakipSistemi\\images\\girisarkaplan.png")
        canvas.create_image(0,0,anchor=NW, image=myimage)


        kapatButton = Button(canvas,text="Kapat",bg="white",command=self.kapat)
        kapatButton.place(x=160,y=20)
        resim2=self.imageAdd("kapat")
        kapatButton.config(image=resim2,width=45, height=35)

        kayitolButton =Button(canvas,text="kayit ol",bg="white",command=self.kayitol_yonlen)
        kayitolButton.place(x=265,y=0)
        kayitol=self.imageAdd("kayitol")
        kayitolButton.config(image=kayitol,width=90, height=20)



        kullanici_adilb = Label(canvas,text="Kullanıcı Adı ",width=10,bg="gray",fg="white")
        kullanici_adilb.place(x=30,y=80)
        self.kontrol1=StringVar()
        self.kontrol1.trace("w", lambda name, index, mode, kontrol=self.kontrol1:self.bosluk_kullanici_kontrol(self.kontrol1))
        self.kullanici_adi = Entry(canvas, insertbackground="red",textvariable=self.kontrol1)
        self.kullanici_adi.insert(0, 'TC veya Posta Adresiniz...')
        self.kullanici_adi.bind('<Button-1>', self.on_entry_click)
        self.kullanici_adi.place(x=130,y=80)

        sifrelb = Label(canvas, text="Sifre",width=10,bg="gray",fg="white")
        sifrelb.place(x=30, y=120)
        self.kontrol2=StringVar()
        self.kontrol2.trace("w", lambda name, index, mode, kontrol=self.kontrol2:self.bosluk_sifre_kontrol(self.kontrol2))
        self.sifre = Entry(canvas,show="*", insertbackground="red",textvariable=self.kontrol2)
        self.sifre.place(x=130, y=120)

        self.CheckVar1 = IntVar()
        self.hatirla = Checkbutton(canvas , text="Beni Hatırla" , variable = self.CheckVar1 , onvalue = 1 , offvalue = 0 ,height = 1, width=0,bg="gray",fg="black" )
        self.hatirla.place(x=265,y=117)

        self.girisyap = Button(canvas,text="GirisYap",command=self.girisYap)
        self.girisyap.place(x=30,y=160)
        resim=self.imageAdd("giris")
        self.girisyap.config(image =resim, width = 70 , height = 20,command=self.girisYap)
        pencere.bind('<Return>', self.girisYap)

        self.sifremiunuttum = Button(canvas,text="Şifremi Unuttum",width="16",bg="gray",fg="white",command=self.sifreSifirla)
        self.sifremiunuttum.place(x=130,y=160)
        self.acilis_Kontrol()
        self.k_adi=None
        self.giris_turu=None

        canvas.pack()
        pencere.mainloop()

    def girisYap(self,event=None):


        if(self.kullanici_adi.get()=="" or self.sifre.get()==""):
            messagebox.showwarning("Uyarı","Kullanıcı Adı ve Sifrenizi Giriniz")
        else:

                self.connection = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='',
                                                     db='stoktakipsistemi',
                                                     charset='utf8mb4',
                                                     cursorclass=pymysql.cursors.DictCursor)

                self.kullanıcıadı = self.kullanici_adi.get()
                self.sıfre = self.sifre.get()

                self.müsteri_idler = []
                self.müsteri_isimler=[]
                self.müsteri_postalar=[]
                self.müsteri_sifreler=[]

                self.yetkili_idler=[]
                self.yetkili_isimler=[]
                self.yetkili_postalar=[]
                self.yetkili_sifreler=[]



                with self.connection.cursor() as cursor:
                    sqlYetkili="SELECT * FROM `sts_yetkili`"
                    cursor.execute(sqlYetkili)
                    for i in cursor.fetchall():
                        self.yetkili_idler.append(i["yetkili_id"])
                        self.yetkili_postalar.append(i["yetkili_posta"])
                        self.yetkili_sifreler.append(i["yetkili_sifre"])
                        self.yetkili_isimler.append(i["yetkili_adi"])

                    sqlMüsteri ="SELECT * FROM `sts_müsteri`"
                    cursor.execute(sqlMüsteri)
                    for i in cursor.fetchall():
                        self.müsteri_idler.append(i["müsteri_id"])
                        self.müsteri_postalar.append(i["müsteri_posta"])
                        self.müsteri_sifreler.append(i["müsteri_sifre"])
                        self.müsteri_isimler.append(i["müsteri_adi"])



#####################################   KULLANICI MÜŞTERİ Mİ KONTROLÜ #####################
                müsteri_sayisi=len(self.müsteri_idler)
                self.sonuc=FALSE

                for i in range(0,müsteri_sayisi):
                    if(self.müsteri_idler[i] == self.kullanıcıadı):

                        if(self.müsteri_sifreler[i] == self.sıfre):
                            print("GirisYapabilir Müsteri")
                            self.sonuc=TRUE
                            if(self.CheckVar1.get()==1):
                                    with self.connection.cursor() as cursor:
                                        temizle="DELETE FROM sts_kayıt"
                                        cursor.execute(temizle)
                                        gecici="INSERT INTO sts_kayıt(uye_kullaniciadi,uye_sifre)\
                                        VALUES('%s','%s')"%\
                                        (self.kullanıcıadı,self.sıfre)
                                        cursor.execute(gecici)
                            else:
                                with self.connection.cursor() as cursor:
                                    temizle="DELETE FROM sts_kayıt"
                                    cursor.execute(temizle)
                                pass
                            self.k_adi = self.kullanıcıadı
                            self.giris_turu="Müsteri"
                            self.pencere.destroy()


                        else:
                            print("giris yapamaz")

                     #########################  HATA VARSA POSTA GİRİŞİ VARDIR ##################
                    else:
                        for i in range(0,müsteri_sayisi):
                            if(self.müsteri_postalar[i]==self.kullanıcıadı):
                                if(self.müsteri_sifreler[i] == self.sıfre):
                                    print("GirisYapabilir Müsteri")
                                    self.sonuc=TRUE
                                    if(self.CheckVar1.get()==1):
                                            with self.connection.cursor() as cursor:
                                                temizle="DELETE FROM sts_kayıt"
                                                cursor.execute(temizle)
                                                gecici="INSERT INTO sts_kayıt(uye_kullaniciadi,uye_sifre)\
                                                VALUES('%s','%s')"%\
                                                (self.kullanıcıadı,self.sıfre)
                                                cursor.execute(gecici)
                                    else:
                                        with self.connection.cursor() as cursor:
                                            temizle="DELETE FROM sts_kayıt"
                                            cursor.execute(temizle)
                                        pass
                                    self.k_adi = self.kullanıcıadı
                                    self.giris_turu="Müsteri"
                                    try:
                                        self.pencere.destroy()
                                    except:
                                        print("hata nedensiz")


                pass
########################################   MÜŞERİ DEĞİLSE YETKİLİ (ADMİN) DİR ###############################################
                if(self.sonuc==FALSE):
                    try:

                        yetkili_sayisi=len(self.yetkili_idler)
                        for y in range(0,yetkili_sayisi):
                            if(self.yetkili_idler[y] == int(self.kullanıcıadı)):
                                if(self.yetkili_sifreler[y] == self.sıfre):
                                    self.sonuc=TRUE
                                    if(self.CheckVar1.get()==1):
                                        with self.connection.cursor() as cursor:
                                            temizle="DELETE FROM sts_kayıt"
                                            cursor.execute(temizle)
                                            gecici="INSERT INTO sts_kayıt(uye_kullaniciadi,uye_sifre)\
                                            VALUES('%s','%s')"%\
                                            (self.kullanıcıadı,self.sıfre)
                                            cursor.execute(gecici)
                                    if(self.CheckVar1.get()==0):
                                        with self.connection.cursor() as cursor:
                                            temizle="DELETE FROM sts_kayıt"
                                            cursor.execute(temizle)
                                    self.k_adi = self.kullanıcıadı
                                    self.giris_turu="Admin"
                                    self.pencere.destroy()
                                else:
                                    print("giriş yapamaz")
                    except: #########################  HATA VARSA POSTA GİRİŞİ VARDIR ##################
                        print("hata var ADMİN SANDI")
                        for y in range(0,yetkili_sayisi):
                            if(self.yetkili_postalar[y]==str(self.kullanıcıadı)):
                                if(self.yetkili_sifreler[y] == self.sıfre):
                                    print("GirisYapabilir Yetkili")
                                    self.sonuc=TRUE
                                    if(self.CheckVar1.get()==1):
                                        with self.connection.cursor() as cursor:

                                            temizle="DELETE FROM sts_kayıt"
                                            cursor.execute(temizle)
                                            gecici="INSERT INTO sts_kayıt(uye_kullaniciadi,uye_sifre)\
                                            VALUES('%s','%s')"%\
                                            (self.kullanıcıadı,self.sıfre)
                                            cursor.execute(gecici)
                                    else:
                                        with self.connection.cursor() as cursor:
                                            temizle="DELETE FROM sts_kayıt"
                                            cursor.execute(temizle)
                                    self.k_adi = self.kullanıcıadı
                                    self.giris_turu="Admin"
                                    self.pencere.destroy()
                                    #sys.exit
                                    #anaSayfaYonlen =

                                else:

                                    print("giris yapamaz")
                if(self.sonuc==FALSE):
                    messagebox.showerror("HATA","Bilgiler eksik veya hatalı")

    def acilis_Kontrol(self):
        self.connection_first = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='',
                                                     db='stoktakipsistemi',
                                                     charset='utf8mb4',
                                                     cursorclass=pymysql.cursors.DictCursor)
        self.hatirla_kullaniciadi=[]
        self.hatirla_kullanicisifre=[]
        with self.connection_first.cursor() as cursor:
                    sqlFirst="SELECT * FROM `sts_kayıt`"
                    cursor.execute(sqlFirst)
                    for i in cursor.fetchall():
                        self.hatirla_kullaniciadi.append(i["uye_kullaniciadi"])
                        self.hatirla_kullanicisifre.append(i["uye_sifre"])
        if(len(self.hatirla_kullaniciadi)>0):
            print("aktif kullanıcı var")
            self.kullanici_adi.delete(0, "end")
            self.kullanici_adi.insert(END,self.hatirla_kullaniciadi[0])
            self.sifre.insert(END,self.hatirla_kullanicisifre[0])
            self.CheckVar1.set(1)
    def sifreSifirla(self):
        self.pencere.destroy()
        self.pencere2 = Tk()
        self.pencere2.title("E-Posta Dogrulama")
        self.pencere2.geometry("360x130+500+200")
        self.canvas2 = Canvas(self.pencere2,width=360,height=130)
        img = PhotoImage(file ="StokTakipSistemi\\images\\hafıza.png")
        self.canvas2.create_image(0,0,anchor=NW, image=img)
        self.label = Label(self.canvas2,text="Dogrulama Kodu E-postanıza Gönderilecektir",bg="#4abed9",fg="black")
        self.label.place(x=10,y=15)
        self.label = Label(self.canvas2,text="E-posta Adresiniz",bg="#4abed9",fg="black")
        self.label.place(x=10,y=45)
        self.eposta = Entry(self.canvas2,width=30)
        self.eposta.place(x=120,y=45)
        self.send = Button(self.canvas2,text="Gönder",width=12,bg="gray",command=self.gonder)
        self.send.place(x=10,y=90)
        self.vazgeç = Button(self.canvas2,text="Vazgeç",width=12,bg="gray",command=self.vazgeç)
        self.vazgeç.place(x=120,y=90)
        self.pencere2.bind('<Return>', self.gonder)

        self.canvas2.pack()
        self.pencere2.mainloop()

    def gonder(self,event=None):

        self.connection = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='',
                                                     db='stoktakipsistemi',
                                                     charset='utf8mb4',
                                                     cursorclass=pymysql.cursors.DictCursor)

        self.müsteri_idler = []
        self.müsteri_postalar=[]
        self.yetkili_idler=[]
        self.yetkili_postalar=[]
        with self.connection.cursor() as cursor:
            sqlYetkili="SELECT * FROM `sts_yetkili`"
            cursor.execute(sqlYetkili)
            for i in cursor.fetchall():
                self.yetkili_idler.append(i["yetkili_id"])
                self.yetkili_postalar.append(i["yetkili_posta"])

            sqlMüsteri ="SELECT * FROM `sts_müsteri`"
            cursor.execute(sqlMüsteri)
            for i in cursor.fetchall():
                self.müsteri_idler.append(i["müsteri_id"])
                self.müsteri_postalar.append(i["müsteri_posta"])


        self.dogrulanacak_posta = self.eposta.get()
        self.uye_durum = "HİC"
        for y in range(0,len(self.yetkili_idler)):
            if(self.yetkili_postalar[y] == self.dogrulanacak_posta):
                self.uye_durum = "Yetkili"
                self.guncellenecekposta=self.yetkili_postalar[y]

        for y in range(0,len(self.müsteri_idler)):
            if(self.müsteri_postalar[y] == self.dogrulanacak_posta):
                self.uye_durum = "Müsteri"
                self.guncellenecekposta=self.müsteri_postalar[y]
        if(self.uye_durum == "HİC"):  ##Üye değil ise
            messagebox.showinfo("Uye Hatası","Bu E-posta sisteme kayıtlı değildir")

        if(self.uye_durum !="HİC"):
            self.mail_gonder()
            messagebox.showinfo("Kod Dogrulama","E-Postanızdaki doğrulama kodunu 120sn içerisinde giriniz.")
            self.pencere3 = Toplevel()
            self.pencere3.geometry("380x130+850+270")
            self.canvas3 = Canvas(self.pencere3,width=380,height=130)
            img2 = PhotoImage(file ="StokTakipSistemi\\images\\hafıza.png")
            self.canvas3.create_image(0,0,anchor=NW, image=img2)
            self.label2 = Label(self.canvas3,text="Saniye içinde epostanızdaki dogrulama kodunu giriniz",bg="#4abed9",fg="black")
            self.label2.place(x=40,y=30)
            self.sayac = StringVar()
            self.sayac.set("asd")
            self.sayac2 = Label(self.canvas3,width=2,bg="#4abed9",fg="black")
            self.sayac2.place(x=10,y=30)
            self.onaykodu = Entry(self.canvas3,width=15)
            self.onaykodu.place(x=150,y=60)
            self.onay = Button(self.canvas3,text="Onayla",width=12,bg="gray",command=self.onayla)
            self.pencere3.bind('<Return>', self.onayla)
            self.onay.place(x=40,y=90)
            self.saniye = 120

            a =self.sayım()
            self.canvas3.pack()
            self.pencere3.mainloop()
    def onayla(self,event=None):
        if(int(self.onaykodu.get()) != self.random_sayi):
            messagebox.showinfo("Hata","Hatalı Kod Girişi Yaptınız")
        else:

            self.pencere3.destroy()
            self.pencere4 = Toplevel()
            self.pencere4.geometry("250x200+850+270")
            self.canvas4 = Canvas(self.pencere4,width=300,height=200)
            img3 = PhotoImage(file ="StokTakipSistemi\\images\\hafıza.png")
            self.canvas4.create_image(0,0,anchor=NW, image=img3)
            self.label2 = Label(self.canvas4,text="Yeni Parolanızı Oluşturunuz",bg="#4abed9",fg="black")
            self.label2.place(x=60,y=20)

            self.pass1lb=Label(self.canvas4,text="Yeni Parola",bg="#4abed9",fg="black")
            self.pass1lb.place(x=30,y=60)
            self.pass1 = Entry(self.canvas4,width=18,show="*")
            self.pass1.place(x=110,y=60)

            self.pass2lb=Label(self.canvas4,text="Yeni Parola",bg="#4abed9",fg="black")
            self.pass2lb.place(x=30,y=90)
            self.pass2 = Entry(self.canvas4,width=18,show="*")
            self.pass2.place(x=110,y=90)

            self.tamam = Button(self.canvas4,text="Kaydet",width=25,bg="gray",command=self.yeniparola_kaydet)
            self.tamam.place(x=30,y=130)
            self.pencere4.bind('<Return>', self.yeniparola_kaydet)

            self.canvas4.pack()
            self.pencere4.mainloop()

    def yeniparola_kaydet(self,event=None):

        if(self.pass1.get()!= self.pass2.get()):
            messagebox.showwarning("Parola Hatası","İki Parola Örtüşmüyor")
        else:
            if(self.uye_durum=="Müsteri"):
                with self.connection.cursor() as cursor:
                    basarı=cursor.execute ("UPDATE sts_müsteri SET müsteri_sifre='%s'  WHERE müsteri_posta='%s' " % (self.pass1.get(),self.guncellenecekposta))
                    if(basarı==1):
                        messagebox.showinfo("BAŞARI","Yeni Parolanız Oluşturuldu.")
                        self.pencere4.destroy()
                        self.pencere2.destroy()
                        sys.exit
                        loginac=Giris()
                    else:
                        print("hata var")
            if(self.uye_durum=="Yetkili"):
                with self.connection.cursor() as cursor:
                    cursor.execute ("UPDATE sts_yetkili SET yetkili_sifre='%s'  WHERE yetkili_posta='%s' " % (self.pass1.get(),self.guncellenecekposta))
                    messagebox.showinfo("BAŞARI","Yeni Parolanız Oluşturuldu.")
                    self.pencere4.destroy()
                    self.pencere2.destroy()
                    sys.exit

                    loginac=Giris()



    def vazgeç(self):

        self.pencere2.destroy()
        from STS_AnaSayfa import AnaSayfa
        calistir = AnaSayfa()

    def sayım(self):

        self.sayac2.config(text=str(self.saniye))
        self.sayac2.after(1000,self.sayım)
        self.saniye = self.saniye - 1
        if (self.saniye == 0):
            self.sayac2.destroy()
            self.tekrargonderButton = Button(self.canvas3,text="Tekrar Gönder",width=12,command = self.tekrargonder, bg="gray")
            self.tekrargonderButton.place(x=190,y=90)

    def tekrargonder(self):
        self.mail_gonder()
        self.tekrargonderButton.destroy()
        self.saniye = 120
        self.sayac2 = Label(self.canvas3,width=2,bg="#4abed9",fg="black")
        self.sayac2.place(x=10,y=30)
        self.sayım()
    def mail_gonder(self):
        self.random_sayi = random.randint(100000,999999)
        print("giden random : {}".format(self.random_sayi))
		
		######################################DOLDUR#############3
        # Hesap bilgilerimiz
        self.kullanıcı="(REFERANS ALINACAK MAİL ADRESİ GİR"
//        self.kullanıcı_sifresi = 'REFERANS MAİL ADRESİNİN ŞİFRESİ'
//        self.alıcı = self.eposta.get()          # alıcının mail adresi
        konu = "Dogrulama_Kodu"
        msj = """Merhaba,
        Dogrulama Kodunuz: {}""".format(self.random_sayi)
        email_text = """
        From: {}
        To: {}
        Subject: {}
        {}
        """ .format(self.kullanıcı,self.alıcı, konu, msj)
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')   #servere bağlanmak için gerekli host ve portu belirttik
            server.starttls() #serveri TLS(bütün bağlantı şifreli olucak bilgiler korunucak) bağlantısı ile başlattık
            server.login(self.kullanıcı, self.kullanıcı_sifresi)   # Gmail SMTP server'ına giriş yaptık
            server.sendmail(self.kullanıcı, self.alıcı, email_text) # Mail'imizi gönderdik
            server.close()     # SMTP serverimizi kapattık
        except:
            messagebox.showerror("HATA","Server geçici süre hizmet dışıdır. Kayıt Tamamlanamadı.")

pass


