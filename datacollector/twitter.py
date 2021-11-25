# -*- coding: utf-8 -*-
from tweepy import OAuthHandler
import datetime
import pandas as pd
import tweepy
import time
import random
import traceback
from dbs.db import *
 
class Twitter_Spider():
    def __init__(self):
        self.main_tw_url="https://twitter.com/{}/status/{}"
        self.china_time_list = []
        self.twitter_id_list = []
        self.twitter_url_list = []
        self.twitter_text_list = []
        self.twitter_url_list = []
        self.update_time_list = []
        self.twitter_dicts = {}
        self.user_id_list = []
        self.user_name_list = []
        self.crate_time_list=[]
        self.userdicts={}
        self.stopflag=False
 
    def getapi(self):
        consumer_key = 'IAaj345Xf673kzT2'
        consumer_secret = 'ee9WEQ235555We0gP4peRbOPeeHGX1'
        access_token = '9767625356VEnq7s9ZXOHEI'
        access_secret = 'lyqj2122333o9G4fHta'
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        return api
 
    def start(self):
        api =None
        try:
            api = self.getapi()
        except tweepy.TweepError:
            print('Error! Failed to get access token.')
 
        nowdate = datetime.datetime.now()
        beforeweek=nowdate-datetime.timedelta(days=7) #一周前
        #只获取关注者id
        # ids = []
        # for page in tweepy.Cursor(api.friends_ids).pages():
        #     ids.extend(page)
        # 获取关注者id和screen_name
 
        for pages in tweepy.Cursor(api.friends).pages():
            for page in pages:
                userstr = page._json
                self.userdicts.setdefault(userstr.get("id"),userstr.get("screen_name"))
        for  user_id in self.userdicts.keys():
            self.stopflag=False
            self.twitter_dicts.clear()
            for i,statuslist in enumerate(tweepy.Cursor(api.user_timeline, id=user_id).pages()): #获取第一页,一页20个
                if not self.stopflag:
                    print("start page:{}".format(i))
                    for status in statuslist:
                        jsonstr = status._json
                        if  self.getItem(jsonstr,beforeweek,user_id):
                            break
                else:
                     break
                time.sleep(random.randint(2, 6))
            self.twitter_dicts.setdefault("user_id", self.user_id_list)
            self.twitter_dicts.setdefault("user_name", self.user_name_list)
            self.twitter_dicts.setdefault("china_time",self.china_time_list)
            self.twitter_dicts.setdefault("tw_time", self.crate_time_list)
            self.twitter_dicts.setdefault("tw_id", self.twitter_id_list)
            self.twitter_dicts.setdefault("tw_text", self.twitter_text_list)
            self.twitter_dicts.setdefault("tw_url", self.twitter_url_list)
            self.twitter_dicts.setdefault("updatetime", self.update_time_list)
            try:
               SaveData().save_object_data(self.twitter_dicts)
            except:
                print(traceback.format_exc("insert db error"))
 
 
    def getItem(self, jsonstr,beforeweek,user_id):
        create_time = jsonstr.get("created_at")
        china_time=""
        try:
           china_time=datetime.datetime.strptime(create_time,"%a %b %d %H:%M:%S +0000 %Y")
           if beforeweek>china_time:
               self.stopflag=True
               return self.stopflag
        except:
            print(traceback.format_exc())
        screen_name=self.userdicts.get(user_id)
        self.china_time_list.append(china_time)
        self.crate_time_list.append(create_time)
        self.user_id_list.append(user_id)
        self.user_name_list.append(screen_name)
        twitter_id = jsonstr.get("id")
        self.twitter_id_list.append(twitter_id)
        self.twitter_url_list.append(self.main_tw_url.format(screen_name,twitter_id))
        twitter_text = jsonstr.get("text")
        print(twitter_text)
        self.twitter_text_list.append(twitter_text)
        self.update_time_list.append(datetime.datetime.now())
        return self.stopflag
 
 
if __name__ == "__main__":
    Twitter_Spider().start()