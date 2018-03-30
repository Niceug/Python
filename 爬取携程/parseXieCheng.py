#coding:utf8
import urllib.request
import urllib.parse

#import pymysql
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
#def data_Import(sql):
   # conn=pymysql.connect(host='127.0.0.1',user='dengjp',password='123456',db='python',charset='utf8')
   # conn.query(sql)
   # conn.commit()
   # conn.close()

if __name__=='__main__':
    try:
        #关键词
        keyword="鞋子"
        # 关键字编码成所需编码
        keywordCoded=urllib.parse.quote(keyword)

        #爬取10页
        pageNum=10
        for i in range(pageNum):
            print(i)
            url="https://s.taobao.com/search?q="+keywordCoded+"&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&&sort=price-asc&sort=renqi-desc&s="+str(i*45)
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
            #查找满足匹配规则的内容，并存在列表中
            print("re=" + str(re))
            imgL=re.compile(img_pat).findall(data)
            nameL=re.compile(name_pat).findall(data)
            nickL=re.compile(nick_pat).findall(data)
            priceL=re.compile(price_pat).findall(data)
            feeL=re.compile(fee_pat).findall(data)
           # salesL=re.compile(sales_pat).findall(data)
            commentL=re.compile(comment_pat).findall(data)
            cityL=re.compile(city_pat).findall(data)
            print('1fdfdf')
            for j in range(len(imgL)):
                print('j'+str(j))
                print('长度为：'+str(len(imgL)))

                img="http:"+imgL[j]#商品图片链接

                name=nameL[j]#商品名称
                nick=nickL[j]#淘宝店铺名称
                price=priceL[j]#商品价格
                fee=feeL[j]#运费
                #sales=salesL[j]#商品付款人数
                comment=commentL[j]#商品评论数，会存在为空值的情况

                if(comment==""):
                    comment=0
                city=cityL[j]#店铺所在城市
                print('正在爬取第'+str(i)+"页，第"+str(j)+"个商品信息...")
                print('名称:'+name+'图片链接:'+img+'店铺名称:'+nick+'价格:'+price+'运费:'+fee)
                #sql="insert into taobao(name,price,fee,sales,comment,city,nick,img) values('%s','%s','%s','%s','%s','%s','%s','%s')" %(name,price,fee,sales,comment,city,nick,img)
                #data_Import(sql)
                print("爬取完成，且数据已存入数据库")
        print(sum)
    except Exception as e:
        print(str(e))
    print("任务完成")