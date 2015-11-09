#!~/local/Python-2.7.10/bin/python
# -*- coding: UTF-8 -*-

from SB_Spider_Url import SB_Spider_Url
import urllib2
import socket
import re
import os
import threading
import time
import hashlib

ISOTIMEFORMAT = '%Y-%m-%d %X'

from SB_Spider_Url import SB_Spider_Url

class SB_Spider_Producer(threading.Thread):
	def __init__ (self, threadName, kargs):
		threading.Thread.__init__(self, name = threadName, kwargs = kargs)
		self.name = threadName
		self.kwargs = kargs
		self.urlPattern = re.compile(r'((<a ).*?(/a>){1,1})')
		self.uid = "273823537"
		#self.domainPattern = re.compile(r'(http://)([^/]+)/')
		self.domainPattern = re.compile(r'(http(s)*://)([^/]+)(/)*')

	def trim(self, str) :
		if -1 != str.find("\t") :
			x_list = str.split("\t")
			ret = ''.join(x_list)
		else :
			ret = str
		if -1 != ret.find(' ') :
			x_list = ret.split(' ')
			ret = ''.join(x_list)
		return ret

	def getUrlDomain(self, url) :
		domains = self.domainPattern.match(url)
		groups = domains.groups()
		return groups[0] + groups[2]

	def getUrlValueFromStr(self, str, domain) :
		urls = []
		value = ''
		valueTmp = ''
		tmp1 = str.replace('<?=user_id?>', "273823537")
		tmp1 = str.replace('amp;', "")
		tmp2 = tmp1.replace('<', ' ')
		tmp3 = tmp2.replace('>', ' ')
		arrTmp = tmp3.split(' ');
		for one in arrTmp :
			part = ''
			if -1 != one.find('href') :
				part = one[6:-1]
			elif -1 != one.find('src') :
				part = one[4:-1]
			else :
				pass
			if part :
				if '/' == part[0] :
					part = domain + part
				if '"' == part[0] :
					part = part[1:]
				if '"' == part[-1] :
					part = part[0:-1]
				urls.append(part)

		if len(urls) > 0:
			valueTmp = arrTmp[-3]
			if -1 != value.find(' ') :
				value = self.trim(valueTmp)
			else :
				value = valueTmp
		#pp = pprint.PrettyPrinter(indent=4)
		#pp.pprint(value)
		return (urls,value)
	
	def debug(self) :       
		print self.name + " Total Records : " + str(len(self.kwargs['urlMap']))
		print self.name + " UrlQueue Records : " + str(self.kwargs['urlQueue'].qsize())
		print self.name + " Html Records : " + str(self.kwargs['htmlQueue'].qsize())
		print self.name + " UrlJoinCount : " + str(self.kwargs['urlJoinCount'])
		print self.name + " HtmlJoinCount : " + str(self.kwargs['htmlJoinCount'])

	def run(self) :
		self.produce()
		self.debug()
	
	def produce(self) :
		retry = 0
		while 3 > retry :
			if self.kwargs['htmlQueue'].empty() :
				time.sleep(60)
				#print self.name + " self.kwargs['htmlQueue'] Empty ! Retry : " + str(retry)
				retry += 1
			else :
				retry = 0
				htmlInstance = self.kwargs['htmlQueue'].get()
				objUrl = htmlInstance['objUrl']
				html = htmlInstance['html']
				allUrls = self.urlPattern.findall(html)
				domain = self.getUrlDomain(objUrl.url)
				for urlInstance in allUrls :
					urls  = []
					value = ''
					urls, value = self.getUrlValueFromStr(urlInstance[0], domain)
					if 0 < len(urls) :
						for url in urls :
							spiderUrlTmp = SB_Spider_Url()
							spiderUrlTmp.parentMd5.append(objUrl.selfMd5)
							if spiderUrlTmp.preUrlForQueue(url, value, (objUrl.level + 1), self.kwargs['urlMap'], self.kwargs['filters']) :
								self.kwargs['urlQueue'].put(spiderUrlTmp)
								#if spiderUrlTmp.selfMd5 :
								self.kwargs['urlMap'][objUrl.selfMd5].childMd5.append(spiderUrlTmp.selfMd5)
		if self.kwargs['htmlMutex'].acquire(3) :
			self.kwargs['htmlJoinCount'] += 1
			self.kwargs['htmlMutex'].release()
