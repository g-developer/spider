#!~/local/Python-2.7.10/bin/python
# -*- coding: UTF-8 -*-
import sys,os,time
import ConfigParser

class SB_Ini_Reader:
	def __init__(self):
		self.cf = ConfigParser.ConfigParser()
	def load(self, path): 
		self.cf.read(path)

	def getValue(self, field, key): 
		result = self.cf.get(field, key)
		return result

	def getItemsNum(self, field): 
		result = self.cf.items(field)
		return len(result)

	def getItems(self, field): 
		result = self.cf.items(field)
		return result


#if __name__ == '__main__':
#	sbIniReader = SB_Ini_Reader()
#	sbIniReader.load('./../conf/spider.ini');
#	print sbIniReader.getValue("url_entry", "0");
#	print sbIniReader.getItemsNum("url_entry");
