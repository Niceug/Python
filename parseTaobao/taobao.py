#coding:utf8
#爬取taobao商品
import urllib.request
import urllib.parse
import pymysql

import re
#打开网页，获取网页内容
def url_open(url):
    headers=("user-agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
    opener=urllib.request.build_opener()
    opener.addheaders=[headers]
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(url).read().decode("utf-8","ignore")
    return data

#将数据存入mysql中
def data_Import(sql):
   conn=pymysql.connect(host='127.0.0.1',user='root',password='123456',db='python',charset='utf8')
   conn.query(sql)
   conn.commit()
   conn.close()

#!/usr/bin/python
# -*- coding: UTF-8 -*-



if __name__=='__main__':
    try:
        #定义要查询的商品关键词
        keyword="鞋子"
        #将爬取的关键字编码成utf-8，因为地址栏默认编码成utf-8
        keywordCoded=urllib.parse.quote(keyword)
        #定义要爬取的页数
        num=10
        for i in range(num):
            url="https://s.taobao.com/search?q="+keywordCoded+"&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&filter=reserve_price%5B47.01%2C145.00%5D&sort=default&s="+str(i*45)

            #获取网页源代码
            data=url_open(url)

            #定义各个字段正则匹配规则
            img_pat='"pic_url":"(//.*?)"'
            name_pat='"raw_title":"(.*?)"'
            nick_pat='"nick":"(.*?)"'
            price_pat='"view_price":"(.*?)"'
            fee_pat='"view_fee":"(.*?)"'
            sales_pat='"view_sales":"(.*?)"'
            comment_pat='"comment_count":"(.*?)"'
            city_pat='"item_loc":"(.*?)"'

            #查找满足匹配规则的内容，并存在列表中,re是Regular Expression 的缩写，是分析正则表达式的一个工具
            imgL=re.compile(img_pat).findall(data)
            nameL=re.compile(name_pat).findall(data)
            nickL=re.compile(nick_pat).findall(data)
            priceL=re.compile(price_pat).findall(data)
            feeL=re.compile(fee_pat).findall(data)
            commentL=re.compile(comment_pat).findall(data)
            cityL=re.compile(city_pat).findall(data)

            #len（imgL）求出的是每页面里面商品的个数。
            for j in range(len(imgL)):
                # 商品图片链接
                img="http:"+imgL[j]
                # 商品名称
                name=nameL[j]
                # 淘宝店铺名称
                nick=nickL[j]
                # 价格
                price=priceL[j]
                # 运费
                fee=feeL[j]
                # 评论数，可能为空
                comment=commentL[j]
                #处理评论为空的情况
                if(comment==""):
                    comment=0
                # 店铺所在城市
                city=cityL[j]
                print('正在爬取第'+str(i)+"页，第"+str(j)+"个商品信息...")
                print('名称:'+name+'图片链接:'+img+'店铺名称:'+nick+'价格:'+price+'运费:'+fee)
                sql="insert into taobao(name,price,fee,comment,city,nick,img) values('%s','%f','%s','%d','%s','%s','%s')" %(name,float(price),fee,int(comment),city,nick,img)
                data_Import(sql)
                print("爬取完成，且数据已存入数据库")
    except Exception as e:
        print(str(e))
    print("任务完成")