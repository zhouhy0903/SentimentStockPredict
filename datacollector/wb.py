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

    def get_page(self,pagenum):
        # params={'container_ext':'profile_uid:'+self.userid, 'containerid':'100103type=401&q='+self.query,'page_type':'searchall'} if self.query else {'containerid':'107603'+self.userid}
        params={'containerid':'107603'+self.userid}
        params['page']=pagenum
        url='https://m.weibo.cn/api/container/getIndex?'
        r=requests.get(url,params=params,headers=self.headers,verify=False)
        # reply=self.testjson()
        # print(r.text)
        reply=r.json()

        # print(reply)
        wb_list=[]
        if reply['ok']==1:
            # print(reply['data']['cards'])
            cards=reply['data']['cards']
            for card in cards:
                isLong=card['mblog'].get('isLongText')
                # print(isLong)
                wb={}                
                # get weibo info
                wb["time"]=self.convertdate(card['mblog']['created_at'])
                # get text content
                if isLong:
                    for _ in range(self.maxtry):
                        url="https://m.weibo.cn/detail/"+card['mblog']['id']
                        html=requests.get(url,headers=self.headers,verify=False).text
                        html = html[html.find('"status":'):html.find("hotScheme")]
                        html = '{'+html[:html.rfind(',')]+'}'
                        html_json=json.loads(html,strict=False)
                        if html_json.get("status"):
                            html=etree.HTML(html_json["status"]["text"])
                            wb["text"]=html.xpath('string(.)')       
                            break
                        sleep(randint(2,5))
                else:
                    text=card['mblog']['text']
                    html=etree.HTML(text)
                    wb["text"]=html.xpath('string(.)')       
                wb_list.append(wb)
        else:
            pass
        self.wb_list=wb_list
        return

    # 用于实现获取指定页数 
    def get_pages(self,startdate,enddate):
        pass



if __name__=="__main__":
    # 这里填写需要抓取的用户id和cookie
    mycrawler=crawler("2803301701")
    mycrawler.get_page(10)
    wb_dataframe=pd.DataFrame(mycrawler.wb_list)
    print(wb_dataframe)
    # wb_dataframe.to_csv("test_ren.csv",index=False)

