# getBuffDatas
_爬取网易Buff.com的数据并实时交易_

# 此项目是一个实验性质的项目，不打算继续更新，因此已存档。代码和接口仅供参考！

## 简介
本程序用于爬取buff.com上的数据，用户可以设置想要监测的枪械的磨损度和价格区间来实时监测。如果监测到符合要求的装备就会自动购买。

程序实现的功能如下：
>1. 自动登录，这是通过selenium模拟点击浏览器获得到cookie实现的，cookie被保存在cookies_string.txt文档中
>2. 批量爬取，写入data.txt的文件得以实现批量工作，写入格式为: 类别,枪械全称,最低价格,最高价格,最低磨损,最高磨损 例如:二西莫夫,AK-47 | 二西莫夫 (崭新出厂),100,200,0.1,0.12 *注意：需要用逗号分隔每一项，且类别名不能写错*
>3. GUI页面，使用tkinter写了GUI，方便使用。
>4. ~~异步处理~~
>5. ~~ip隧穿实现高速爬取~~


## 使用方法

1. 将文件clone到本地`git clone`
2. cd到解压的文件夹 `pip install -r requirements.txt`
3. `python -m GUI.py`

## 注意事项
1. 打开GUI页面之前检查程序同目录下有没有“data.txt”,"cookies_string.txt"文件，如果没有可以自己建一个(GUI页面插入也会自动建)，如果没有这两个文件会报错。
2. 使用自动获取cookie的功能时确保文件不处于中文路径上 (opencv在中文路径上会报错)
