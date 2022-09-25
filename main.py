import requests
import re
import datetime
import random
import time
import openpyxl

bv=str(input('请输入你想要爬取的视频的BV号:'))
n=int(input('请输入您想爬取的数据条数(每两条数据间隔大概7s,您可以在下方更改间隔时间):'))
#一级页面头
header={
    'Host':'api.bilibili.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Cookie':''
}

#页面url
url0='http://api.bilibili.com/x/web-interface/archive/stat?bvid='
url1a='https://api.bilibili.com/x/player/pagelist?bvid='
url1b='&jsonp=jsonp'
url2a='https://api.bilibili.com/x/player/online/total?aid='
url2b='&cid='
url2c='&bvid='

# 打开文件
wb=openpyxl.Workbook()
# 使用的工作对象创建一张表
sheet1=wb.active
# 在sheet1表中写入内容  插入内容
sheet1.append(['播放量','评论数','硬币数','分享数','点赞量','在线观看人数','数据记录时间'])

for i in range(n):
    if i>0:
        #延时
        time.sleep(5+random.randint(-5,5))
    res0=requests.get(url0+bv,headers=header).text
    #获取aid
    aid0=re.search(r'"aid":\d+,',str(res0)).group(0)
    aid=re.search(r'\d+',str(aid0)).group(0)
    res1=requests.get(url1a+bv+url1b,headers=header).text
    #获取cid
    cid0=re.search(r'"cid":\d+,',str(res1)).group(0)
    cid=re.search(r'\d+',str(cid0)).group(0)
    res2=requests.get(url2a+aid+url2b+cid+url2c+bv,headers=header).text
    #在线观看人数
    total=re.search(r'"total":"\d+',str(res2)).group(0)
    concurrent_viewers=re.search(r'\d+',str(total)).group(0)
    if int(concurrent_viewers)>=1000:#判断当前观看人数是否大于1000，需不需要加+号
        concurrent_viewers=concurrent_viewers+'+'
    #播放量
    l1=re.search(r'"view":\d+,',str(res0)).group(0)
    view=re.search(r'\d+',str(l1)).group(0)
    #评论数
    l2=re.search(r'"reply":\d+,',str(res0)).group(0)
    reply=re.search(r'\d+',str(l2)).group(0)
    #硬币数
    l3=re.search(r'"coin":\d+,',str(res0)).group(0)
    coin=re.search(r'\d+',str(l3)).group(0)
    #分享数
    l4=re.search(r'"share":\d+,',str(res0)).group(0)
    share=re.search(r'\d+',str(l4)).group(0)
    #点赞量
    l5=re.search(r'"like":\d+,',str(res0)).group(0)
    like=re.search(r'\d+',str(l5)).group(0)
    #时间
    tm=datetime.datetime.now()
    time1=tm.strftime("%Y-%m-%d %H:%M:%S")
    print('播放量:%d'%int(view),'评论数:%d'%int(reply),'硬币数:%d'%int(coin),'分享数:%d'%int(share),'点赞数:%d'%int(like),'当前观看人数:%s'%concurrent_viewers,'数据记录时间:%s'%time1,'剩余抓取次数:%d'%int(n-i-1))
    xx_info=[view,reply,coin,share,like,concurrent_viewers,time1]
    sheet1.append(xx_info)
    wb.save('数据抓取2.xlsx')#可以自定义名字
print('数据爬取完毕')
