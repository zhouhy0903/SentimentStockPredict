# -*- coding: utf-8 -*-
# @Author: zhy99
# @Date:   2021-11-25 10:58:05
# @Last Modified by:   zhy99
# @Last Modified time: 2021-11-27 20:33:24
import sqlite3
import pymysql
import pandas as pd

from utils.readconfig import Config

class Database():
	def __init__(self,host,user,password,database):
		self.host=host
		self.user=user
		self.password=password
		self.database=database
		self.conn=None
		self.cursor=None
	
	def connect(self):
		self.conn = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
		self.cursor=self.conn.cursor()		
	
	def createTable(self,name="test"):
		self.connect()
		sql="""CREATE TABLE IF NOT EXISTS {} (
	id INT auto_increment PRIMARY KEY,time VARCHAR(20),content TEXT)""".format(name)
		self.cursor.execute(sql)
		self.cursor.close()
		self.conn.close()

	def searchText(self,text,start,end):
		self.connect()
		# 返回一段时间内的weibo文字结果，以字典dict或者dataframe格式返回
		sql=""
		self.cursor.execute(sql)
		self.cursor.close()
		self.conn.close()

	def __insert(self,table,insertfield):
		# 向数据库中插入一条数据，字段包括时间、内容等
		sql="INSERT INTO {} (time,content) VALUES (\"{}\", \"{}\");".format(table,list(insertfield.values())[0],list(insertfield.values())[1])
		print("Executing ",sql)
		self.cursor.execute(sql)


	def insertOne(self,text):
		self.connect()
		self.__insert(text)
		self.cursor.close()
		self.conn.close()		

	def insertMany(self,table,texts):
		print(texts)
		self.connect()
		for text in texts:
			self.__insert(table,text)
		self.cursor.close()
		self.conn.commit()
		self.conn.close()		


# 以字典形式将内容写入数据库中
class Writer():
	def __init__(self,data):
		self.data=data
		self.path=Config["savepath"]
		print(self.path)
	
	def write2database(self):
		mydb=Database("localhost","root","root","test")
		mydb.connect()
		mydb.insertMany("test1",self.data)


class Manager():
	def __init__(self):
		self.stockpath=Config["stockpath"]
		pass
	
	@staticmethod
	def search(start,end,content):
		mydb=Database()
		results=mydb.searchText(content,start,end)
		return results

	@staticmethod
	def getstock():
		pass



if __name__=="__main__":
	# mydata=Writer(text)

	# mydb=Database("localhost","root","root","test")
	# mydb.createTable("test1")

	data=[{"time":"20211127","content":"this is a content"}]
	mywriter=Writer(data)
	mywriter.write2database()





