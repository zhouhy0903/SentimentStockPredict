# -*- coding: utf-8 -*-
# @Author: zhy99
# @Date:   2021-11-25 10:58:05
# @Last Modified by:   zhy99
# @Last Modified time: 2021-11-25 11:53:34
import sqlite3
from utils.readconfig import Config

# 需要实现更新数据，数据库查找对应词频率，
class Writer():
	def __init__(self,data):
		self.data=data
		self.path=Config["savepath"]
		
	def write2hdf5(self):
		pass

	def write2database(self):
		pass



class Manager():
	def __init__():
		

	@staticmethod
	def 




if __name__=="__main__":
	text={"time":"20200105","text":"This is a test content for calculating the frequency of the words.",
		  "time":"20211125","text":"This page is a timeline of Tweets about COVID-19 with the latest information and advice from public health authorities, media and experts across the state. For more, visit https://https://coronavirus.wa.gov/"}
	mydata=Writer(text)


