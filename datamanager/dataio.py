# -*- coding: utf-8 -*-
# @Author: zhy99
# @Date:   2021-11-25 10:58:05
# @Last Modified by:   zhy99
# @Last Modified time: 2021-11-27 20:33:24
# import sqlite3
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
	
	def createDatabase(self,dbname):
		conn = pymysql.connect(host=self.host,user=self.user,password=self.password)
		cursor=conn.cursor()		
		sql="CREATE DATABASE {};".format(dbname)
		cursor.execute(sql)
		cursor.close()
		conn.close()

	def createTable(self,name):
		# sql="""CREATE TABLE IF NOT EXISTS {} (
	# id INT auto_increment PRIMARY KEY,time VARCHAR(20),content TEXT)""".format(name)
		
		columns=["id","time","likes","comment","share","text"]
		sql="CREATE TABLE IF NOT EXISTS {} ({} VARCHAR(20) PRIMARY KEY,{} VARCHAR(20),{} VARCHAR(20),{} VARCHAR(20),{} VARCHAR(20),{} TEXT);".format(name,*columns)
		self.cursor.execute(sql)



	def searchText(self,text,start,end):
		# 返回一段时间内的weibo文字结果，以字典dict或者dataframe格式返回
		sql=""
		self.cursor.execute(sql)

	def __insert(self,table,insertfield):
		# 向数据库中插入一条数据，字段包括时间、内容等
		
		columns=["id","time","likes","comment","share","text"]
		sql="INSERT INTO {} ({},{},{},{},{},{}) VALUES (\"{}\", \"{}\" , \"{}\", \"{}\" , \"{}\", \"{}\");".format(table,*columns,*list(insertfield.values()))
		print("Executing ",sql)
		self.cursor.execute(sql)
		self.conn.commit()


	def insertOne(self,text):
		self.__insert(text)

	def insertMany(self,table,texts):
		for text in texts:
			try:
				self.__insert(table,text)
			except:
				pass
	
	def is_exists_databases(self,database):
		conn = pymysql.connect(host=self.host,user=self.user,password=self.password)
		cursor=conn.cursor()		

		sql="SHOW DATABASES;"
		result=None
		try:
			cursor.execute(sql)
			result=cursor.fetchall()
			result=[i[0] for i in result]
			
		except Exception:
			print("Failed to get databases result!")
		cursor.close()
		conn.close()
		return database in result


# 以字典形式将内容写入数据库中
class Writer():
	def __init__(self,df,database,tablename):
		self.database=database
		self.tablename=tablename
		
		self.data=[]
		for idx in range(len(df)):
			# print(df.iloc[idx].tolist())
			self.data.append(dict(zip(df.columns,df.iloc[idx].tolist())))


		# self.path=Config["savepath"]
		# if not os.path.exists(self.path):
			# os.makedirs(self.path)

	
	def write2database(self):
		mydb=Database("localhost","root","mysql990903",self.database)
		if not mydb.is_exists_databases(self.database):
			print("Database {} not exists!".format(self.database))
			mydb.createDatabase(self.database)
			if mydb.is_exists_databases(self.database):
				print("Successful create database!")
			else:
				raise Exception("Failed to create database!")
		
		
		mydb.connect()
		mydb.createTable(self.tablename)
		mydb.insertMany(self.tablename,self.data)
		mydb.cursor.close()
		mydb.conn.close()

class Manager():
	def __init__(self):
		pass









