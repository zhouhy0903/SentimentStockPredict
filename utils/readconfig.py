# -*- coding: utf-8 -*-
# @Author: zhy99
# @Date:   2021-11-25 11:12:09
# @Last Modified by:   zhy99
# @Last Modified time: 2021-11-25 11:27:35
from configparser import ConfigParser

def readconfig():
	cf = ConfigParser()
	cf.read("config.cfg")
	config={}

	print(cf.sections())
	for section in cf.sections():
		for key,value in cf.items(section):
			config[key]=value
	# config=(cf.get("database", "savepath"))
	return config

Config=readconfig()

# print(readconfig())