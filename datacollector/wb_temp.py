import os
import random
from pandas.core.indexing import maybe_convert_ix
import requests
from datetime import datetime
from time import sleep

import json
from lxml import etree
import re
import pandas as pd
from random import randint
import warnings
warnings.filterwarnings('ignore')

from utils.readconfig import Config

class crawler():
    def __init__(self,userid,cookie=None):

        self.userid=str(userid)
        self.headers={'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                      'Cookie':cookie}
        self.query=''
        self.maxtry=5
        self.wb_list=[]

    def run(self):
        pass
    

    def convertdate(self,wbdate):
        format='%Y-%m-%d %H:%M:%S'
        monthdict={v:k+1 for k,v in dict(enumerate(['Jan','Feb','Mar','Apr','May','Jul','Jun','Aug','Sep','Oct','Nov','Dec'])).items()}        
        wbdate='%s-%s-%s %s' % (wbdate[wbdate.rfind(" ")+1:],str(monthdict[wbdate.split(" ")[1]]).zfill(2),wbdate.split(" ")[2],wbdate.split(" ")[3])
        # if u"刚刚" in wbdate:
        #     return datetime.now().strftime(format)
        # if u"分钟前" in wbdate:
        #     return (datetime.now()-timedelta(minutes=int(wbdate[:wbdate.find(u"分钟前")]))).strftime(format)
        # if u"小时前" in wbdate:
        #     return (datetime.now()-timedelta(hours=int(wbdate[:wbdate.find(u"小时前")]))).strftime(format)
        # if u"今天" in wbdate:
            # return ()
        return wbdate

    def get_page_json(self,pagenum):
        params={'containerid':'107603'+self.userid}
        # params={'container_ext':'profile_uid:'+self.userid, 'containerid':'100103type=401&q='+self.query,'page_type':'searchall'} if self.query else {'containerid':'107603'+self.userid}
        params['page']=pagenum
        url='https://m.weibo.cn/api/container/getIndex?'
        r=requests.get(url,params=params,headers=self.headers,verify=False)
        # reply=self.testjson()
        # print(r.text)
        reply=r.json()
        return reply

    def get_page_firsttime(self,pagenum):
        reply=self.get_page_json(pagenum)
        if reply['ok']==1:
            # print(reply['data']['cards'])
            try:
                time=self.convertdate(reply['data']['cards'][0]['mblog']['created_at']) if reply['data']['cards'][0].get('mblog') else self.convertdate(reply['data']['cards'][1]['mblog']['created_at'])
                return time
            except:
                print("not find time!") 
        
        return None

    def get_page(self,pagenum):
        reply=self.get_page_json(pagenum)
        wb_list=[]
        if reply['ok']==0:
            print(reply)
            raise Exception("Too frequent!")    

        if reply['ok']==1:
            print("Reply ok!")
            # print(reply['data']['cards'])
            cards=reply['data']['cards']
                
            for card in cards:
                # isLong=card['mblog'].get('isLongText')
                print(card)
                print("\n"*5)
                wb={}                
                # get weibo info
                if not card.get('mblog'):
                    print("Not find mblog")
                    continue
                wb["wbid"]=card['mblog'].get('id')
                wb["time"]=self.convertdate(card['mblog']['created_at'])
                # get text content
                for _ in range(self.maxtry):
                    url="https://m.weibo.cn/detail/"+card['mblog']['id']
                    html=requests.get(url,headers=self.headers,verify=False).text
                    html = html[html.find('"status":'):html.find("hotScheme")]
                    html = '{'+html[:html.rfind(',')]+'}'
                    html_json=json.loads(html,strict=False)
                    if html_json.get("status"):
                        wb["like"]=html_json["status"]["attitudes_count"]
                        wb["comment"]=html_json["status"]["comments_count"]
                        wb["repost"]=html_json["status"]["reposts_count"]
                        html=etree.HTML(html_json["status"]["text"])
                        wb["text"]=html.xpath('string(.)')
                        break
                    sleep(randint(2,5))
                
                wb_list.append(wb)
        else:
            pass
        self.wb_list.extend(wb_list)
        print(len(self.wb_list))
        return

    def get_max_page(self):
        return 100 #待修改

    # 用于实现获取指定页数
    def get_pages(self,startpage,endpage):
        if startpage>endpage:
            startpage,endpage=endpage,startpage
        for i in range(startpage,endpage):
            print("Crawling page %s" % i)
            self.get_page(i)
            sleep(randint(1,40)/10)
        return self.wb_list

    def get_pages_by_date(self,startdate,enddate):
        page20=self.get_page_firsttime(20)
        sleep(randint(1,500)/50)
        page1=self.get_page_firsttime(1)

        datetime20=datetime.strptime(page20,"%Y-%m-%d %H:%M:%S")
        datetime1=datetime.strptime(page1,"%Y-%m-%d %H:%M:%S")
        
        freq=20//(datetime1-datetime20).days-1
        
        datetimestart=datetime.strptime(startdate,"%Y-%m-%d")
        datetimeend=datetime.strptime(enddate,"%Y-%m-%d")
        

        left,right=1,self.get_max_page()
        mid=(left+right)//2        
        startpage,endpage=0,0
        while left+3<right:
            mid=(left+right)//2        
            print(left,right)
            midtime=datetime.strptime(self.get_page_firsttime(mid),"%Y-%m-%d %H:%M:%S")
            if 0<(midtime-datetimeend).days<1:
                endpage=mid
                break
            if midtime<=datetimeend:
                right=mid
            else:
                left=mid
            sleep(randint(1,500)/50)
        
        if left+3>=right:
            endpage=left
        endtime=datetime.strptime(self.get_page_firsttime(endpage),"%Y-%m-%d %H:%M:%S")
        # print(endpage,endtime)
        

        left,right=1,self.get_max_page()
        mid=(left+right)//2        
        while left+3<right:
            mid=(left+right)//2      
            print(left,right)  
            midtime=datetime.strptime(self.get_page_firsttime(mid),"%Y-%m-%d %H:%M:%S")
            if 0<(datetimestart-midtime).days<1:
                startpage=mid
                break
            if midtime>=datetimestart:
                left=mid
            else:
                right=mid
            sleep(randint(1,500)/50)

        if left+3>=right:
            startpage=right
        starttime=datetime.strptime(self.get_page_firsttime(startpage),"%Y-%m-%d %H:%M:%S")
        
        print(startpage,starttime)
        print(endpage,endtime)
        print("Crawling from %s to %s pages" % (endpage,startpage))
        self.get_pages(endpage,startpage)
        


    def write2csv(self,f):
        for wb in self.wb_list:
            f.write(",".join([str(v) for v in wb.values()])+"\n")



if __name__=="__main__":
    # 这里填写需要抓取的用户id和cookie
    mycrawler=crawler("1638782947")
    #startdate="2021-12-03"
    #enddate="2021-12-05"

    startpage=1
    #endpage=28065
    endpage=28065
    
    filename="caijingwang.csv"
    
    curpage=startpage
    
    pagenum=5
    for i in range(startpage,endpage-pagenum,pagenum):
        while True:
            try:
                print("Crawling from %s to %s" % (i,i+pagenum))
                curpage=i+pagenum
                mycrawler.get_pages(i,i+pagenum)
                with open(filename,"a") as f:
                    mycrawler.write2csv(f)
                    
                sleep(randint(20,60))
                if len(mycrawler.wb_list)!=0:
                    mycrawler.wb_list=[]
                    break
            except:
                sleep(randint(100,120))
                print("Retrying...")

    mycrawler.get_pages(curpage,endpage)
    with open(filename,"a") as f:
        mycrawler.write2csv(f)

    #wb_dataframe=pd.DataFrame(mycrawler.wb_list)
    #wb_dataframe["title"]=wb_dataframe["text"].apply(lambda x:x[x.find("【"):x.find("】")+1])
    
    #print(wb_dataframe)
    #wb_dataframe.to_csv("caijingwang.csv",index=False)

