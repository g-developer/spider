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



class SB_Spider_Consumer(threading.Thread):
	timeout = 30
	uid = "273823537"
	__headers = {
			"Content-type": "application/x-www-form-urlencoded",
			"Accept": "text/plain",
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
			"Refer": "http://www.meilishuo.com/",
			"Cookie": "SEASHELL=fMqQClYOjekZl591GOMtAg==; CHANNEL_FROM=0; pgv_pvi=6726221824; __v3_c_review_10918=0; __v3_c_last_10918=1444644446616; __v3_c_visitor=1444644446616717; oa_mlsoatoken=59bc9c4295d258b1f51209048ec25575; MEILISHUO_MM=60055305636dd201f5b647b8edae9735; santorini_mm=83079e32546d732c56dc1a1510bf01cb; pgv_si=s6491837440; query_param_r=qr_code.1_m-running_man_vote; r_mark=qr_code.1_m-running_man_vote; _pzfxuvpc=1445417052968%7C2855937860591640555%7C6%7C1445417079580%7C1%7C%7C5806441474314875839; _ga=GA1.2.1175686526.1445417053; ORIGION_REFER=http%3A%2F%2Fwww.meilishuo.com%2F; MEILISHUO_GLOBAL_KEY=a268efaa34ef98583150518194652059; numInCart=0; Hm_lvt_dde72e241ea4e39b97eca9a01eea2dda=1444393538,1445323968,1445396367,1445414975; Hm_lpvt_dde72e241ea4e39b97eca9a01eea2dda=1445583416; MEILISHUO_RZ=821470618; MLS_S_RZ=821470618; home_up_num=0"
			}

	def __init__ (self, threadName, kargs):
		threading.Thread.__init__(self, name = threadName, kwargs = kargs)
		urllib2.socket.setdefaulttimeout(self.timeout)
		socket.setdefaulttimeout(self.timeout)
		self.name = threadName
		self.kwargs = kargs


	def debug(self) :
		print self.name + " Total Records : " + str(len(self.kwargs['urlMap']))
		print self.name + " UrlQueue Records : " + str(self.kwargs['urlQueue'].qsize())
		print self.name + " Html Records : " + str(self.kwargs['htmlQueue'].qsize())
		print self.name + " UrlJoinCount : " + str(self.kwargs['urlJoinCount'])
		print self.name + " HtmlJoinCount : " + str(self.kwargs['htmlJoinCount'])

	def run(self) :
		self.consume()
		self.debug()
		
	def doRequest(self, urlInstance) :
		resp = None
		httpCode = 200
		reason = ''
		if not urlInstance.isVisited or (urlInstance.level > 6):
			try :
				req = urllib2.Request(urlInstance.url, None, self.__headers)
				resp = urllib2.urlopen(req)
				html = resp.read()
				tmp = {"objUrl" : urlInstance, "html" : html}
				self.kwargs['htmlQueue'].put(tmp)
			except urllib2.URLError as e :
				if hasattr(e, 'code'): 
					httpCode = e.code
				elif hasattr(e, 'reason'):
					httpCode = 0
					reason = e.reason
					print self.name + " -----1111111-- " + e.reason
					print e
					urlInstance.showInfo()
					exit(0)
			except BaseException as e2 :
				httpCode = -1
				reason = 'socket Error!'
				print self.name + " -----2222222-- " + e2.reason
				print e2
				urlInstance.showInfo()
				exit(0)
			finally :
				if resp :
					resp.close()
				return (httpCode,reason)


	def consume(self) :
		retry = 0
		while 3 > retry :
			if self.kwargs['urlQueue'].empty() :
				time.sleep(60)
				#print self.name + " self.kwargs['urlQueue'] Empty ! Retry : " + str(retry)
				retry += 1
			else :
				retry = 0
				urlInstance = self.kwargs['urlQueue'].get()
				
				for i in range(0, 1) :
					httpCode,reason = self.doRequest(urlInstance)
					if 200 == httpCode :
						break;
					else :
						pass

				urlInstance.httpCode = httpCode
				urlInstance.reason = reason

				self.kwargs['urlMap'][urlInstance.selfMd5] = urlInstance
				self.kwargs['urlMap'][urlInstance.selfMd5].isVisited = True
				if 200 != urlInstance.httpCode and urlInstance.level > 0:
					self.writeUrl(urlInstance)

		if self.kwargs['urlMutex'].acquire(3) :
			self.kwargs['urlJoinCount'] += 1
			self.kwargs['urlMutex'].release()

	def writeUrl(self, urlInstance) :
		if self.kwargs['urlLogMutex'].acquire(6) :
			level = 0
			index = ''
			padding = '--'
			objUrlTmp = urlInstance
			ctx = ''
			while objUrlTmp.level > 0 :
				if (0 == level) :
					index = ''
				else :
					if len(objUrlTmp.parentMd5) > 0 :
						for j in objUrlTmp.parentMd5 :
							if self.kwargs['urlMap'][objUrlTmp.parentMd5[j]].level == (objUrlTmp.level - 1):
								objUrlTmp = self.kwargs['urlMap'][objUrlTmp.parentMd5[j]]
								break
					index = '|'
				print self.name + "------------3333333---------------\n"
				objUrlTmp.showInfo()
				for i in range(0, level) :
					index += padding
				ctx = index + objUrlTmp.url + "; httpCode=" + str(objUrlTmp.httpCode)  + "; value=" + objUrlTmp.hrefValue + "; pv=" + str(objUrlTmp.pv)+ "\n"
				#ctx += index + objUrlTmp.url + "; httpCode=" + str(objUrlTmp.httpCode)  + "; value=" + objUrlTmp.hrefValue + "\n"
				level += 1
			ctx += "\n"
			self.kwargs['urlfd'].write(ctx)
			self.kwargs['urlLogMutex'].release()
