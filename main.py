#create a database named online_library
#change user name and password of db.connect @ line 437



from tkinter import *
from tkinter import messagebox
import datetime
import os
import shutil
import pymysql
import time
import tkinter.filedialog

class Mainwin:
    def __init__(self,sqlhelper):
        self.sqlhelper = sqlhelper
        self.canvas = Canvas(win,width = 800,height=30,bg="skyblue")
        self.curuser =None
        self.canvas.pack()
        self.x = 2
        self.des = 0
        self.actview = 0
        self.weltext = "Welcome to Online Library"
        self.canvaswidth = self.canvas.winfo_width()
        self.id1 = self.canvas.create_text(self.canvaswidth,15,text=self.weltext,fill="red",font = ('Eras Bold ITC',14))
        self.rootframe()


    def textani(self):
        self.canvas.move(self.id1,self.x,0)
        pos = self.canvas.coords(self.id1)
        if (pos[0] >= 660):
            self.x = -2
        elif (pos[0] <= 130):
            self.x = 2
    def b1f(self):
        self.sqlhelper.close()
        m.des = 1
        win.destroy()

    def _login(self,event):
        self.login()

    def login(self):
        user = str(self.id5.get())
        passw = str(self.id6.get())
        ut = str(self.variable.get())
        try:
            if "Select" == self.variable.get():
                messagebox.showerror("User type","Select your user type")
                raise AssertionError
            if ut == "Member":
                self.data =self.sqlhelper.retuserdetails(user)
            elif self.variable.get() == "Admin":
                self.data =self.sqlhelper.retadmindetails(user)
            if self.data==None:
                messagebox.showerror("Recheck Username","Username incorrect. New user please register")
                raise ValueError
            if self.data[1] == passw:
                if ut == "Member":
                    self.curuser = user
                    self.transit12()

                elif ut == "Admin":
                    self.curuser = user
                    self.transit13()
            else:
                raise ValueError
        except ValueError:
            self.id7 = self.canvas1.create_text(200,280,text = "User ID or Password incorrect",font = ("Bahnschrift",9,"bold"),fill = "red",anchor ="sw")
            pass

    def transit12(self):
       self.canvas1.destroy()
       win.unbind("<Return>")
       self.userframe()

    def transit21(self):
        self.curuser = None
        self.frame1.destroy()
        self.rootframe()

    def transit13(self):
        self.canvas1.destroy()
        win.unbind("<Return>")
        self.adminframe()

    def transit31(self):
        self.curuser = None
        try:
            self.sel.destroy()
        except:
            pass
        try:
            self.temp.destroy()
        except:
            pass
        self.frame2.destroy()
        self.rootframe()

    def transit34(self):
        self.frame2.pack_forget()
        win.bind('<Return>', self._register)
        self.regiswin("Add Admin",self.register)
        self.b3.config(command = self.transit43)

    def transit43(self):
        self.canvas2.destroy()
        win.unbind("<Return>")
        self.adminframe()

    def transit14(self):
        self.canvas1.destroy()
        win.unbind("<Return>")
        self.regiswin("Register",self.register)
        win.bind("<Return>",self._register)

    def transit41(self):
        self.canvas2.destroy()
        win.unbind("<Return>")
        self.rootframe()
        win.bind("<Return>",self._login)

    def _register(self,event):
        self.register()

    def register(self):
        cp = self.id8.get()
        p = self.id6.get()
        u = self.id5.get()
        if u!="":
            if p == cp and p != "":
                try:
                    if self.b2["text"] == "Register":
                        self.sqlhelper.adduser(u,p)
                        self.transit41()
                    else:
                        self.sqlhelper.addadmin(u,p)
                        self.transit43()
                    messagebox.showinfo("Registered","Succesfully Registered\nLogin now")
                except:
                    messagebox.showerror("Error","Sorry,User name already taken.\nTry another name")
            else:
                messagebox.showerror("Error","Password does not match. \nRetry!")
        else:
            messagebox.showerror("Error","User Name can't be empty. \nRetry!")

    def search(self):
        key = self.searchentry.get()
        self.data = self.sqlhelper.search(key,self.viewsub)
        self.adactframe.destroy()
        self.adactframe1.destroy()
        self.adact2.destroy()
        self.viewframe(self.data)

    def choosefile(self):
        self.file = tkinter.filedialog.askopenfilename()
        tempname = self.file.rpartition("/")
        pass

    def upload(self):
        bookname = self.id5.get()
        author = self.id6.get()
        publications = self.id8.get()
        self.dest = self.sqlhelper.rootdir + self.sub
        tempname = self.file.rpartition("/")
        booktuple = (self.sub,bookname,author,publications,tempname[-1])
        self.sqlhelper.copyit(self.file,self.dest)
        self.sqlhelper.adminuploadrec(self.curuser,self.sub,tempname[-1])
        self.sqlhelper.insexistings(booktuple,tempname[-1])
        messagebox.showinfo("Uploaded","Uploaded Succesfully!")
        self.canvas2.destroy()
        self.adminframe()


    def viewadminactivity(self):
        if self.actview == 0:
            data=self.sqlhelper.viewadminactivity()
            self.adminactivityframe(("Time","Admin","Book Name","Subject"),data)

    def adactclose(self):
            self.actview = 0
            self.temp.destroy()

    def view(self,sub):
        if self.actview == 0:
            self.viewsub = sub
            data=self.sqlhelper.getfiles(self.viewsub)
            self.viewframe(data)

    def openfile(self,i):
        sbookname = self.allbutton[i][0]["text"]
        self.sqlhelper.cursor.execute("select pdfname from existingfiles where bookname = '%s' and sub = '%s' " %(sbookname,self.viewsub))
        self.pdfname = self.sqlhelper.cursor.fetchall()
        self.pdfname = str(self.pdfname[0])
        a = self.pdfname.split("'")
        bookname = a[1]
        print(bookname)
        path = self.sqlhelper.rootdir + "/" + self.viewsub + "/" + bookname
        try:
            if messagebox.askyesno("Python","Would you like to open the data?") == True:
                os.startfile(path)
                self.adactclose()
            else:
                pass
        except:
            messagebox.showerror("Error","File not found")




    #MAIN GUI

    def regiswin(self,btext,func):
        self.canvas2 = Canvas(win,width = 800, height = 500)
        self.canvas2.pack()
        self.background_image = PhotoImage(file = "lib.gif")
        self.bg1 = self.canvas2.create_image(0, 0, image=self.background_image, anchor=NW)
        self.b2 = Button(self.canvas2,text= btext,command = func,width = 10,bg = "#724006",fg="white")
        self.b3 = Button(self.canvas2,text="Back",command = self.transit41,width = 10,bg = "#724006",fg="white")
        self.id2 = self.canvas2.create_text(400,50,text = "TSEC Library",fill = "white",font = ("Bahnschrift",35,"bold underline"))
        self.id2 = self.canvas2.create_text(150,180,text = "Registration form",fill = "red",font = ("Bahnschrift",12,"bold underline"),anchor="sw")
        self.id3 = self.canvas2.create_text(150,220,text = "User ID:",fill = "white",font = ("Bahnschrift",12,"bold"),anchor="sw")
        self.id4 = self.canvas2.create_text(150,260,text = "Password:",fill = "white",font = ("Bahnschrift",12,"bold"),anchor="sw")
        self.id7 = self.canvas2.create_text(150,300,text = "Confirm Password:",fill = "white",font = ("Bahnschrift",12,"bold"),anchor="sw")
        self.id5 = Entry(self.canvas2)
        self.id6 = Entry(self.canvas2,show= "*")
        self.id8 = Entry(self.canvas2,show="*")
        self.e1 = self.canvas2.create_window(360, 210,window=self.id5)
        self.e2 = self.canvas2.create_window(360, 250,window=self.id6)
        self.e2 = self.canvas2.create_window(360, 290,window=self.id8)
        self.b2.place(x=300,y=320)
        self.b3.place(x=100,y=380)


    def uploadgui(self,sec):
        try:
            self.sel.destroy()
            self.frame2.destroy()
        except:
            pass
        self.canvas2 = Canvas(win,width = 800, height = 500)
        self.canvas2.pack()
        self.sub = sec
        self.background_image = PhotoImage(file = "lib.gif")
        self.bg1 = self.canvas2.create_image(0, 0, image = self.background_image, anchor=NW)
        self.id2 = self.canvas2.create_text(400,50,text = "TSEC Library",fill = "white",font = ("Bahnschrift",35,"bold underline"))
        self.id2 = self.canvas2.create_text(250,180,text = "Upload Details",fill = "white",font = ("Bahnschrift",20,"bold underline"),anchor="sw")
        self.id3 = self.canvas2.create_text(150,220,text = "Book Name",fill = "white",font = ("Bahnschrift",12,"bold"),anchor="sw")
        self.id4 = self.canvas2.create_text(150,260,text = "Author",fill = "white",font = ("Bahnschrift",12,"bold"),anchor="sw")
        self.id7 = self.canvas2.create_text(150,300,text = "Publications",fill = "white",font = ("Bahnschrift",12,"bold"),anchor="sw")
        self.id5 = Entry(self.canvas2)
        self.id6 = Entry(self.canvas2)
        self.id8 = Entry(self.canvas2)
        self.e1 = self.canvas2.create_window(360, 210,window=self.id5)
        self.e2 = self.canvas2.create_window(360, 250,window=self.id6)
        self.e2 = self.canvas2.create_window(360, 290,window=self.id8)
        self.b2 = Button(self.canvas2,text= "Upload",width = 10,bg = "#724006",fg="white",command = self.upload)
        self.b3 = Button(self.canvas2,text= "choose a file",command = self.choosefile)
        self.b4 = Button(self.canvas2,text="Back",command = self.transit43,width = 10,bg = "#724006",fg="white")
        self.b4 .place(x=600,y = 450)
        self.b2.place(x=300,y=370)
        self.b3.place(x=300,y=320)

    def rootframe(self):
        self.canvas1 = Canvas(win,width = 800, height = 500)
        self.canvas1.pack()
        self.background_image = PhotoImage(file = "lib.gif")
        self.bg1 = self.canvas1.create_image(0, 0, image=self.background_image, anchor=NW)
        
        self.b1 = Button(self.canvas1,text="Exit",command = self.b1f,width = 10,fg = "white",bg = "#724006")
        self.b2 = Button(self.canvas1,text="Login",command = self.login,width = 10,fg = "white",bg = "#724006")
        self.b3 = Button(self.canvas1,text="Become a member",command = self.transit14,bg = "#724006",fg="white")
            
        self.id2 = self.canvas1.create_text(400,50,text = "Online Library",fill = "white",font = ("Bahnschrift",35,"bold underline"))
        self.id2 = self.canvas1.create_text(150,180,text = "Select User:",fill = "white",font = ("Bahnschrift",12,"bold"),anchor="sw")
        self.id3 = self.canvas1.create_text(150,220,text = "User ID:",fill = "white",font = ("Bahnschrift",12,"bold"),anchor="sw")
        self.id4 = self.canvas1.create_text(150,260,text = "Password:",fill = "white",font = ("Bahnschrift",12,"bold"),anchor="sw")
        self.id7 = self.canvas1.create_text(550,400,text = "New user?",fill = "white",font = ("Bahnschrift",12,"bold"),anchor="sw")
        self.id5 = Entry(self.canvas1)
        self.id6 = Entry(self.canvas1,show= "*")
        self.e1 = self.canvas1.create_window(310, 210,window=self.id5)
        self.e2 = self.canvas1.create_window(310, 250,window=self.id6)
        choices = ['Select', 'Admin', 'Member']
        self.variable = StringVar(self.canvas1)
        self.variable.set('Select')
        self.w = OptionMenu(self.canvas1, self.variable, *choices)
        self.w.config(bg = "#724006",fg="white",activebackground="#724006",activeforeground = "white")
        win.bind('<Return>', self._login)
        self.w.place(x=250,y=160)
        self.b2.place(x=250,y=300)
        self.b3.place(x=650,y=380)
        self.b1.place(x=100,y=450)

    def userframe(self):
        fonts = 'Helvetica 19 bold'
        self.frame1 =Frame(win)
        self.frame1.pack()
        self.background_image = PhotoImage(file = "lib.gif")
        self.fpL1 = Label(self.frame1, image=self.background_image)
        self.fpL1.pack()
        self.l1 = Label(text = "Select Section",bg = "#724006",fg = "white",font = ("Bahnschrift 35 bold italic"))
        self.b1 = Button(self.frame1,text = "Maths",width = 10,font = fonts,fg = "white",bg = "#724006",command = lambda i ="Maths": self.view(i))
        self.b2 = Button(self.frame1,text = "Science",width = 10,fg = "white",font = fonts,bg = "#724006",command = lambda i ="Science": self.view(i))
        self.b3 = Button(self.frame1,text = "Geography",width = 10,fg = "white",font = fonts,bg = "#724006",command = lambda i ="Geography": self.view(i))
        self.b4 = Button(self.frame1,text = "Hindi",width = 10,fg = "white",font = fonts,bg = "#724006",command = lambda i ="Hindi": self.view(i))
        self.fb1 = Button(self.frame1,text = "Log out",width = 10,fg = "white",bg = "#724006",command = self.transit21)
        self.l1.place(x = 300,y = 50)
        self.b1.place(x = 100, y = 150)
        self.b2.place(x = 500, y = 150)
        self.b3.place(x = 100, y = 300)
        self.b4.place(x = 500, y = 300)
        self.fb1.place(x = 700, y = 450)

    def adminframe(self):
        self.userid = self.curuser
        self.frame2 =Frame(win)
        self.frame2.pack()
        self.background_image = PhotoImage(file = "lib.gif")
        self.fpL1 = Label(self.frame2, image=self.background_image)
        self.fpL1.pack()
        fonts = 'Helvetica 19 bold'
        self.fb2 = Button(self.frame2,text = "Add admin",font = fonts,width = 10,fg = "white",bg = "#724006",command = self.transit34)
        self.fb3 = Button(self.frame2,text = "Upload",font = fonts,width = 10,fg = "white",bg = "#724006",command = self.selectsect)
        self.fb1 = Button(self.frame2,text = "Log out",command = self.transit31,width = 10,bg = "#724006",fg="white")
        self.fb4 = Button(self.frame2,text = "view activity",font = fonts,width = 10,fg ="white",bg = "#724006",command = self.viewadminactivity)
        self.fb5 = Button(self.frame2,text = "View Books",font = fonts,width = 10,fg ="white",bg = "#724006",command = self.viewselectsect)
        self.fb2.place(x = 100, y = 150)
        self.fb3.place(x = 500, y = 150)
        self.fb4.place(x = 100, y = 300)
        self.fb5.place(x = 500, y = 300)
        self.fb1.place(x = 700, y = 450)

    def selectsect(self):
        self.sel = Tk()
        self.sel.title("Select Section")
        self.sel.wm_attributes("-topmost", 1)
        self.b1 = Button(self.sel,text = "Maths",width = 10,fg = "white",bg = "#724006",command = lambda i = "Maths": self.uploadgui(i))
        self.b2 = Button(self.sel,text = "Science",width = 10,fg = "white",bg = "#724006",command = lambda i = "Science": self.uploadgui(i))
        self.b3 = Button(self.sel,text = "Geography",width = 10,fg = "white",bg = "#724006",command = lambda i = "Geography": self.uploadgui(i))
        self.b4 = Button(self.sel,text = "Hindi",width = 10,fg = "white",bg = "#724006",command = lambda i = "Hindi": self.uploadgui(i))
        self.b1.pack(ipadx= 100)
        self.b2.pack(ipadx= 100)
        self.b3.pack(ipadx= 100)
        self.b4.pack(ipadx= 100)

    def viewselectsect(self):
        self.sel = Tk()
        self.sel.title("Select Section")
        fonts = 'Helvetica 11 bold'
        self.b1 = Button(self.sel,text = "Maths",width = 10,font = fonts,fg = "white",bg = "#724006",command = lambda i ="Maths": self.view(i))
        self.b2 = Button(self.sel,text = "Science",width = 10,fg = "white",font = fonts,bg = "#724006",command = lambda i ="Science": self.view(i))
        self.b3 = Button(self.sel,text = "Geography",width = 10,fg = "white",font = fonts,bg = "#724006",command = lambda i ="Geography": self.view(i))
        self.b4 = Button(self.sel,text = "Hindi",width = 10,fg = "white",font = fonts,bg = "#724006",command = lambda i ="Hindi": self.view(i))
        self.b1.pack(ipadx= 100)
        self.b2.pack(ipadx= 100)
        self.b3.pack(ipadx= 100)
        self.b4.pack(ipadx= 100)

    def adminactivityframe(self,headingtuple,a):
        try:
            self.temp.destroy()
        except:
            pass
        self.temp = Tk()
        self.temp.title("view activity")
        self.can =Canvas(self.temp)
        self.temp.wm_attributes('-topmost',1)
        self.adactframe1 = Frame(self.temp,borderwidth =1,relief = "solid")
        self.adactframe1.pack()
        self.adactframe = Frame(self.temp,borderwidth =1,relief = "solid")
        self.adactframe.pack()
        fonts = 'Helvetica 9 bold'
        for i in range(len(headingtuple)):
            Label(self.adactframe1, text=headingtuple[i],borderwidth = 2,fg = "white",bg = "#724006",width = 50,relief = "solid",font= fonts).grid(row=0,column=i)
        for i in range(len(a)):
            for j in range(len(a[0])):
                b = Label(self.adactframe, text=a[i][j],borderwidth = 2,fg = "white",bg = "#b57c3b",width = 50,relief = "solid")
                b.grid(row=i+1, column=j)
        self.adact2 = Frame(self.temp)
        self.adact2.pack()
        b = Button(self.adact2, text="close",fg = "white",bg = "#724006",width = 30,command = self.adactclose)
        b.pack()

    def viewframe(self,data):
        try:
            self.temp.destroy()
        except:
            pass
        self.heading = ("bookname","author","publication","")
        self.temp = Tk()
        self.temp.wm_attributes('-topmost',1)
        self.adactframe1 = Frame(self.temp)
        self.adactframe1.pack()
        self.adactframe = Frame(self.temp,borderwidth =1,relief = "solid")
        self.adactframe.pack()
        fonts = 'Helvetica 9 bold'
        self.allbutton = list()
        self.searchentry = Entry(self.adactframe1)
        self.searchentry.grid(row = 0,column = 0)
        self.searchb = Button(self.adactframe1,text = "Search",command = self.search)
        self.searchb.grid(row = 0,column = 1)


        for i in range(len(self.heading)):
            Label(self.adactframe, text=self.heading[i],borderwidth = 2,fg = "white",bg = "#724006",width = 50,relief = "solid",font= fonts).grid(row=0,column=i)
        for i in range(len(data)):
            for j in range(1,4):
                self.lb = Label(self.adactframe, text = data[i][j],borderwidth = 2,fg = "white",bg = "#b57c3b",width = 50,relief = "solid")
                self.lb.grid(row=i+1, column=j-1)
                if j == 1:
                    book = self.lb
            self.vb = Button(self.adactframe,text = "download",width = 50,command = lambda i=i: self.openfile(i))
            self.vb.grid(row=i+1, column=j)
            self.allbutton.append([book,self.vb])
        self.adact2 = Frame(self.temp)
        self.adact2.pack()
        b = Button(self.adact2, text="close",fg = "white",bg = "#724006",width = 30,command = self.adactclose)
        b.pack()




class SqlHelper:
    def __init__(self):
        self.createfolder()
        self.db = self.__connect()
        self.cursor = self.db.cursor()
        
        self.cursor.execute("create table if not exists userdetails (userId varchar(10) primary key,password varchar(20))")
        self.cursor.execute("create table if not exists admindetails (userId varchar(10) primary key,password varchar(20))")
        self.cursor.execute("create table if not exists existingfiles (sub varchar(10),bookname varchar(100),authname varchar(40),publication varchar(50),time datetime,pdfname varchar(1000))")
        self.cursor.execute("create table if not exists adminactivity (time datetime,admin varchar(10),uploaded varchar(100),subject varchar(20),primary key (time,admin))")
        self.db.commit()
    def __connect(self):
        db = pymysql.connect("localhost","Username","Password","online_library")
        return db
    def retuserdetails(self,userid):
        self.cursor.execute("select userid,password from userdetails where userid = '%s';" %(userid))
        self.usercr = self.cursor.fetchone()
        return self.usercr

    def search(self,key,sub):
        keyword = "%"+key+"%"
        self.cursor.execute("select * from existingfiles where sub = '%s' and (bookname like '%s' or authname like '%s' or publication like '%s');" %(sub,keyword,keyword,keyword))
        return self.cursor.fetchall()
    def retadmindetails(self,userid):
        self.cursor.execute("select userid,password from admindetails where userid = '%s';" %(userid))
        self.admincr = self.cursor.fetchone()
        return self.admincr
    def adduser(self,userid,passw):
        self.cursor.execute("insert into userdetails values(\"%s\",\"%s\")" %(userid,passw))
        self.db.commit()

    def addadmin(self,userid,passw):
        self.cursor.execute("insert into admindetails values(\"%s\",\"%s\")" %(userid,passw))
        self.db.commit()

    def close(self):
        self.db.close()

    def adminuploadrec(self,userid,sub,filename):
        self.cursor.execute("insert into adminactivity values(now(),\"%s\",\"%s\",\"%s\")" %(userid,filename,sub))
        self.db.commit()
    def viewadminactivity(self,sortby = "time"):
        self.cursor.execute("select * from adminactivity order by %s" %(sortby))
        return self.cursor.fetchall()
    def createfolder(self):
        self.rootdir = "D:/OnlineLibrary/"
        self.mathdir = "D:/OnlineLibrary/Maths"
        self.scidir = "D:/OnlineLibrary/Science"
        self.geodir = "D:/OnlineLibrary/Geography"
        self.hindir = "D:/OnlineLibrary/Hindi"
        if not os.path.exists(self.rootdir):
            os.makedirs(self.rootdir)
        if not os.path.exists(self.mathdir):
            os.makedirs(self.mathdir)
        if not os.path.exists(self.scidir):
            os.makedirs(self.scidir)
        if not os.path.exists(self.geodir):
            os.makedirs(self.geodir)
        if not os.path.exists(self.hindir):
            os.makedirs(self.hindir)

    def copyit(self,source,dest):
        file = os.path.join(source)
        shutil.copy(file,dest)

    def getfiles(self,sub):
        self.cursor.execute("select * from existingfiles where sub = \"%s\" order by pdfname" %(sub))
        a = self.cursor.fetchall()
        print(a)
        return a

    def insexistings(self,btuple,name):
        self.cursor.execute("insert into existingfiles values('%s','%s','%s','%s',now(),'%s')" %(btuple[0],btuple[1],btuple[2],btuple[3],btuple[4],))
        self.db.commit()

win = Tk()
win.title("Online Library")
win.resizable(0,0)
sqlhelper = SqlHelper()
m = Mainwin(sqlhelper)
while m.des == 0:
    m.textani()
    win.update()
    time.sleep(0.01)
