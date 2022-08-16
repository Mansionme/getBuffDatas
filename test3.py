import threading
import time
from getCommond import Calculator,getcookie
import os
def startMultiprocess():
    a = []
    # path = os.path.split(os.path.realpath(__file__))[0]+r"data.txt"
    with open(os.path.split(os.path.realpath(__file__))[0]+r"/data.txt",'r',encoding='utf-8')as f:
        a.append(f.read())
    cookie =  getcookie()
    threads = []
    b = a[0].split('\n')
    for i in range(len(b)):
        c = b[i].split(',')
        if(len(c)>1):
            cal = Calculator(cookie=cookie,catename=c[0],rifle_name=c[1],minprice=float(c[2]),maxprice=float(c[3]),minmosun=float(c[4]),maxmosun=float(c[5]))
            t = threading.Thread(target=cal.buy_until_complete)
            threads.append(t)
        
    for t in threads:
        t.start()
        time.sleep(1)
        
    
