from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
import cv2
import random
import requests
import numpy as np
from PIL import Image
import json
from io import BytesIO
TIME = lambda:int(time.time() * 1000)
nowtime = TIME()

def move_to_gap(browser, tracks):
    slider = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'yidun_slider')))
    ActionChains(browser).click_and_hold(slider).perform()
    while tracks:
        x = tracks.pop(0)
        ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.05)
    time.sleep(0.05)
    ActionChains(browser).release().perform()
def download_img(url,name):
    
    r = requests.get(url)
    if r.status_code == 200:
        with open(os.path.split(os.path.realpath(__file__))[0]+r"/{}.png".format(name), 'wb') as f:
            f.write(r.content)    
                  
def change_size(file):
    image = cv2.imread(file, 1)  # 读取图片 image_name应该是变量
    img = cv2.medianBlur(image, 5)  # 中值滤波，去除黑色边际中可能含有的噪声干扰
    b = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)  # 调整裁剪效果
    binary_image = b[1]  # 二值图--具有三通道
    binary_image = cv2.cvtColor(binary_image, cv2.COLOR_BGR2GRAY)
    x, y = binary_image.shape
    edges_x = []
    edges_y = []
    for i in range(x):
        for j in range(y):
            if binary_image[i][j] == 255:
                edges_x.append(i)
                edges_y.append(j)
    left = min(edges_x)  # 左边界
    right = max(edges_x)  # 右边界
    width = right - left  # 宽度
    bottom = min(edges_y)  # 底部
    top = max(edges_y)  # 顶部
    height = top - bottom  # 高度
    pre1_picture = image[left:left + width, bottom:bottom + height]  # 图片截取
    return pre1_picture  # 返回图片数据

def match(target, template):
    img_gray = cv2.imread(target, 0)
    img_rgb = change_size(template)
    template = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    run = 1
    # 使用二分法查找阈值的精确值
    L = 0
    R = 1
    while run < 20:
        run += 1
        threshold = (R + L) / 2
        if threshold < 0:
            print('Error')
            return None
        loc = np.where(res >= threshold)
        if len(loc[1]) > 1:
            L += (R - L) / 2
        elif len(loc[1]) == 1:
            break
        elif len(loc[1]) < 1:
            R -= (R - L) / 2
    return loc[1][0]
def get_tracks(distance, seconds, ease_func):
    distance += 20
    tracks = [0]
    offsets = [0]
    for t in np.arange(0.0, seconds, 0.1):
        ease = ease_func
        offset = round(ease(t / seconds) * distance)
        tracks.append(offset - offsets[-1])
        offsets.append(offset)
    tracks.extend([-3, -2, -3, -2, -2, -2, -2, -1, -0, -1, -1, -1])
    return tracks
def ease_out_quart(x):
    return 1 - pow(1 - x, 4)   
def calculImg(target,xp):
    target_img = Image.open(target)
    size_loc = target_img.size
    return xp/int(size_loc[0])


def getCookie(phonenumber,pwd):
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
    chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])# 开启实验性功能
    # 去除特征值
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    browser = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
    with open(os.path.split(os.path.realpath(__file__))[0]+r"/stealth.min.js") as f:
        js = f.read()
    #execute_cdp_cmd用来执行chrome开发这个工具命令
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    browser.get("https://buff.163.com/account/login?back_url=/user-center/asset/recharge/%3F")
    time.sleep(2)
    # browser.get("https://bot.sannysoft.com/")
    browser.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[2]/div[1]/span/i").click()
    browser.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[2]/div[2]/span/i").click()

    frame = browser.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[1]/iframe")  #切换到账号密码登录，因为是frame,首先定位到frame
    time.sleep(0.5)
    browser.switch_to.frame(frame)
    browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/div/div[1]/a").click()
    browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/div/div[2]/div[1]/input").send_keys(phonenumber)
    browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/div/div[4]/div[2]/input[2]").send_keys(pwd)
    time.sleep(0.5)

    try:
        print("正在登录，请稍后......")
        cookie_str = ' '
        img = browser.find_element_by_xpath("//*[@id='ScapTcha']/div/div[1]/div/div[1]/img[1]").get_attribute("src")
        img2 = browser.find_element_by_xpath("//*[@id='ScapTcha']/div/div[1]/div/div[1]/img[2]").get_attribute("src")
        download_img(img,'1')
        download_img(img2,'2')
        target = os.path.split(os.path.realpath(__file__))[0]+r'/1.png'
        template = os.path.split(os.path.realpath(__file__))[0]+r'/2.png'
        xp = 300
        zoom = calculImg(target, xp)
        distance = match(target, template)
        track = get_tracks((distance+7)*zoom, random.randint(2, 4), ease_out_quart)
        move_to_gap(browser, track)
        time.sleep(1)
        # browser.save_screenshot('walkaround.png')
        browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/div/div[7]/a").click()
        time.sleep(1)
        browser.get('https://buff.163.com/?game=csgo')
        cookie_list = browser.get_cookies()
        with open(os.path.split(os.path.realpath(__file__))[0]+r"/cookies.txt",'w')as f:
            f.write(json.dumps(cookie_list))
        cookie = [item['name']+'='+item['value'] for item in cookie_list]
        cookie_str = ';'.join(item for item in cookie)
        with open(os.path.split(os.path.realpath(__file__))[0]+r"/cookies_string.txt",'w') as f:
            f.write(cookie_str)
        print("登录成功！")

        
    except Exception as e:
        print(str(e))
    finally:
        time.sleep(1)
        # srouce = browser.page_source
        # with open('results.html', 'w') as f:
        #     f.write(srouce)
        browser.close()
        return cookie_str

def getCookieStr(phonenumber,pwd):
    flag = 1
    while flag:
        a = getCookie(phonenumber,pwd)
        if len(a)>1:
            flag = 0
            return(a)
        else:
            print("验证码通过失败，正在重新加载")
            flag = 1
