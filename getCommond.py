import getCookie
import io
import urllib.request
import random
from getCookie import getCookie,getCookieStr
import requests
import time
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
from datetime import datetime
TIME = lambda:int(time.time() * 1000)
nowtime = TIME()

def getcookie(phonenumber=None,pwd=None):
    if  phonenumber == None or pwd==None:
        s = ''
        with open(os.path.split(os.path.realpath(__file__))[0]+r"/cookies_string.txt", 'r') as f:
            s = f.read()
        cookie = s
        return cookie
    else:
        getCookieStr(phonenumber, pwd)

buffer = io.StringIO()  #通过写入缓冲区使得GUI页面显示数据
buffer.flush()
class Calculator:
    
    def __init__(self, cookie,catename,rifle_name,minprice,maxprice,minmosun,maxmosun,phonenumber=None,pwd=None,):
        self.cookie = cookie
        self.minprice = minprice
        self.maxprice = maxprice
        self.minmosun = minmosun
        self.maxmosun = maxmosun
        self.catename = catename
        self.rifle_name = rifle_name
        self.gooditme = []
        self.cateitem = []
        self.phonenumber = phonenumber
        self.pwd = pwd
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                'Cookie':self.cookie,
            
        }
        
    def getAllCateIds(self):
        # try:

        url =  'https://buff.163.com/api/market/goods?game=csgo&page_num=1&search={}&use_suggestion=0&trigger=undefined_trigger&_={}'.format(self.catename, nowtime)
        res = requests.get(url,headers=self.headers)
        json_datas = res.json()
        # print(json_datas)
        total_page = json_datas['data']['total_page']
        if total_page >3:
            total_page = 3
        item_list = []
        counter = 0
        try:
            for i in range(1,total_page+1):
                counter = i
                url =  'https://buff.163.com/api/market/goods?game=csgo&page_num={}&search={}&use_suggestion=0&trigger=undefined_trigger&_={}'.format(i,self.catename, nowtime)
                res = requests.get(url,headers=self.headers)
                json_datas = res.json()
                item_count = json_datas['data']['page_size']
                for j in range(0,item_count):
                    item_list.append(json_datas['data']['items'][j])
                time.sleep(0.5)
            print('------------------------------请稍等--------------------------------',file=buffer,flush=True)
            print('------------------------------请稍等--------------------------------')
        except IndexError:
            print("未查到'{}'类别的道具，请检查名称是否正确".format(self.catename),file=buffer,flush=True)
            print("未查到'{}'类别的道具，请检查名称是否正确".format(self.catename))
        except Exception as e:
            print(str(e),file=buffer,flush=True)
            print(str(e))
        finally:
            # if(counter!=(total_page)):
            #     print('获取失败')
            # else:
            #     print('--------成功获取到有关{}的商品--------'.format(self.catename))
            return item_list  
        # except Exception as e:
        #     print(str(e)+"\n"+"爬得太快了",file=buffer,flush=True)
        #     print(str(e)+"\n"+"爬得太快了")
    
    def getGoodsItems(self):
        item_list = self.getAllCateIds()
        for x in range(len(item_list)):
            if self.rifle_name == item_list[x]['name']:
                self.cateitem.append(item_list[x]['id'])
        goodsItems = self.cateitem
        print(goodsItems)
        return goodsItems    
    
    def getSpecificGoods(self):
        if(len(self.cateitem)==0):
            self.getGoodsItems()
        goodsItems = self.cateitem
        goodItem2 = []
        try:
            page = 1
            id = goodsItems[0]
            url = 'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={}&page_num={}&sort_by=default&mode=&allow_tradable_cooldown=1&_={}'.format(id,page,nowtime)
            total_page = requests.get(url,headers = self.headers).json()['data']['total_page']
            total_count = requests.get(url,headers = self.headers).json()['data']['total_count']
            flag = True
            for i in range(0,total_page):
                url2 = 'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={}&page_num={}&sort_by=default&mode=&allow_tradable_cooldown=1&_={}'.format(id,i+1,nowtime)
                time.sleep(0.5)
                response = requests.get(url2,headers=self.headers)
                jsondata = response.json()
                # print(url2)
                if jsondata['code']=='OK':
                    for i in range(0,len(jsondata['data']['items'])):
                        mosun = jsondata['data']['items'][i]['asset_info']['paintwear']
                        price = jsondata['data']['items'][i]['price']
                        user = jsondata['data']['items'][i]['user_id']
                        ids = jsondata['data']['items'][i]['id']
                        self.gooditme.append([mosun,price,user,ids])
            time.sleep(2)
        except IndexError:
            print('请检查类别名称是否输入正确',file=buffer,flush=True)
            print('请检查类别名称是否输入正确')
        except Exception as e:
            print(str(e),file=buffer,flush=True)
            print(str(e))
        finally:
            self.writeGoods(self.gooditme)
            if(len(self.gooditme)!=total_count):
                return 0
            else:
                return 1
    def getGoodsItemsDatas(self):
        if(len(self.gooditme)==0):
            self.getSpecificGoods()
        print(self.gooditme,file=buffer,flush=True)
        print(self.gooditme)

    def getMinMosunRifle(self):
        if(len(self.gooditme)==0):
            self.getSpecificGoods()
        new_list = sorted(self.gooditme,key=lambda x:x[0])
        return new_list[0]
    
    def getMinPriceRifile(self):
        if(len(self.gooditme)==0):
            self.getSpecificGoods()        
        new_list = sorted(self.gooditme,key=lambda x:x[1])
        return new_list[0]
    
    def getSettedArgumentRifile(self): #0:使用cache 1:不使用cache
        self.getGoodsItems()
        goodsItems = self.cateitem
        goodItem2 = []
        try:
            page = 1
            id = goodsItems[0]
            url = 'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={}&page_num={}&sort_by=default&mode=&allow_tradable_cooldown=1&_={}'.format(id,page,nowtime)
            total_page = requests.get(url,headers = self.headers).json()['data']['total_page']
            if total_page>3:
                total_page = 3
            total_count = requests.get(url,headers = self.headers).json()['data']['total_count']
            for i in range(0,total_page):
                url2 = 'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={}&page_num={}&sort_by=default&mode=&allow_tradable_cooldown=1&_={}'.format(id,i+1,nowtime)
                response = requests.get(url2,headers=self.headers)
                jsondata = response.json()
                # print(url2)
                if jsondata['code']=='OK':
                    for i in range(0,len(jsondata['data']['items'])):
                        mosun = jsondata['data']['items'][i]['asset_info']['paintwear']
                        price = jsondata['data']['items'][i]['price']
                        user = jsondata['data']['items'][i]['user_id']
                        ids = jsondata['data']['items'][i]['id']
                        self.gooditme.append([mosun,price,user,ids])
                        print("枪械名称: {},磨损度: {},价格: {}".format(self.rifle_name,mosun,price),file=buffer,flush=True)
                        print("枪械名称: {},磨损度: {},价格: {}".format(self.rifle_name,mosun,price))
                        time.sleep(1)
                        if(self.filter(mosun=mosun, price=price, minprice=self.minprice, maxprice=self.maxprice, minmosun=self.minmosun, maxmosun=self.maxmosun)):
                            print("查找成功！！！！！！",file=buffer,flush=True)
                            print("查找成功！！！！！！")
                            buycode = self.buyItem(goods_id=id, sell_order_id=ids, price=price, cookie=self.cookie)
                            if(buycode==1):
                                print("购买成功",file=buffer,flush=True)
                                print("购买成功")
                                return 1
                            else:
                                print("购买失败",file=buffer,flush=True)
                                print("购买失败")
                                return 0
                        
                        else:
                            pass
                else:
                    print(jsondata['code'],file=buffer)
        except Exception as e:
            print(goodsItems)
            print("error429 [{}] 爬取速度太快了".format(self.rifle_name),file=buffer,flush=True)
            print("error429 [{}] 爬取速度太快了"+str(e).format(self.rifle_name))
            print("等待10秒钟........",file=buffer,flush=True)
            print("等待10秒钟........")
            time.sleep(10) 
        
    
    def filter(self,mosun,price,minprice,maxprice,minmosun,maxmosun):
        if(float(mosun)>=minmosun and float(mosun)<=maxmosun and float(price)>=minprice and float(price)<=maxprice):
            return True
        else:
            return False
        
    
    def getCacheDataOfGoods(self):
        
        a = self.readGoods()
        if(len(a)==0):
            self.getSpecificGoods()
            a = self.readGoods()
        return a
    
    def writeGoods(self,L):
        with open(self.rifle_name+'_'+'.txt' ,'w') as f:
            for x in L:
                f.write(x[0])
                f.write(',')
                f.write(x[1])
                f.write(',')
                f.write(x[2])
                f.write(',')
                f.write(x[3])
                f.write('\n')      
    
    def readGoods(self):
        a = []
        for line in open(self.rifle_name+'_'+'.txt'):
            a.append(line.split(','))
        c = []   
        for x in range(len(a)):
            c.append([x.strip() for x in a[x]])  
            
        return c 
    
            
    def updateCookie(self):
        if(phonenumber == None or pwd==None):
            self.phonenumber = input("输入电话号码")
            self.pwd = input("输入密码")
        getCookieStr(self.phonenumber,self.pwd)
        
        
    def buyItem(self,goods_id,sell_order_id,price,cookie):
        headers1 = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                'Cookie':self.cookie,
                
            
        }
 

        r2 = requests.session()
        r2.get('https://buff.163.com/api/market/goods/buy/preview?game=csgo&sell_order_id={}&goods_id={}&price={}&allow_tradable_cooldown=0&cdkey_id=&_={}'.format(sell_order_id,goods_id,price,nowtime),headers=headers1)
        a = r2.cookies.get_dict()
        data= {"game": "csgo", "goods_id": goods_id, "sell_order_id": sell_order_id, "price": price, "pay_method": 3, "allow_tradable_cooldown": 0, "token": "", "cdkey_id": ""}
        url = 'https://buff.163.com/api/market/goods/buy'
        headers = {
            'Content-Type': 'application/json',
            'oringin':'https://buff.163.com',
            'x-requested-with':'XMLHttpRequest',   
            'Accept':'application/json, text/javascript, */*; q=0.01',
            # 'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer':'https://buff.163.com/goods/{}'.format(goods_id),
            'cookie': cookie,
            'x-csrftoken':a['csrf_token'],
            }
        request = urllib.request.Request(url=url,headers=headers,data = json.dumps(data).encode())
        response = urllib.request.urlopen(request)
        jsondata = json.loads(response.read())
        state = jsondata['code']
        # print(jsondata)
        if(state == 'OK'):
            print("购买成功！请到手机app上发起报价",file=buffer,flush=True)
            print("购买成功！请到手机app上发起报价")
            return 1
        else:
            print(jsondata['error'],file=buffer,flush=True)
            print(jsondata['error'])
            return 0
    def buy_until_complete(self):
        flag = True
        while flag:
            a = self.getSettedArgumentRifile()
            if(a==1 or a==0):
                flag = False
                return a

def getbuffer():
    return buffer           
