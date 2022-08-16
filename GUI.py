import tkinter as tk
from tkinter import *
import tkinter.simpledialog
from tkinter import Menu
import threading
import time
import getCookie
import getCommond
import test3
import io
import os
import sys
event = threading.Event()
class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('buff自动买货小程序')
        self.root.geometry("500x700+1100+150")
        self.interface()
        self.refresh_data()

    def interface(self):
        """"界面编写位置"""
        self.Entry0 = tk.Entry(self.root)
        self.Entry0.place(x = 120,y = 50,width=300,height=50)
        self.Label0 = tk.Label(self.root,text="输入Cookie值：")
        self.Label0.place(x =10 ,y = 50,width=100,height=20)
        self.Entry1 = tk.Entry(self.root)
        self.Entry1.place(x = 120,y = 100,height=40,width=300)
        self.Label1 = tk.Label(self.root,text="输入种类名称：")
        self.Label1.place(x =10 ,y = 100,height=20,width=100)
        self.Entry2 = tk.Entry(self.root)
        self.Entry2.place(x = 120,y = 150,height=40,width=300)
        self.Label2 = tk.Label(self.root,text="输入枪械全称：")
        self.Label2.place(x =10 ,y = 150,height=20,width=100)
        self.Entry3 = tk.Entry(self.root)
        self.Entry3.place(x = 120,y = 200,height=30,width=80)
        self.Label3 = tk.Label(self.root,text="输入最小磨损：")
        self.Label3.place(x =10 ,y = 200,height=20,width=100)
        self.Entry4 = tk.Entry(self.root)
        self.Entry4.place(x = 330,y = 200,height=30,width=80)
        self.Label4 = tk.Label(self.root,text="输入最大磨损：")
        self.Label4.place(x =230 ,y = 200,height=20,width=100)
        self.Entry5 = tk.Entry(self.root)
        self.Entry5.place(x = 120,y = 250,height=30,width=80)
        self.Label5 = tk.Label(self.root,text="输入最小价格：")
        self.Label5.place(x =10 ,y = 250,height=20,width=100)
        self.Entry6 = tk.Entry(self.root)
        self.Entry6.place(x = 330,y = 250,height=30,width=80)
        self.Label6 = tk.Label(self.root,text="输入最大价格：")
        self.Label6.place(x =230 ,y = 250,height=20,width=100)
        self.w1 = tk.Text(self.root,wrap=WORD)
        self.w1.place(x=0,y=300,width=500,height=200)
        self.Button0 = tk.Button(self.root,text="插入数据",command=self.getmsg)
        self.Button0.place(x=0,y=500,width=200,height=50)
        self.Button1 = tk.Button(self.root,text="开始爬虫",command=self.startMultiProcess)
        self.Button1.place(x=300,y=500,width=200,height=50)
        self.Button0 = tk.Button(self.root,text="手动更新Cookie",command=self.get_cookie)
        self.Button0.place(x=0,y=600,width=200,height=50)
        self.Button1 = tk.Button(self.root,text="自动获取Cookie",command=self.autoUpdate)
        self.Button1.place(x=300,y=600,width=200,height=50)
        self.Button2 = tk.Button(self.root,text="退出程序",command=self.exitProcess)
        self.Button2.place(x=200,y=550,width=100,height=50)



    def getmsg(self):
        catename = self.Entry1.get()
        riflie_name = self.Entry2.get()
        minmosun = self.Entry3.get()
        maxmosun = self.Entry4.get()
        minprice = self.Entry5.get()
        maxprice = self.Entry6.get()
        if(len(catename)==0 or len(riflie_name)==0 or len(minmosun)==0 or len(maxmosun)==0 or len(minprice)==0 or len(maxprice)==0):
            self.w1.insert("insert", "请检查参数是否为空\n")
        else:
            self.w1.delete(1.0,"end")
            str1 = catename+','+riflie_name+','+minprice+','+maxprice+','+minmosun+','+maxmosun+'\n'
            try:
                
                with open(os.path.split(os.path.realpath(__file__))[0]+r"/data.txt",'a+') as f:
                    content = f.read()
                    f.seek(0,2)
                    f.write(str1)
                self.w1.insert("insert", "插入成功！\n")
                fp = os.path.dirname(os.path.abspath(__file__))
                print(fp)
                
                
            except Exception as e:
                self.w1.insert("insert", str(e))
    def get_cookie(self):
        cookie = self.Entry0.get()
        if(len(cookie)==0):
            self.w1.delete(1.0,"end")
            self.w1.insert("insert","请输入cookie值！\n")
        else:
            self.w1.delete(1.0,"end")
            with open(os.path.split(os.path.realpath(__file__))[0]+r"/cookies_string.txt",'w') as f:
                f.write(cookie)
                self.w1.insert("insert","插入cookie成功！\n")
            
    def startMultiProcess(self):
        t = threading.Thread(target=test3.startMultiprocess)
        t.setDaemon(True)
        t.start()
    def exitProcess(self):
        sys.exit(0)
    def refresh_data(self):
        buff = getCommond.getbuffer().getvalue()  #从buffer缓冲区获得数据实时显示
        self.w1.delete(1.0,END)
        self.w1.insert(tk.INSERT, buff)
        self.w1.see(END)  #锁定光标总是在最后一行
        self.w1.update()
        self.root.after(2000,self.refresh_data)
        
    def autoUpdate(self):
        r1 = tkinter.simpledialog.askstring("获取信息", prompt="输入电话号码和密码，以逗号分隔")
        phonenumber = r1.split(",")[0]
        pwd = r1.split(",")[1]
        cookie = getCookie.getCookieStr(phonenumber, pwd)
        self.w1.insert(tk.INSERT, cookie)
if __name__ == '__main__':
    a = GUI()
    a.root.mainloop()
