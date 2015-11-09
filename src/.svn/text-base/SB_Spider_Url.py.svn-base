#!~/local/Python-2.7.10/bin/python
# -*- coding: UTF-8 -*-

import urllib2
import re
import hashlib

class SB_Spider_Url :
	def __init__ (self):
		self.httpCode = 200
		self.pv = 0
		self.selfMd5 = ''
		self.parentMd5 = []
		self.childMd5 = []
		self.level = 0
		self.hrefValue = ''
		self.isVisited = False
		self.isInFilter = False
		self.reason = ''
	
	def checkInFilter(self, url, filters) :
		ret = False
		for filter in filters :
			if -1 != url.find(filter[1]) :
				ret = True
				break
		return ret

	def preUrlForQueue (self, url, value, level, urlMap, filters) :	
		if -1 == url.find('meilishuo') :
			return False

		if self.checkInFilter(url, filters) : 
			#self.level = level
			#self.url = url
			#self.selfMd5 = self.getStrMd5(url)
			#self.isVisited = True
			#self.hrefValue = value
			#self.pv = 1
			#urlMap[urlMd5] = self
			#self.isInFilter = True
			return False
		else :
			urlMd5 = self.getStrMd5(url)
			if urlMap.has_key(urlMd5) and urlMap[urlMd5].isVisited :
				urlMap[urlMd5].pv += 1
				return False
			else :
				self.level = level
				self.url = url
				self.selfMd5 = self.getStrMd5(url)
				self.isVisited = False
				self.hrefValue = value
				self.pv = 0
				urlMap[urlMd5] = self
				return True
	
	def getStrMd5(self, str):
		md5 = hashlib.md5()
		md5.update(str)
		return md5.hexdigest()

	def showInfo(self) :
		print "\turl		:" + str(self.url)
		print "\thttpCode	:" + str(self.httpCode)
		print "\tlevel		:" + str(self.level)
		print "\tselfMd5	:" + str(self.selfMd5)
		print "\tparentMd5	:" + str(self.parentMd5)
		print "\tchildMd5	:" + str(self.childMd5)
		print "\threfValue	:" + self.hrefValue
		print "\tisVisited	:" + str(self.isVisited)
		print "\tpv		:" + str(self.pv)


