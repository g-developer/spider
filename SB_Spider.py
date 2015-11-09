#!~/local/Python-2.7.10/bin/python
# -*- coding: UTF-8 -*-
from src.ConfReader import SB_Ini_Reader
from src.SB_Spider_Url import SB_Spider_Url
from src.SB_Spider_Consumer import SB_Spider_Consumer
from src.SB_Spider_Producer import SB_Spider_Producer
import threading
import Queue
import time
import urllib2
import socket

if __name__ == '__main__':

	path = './conf/spider.ini';
	sbIniReader = SB_Ini_Reader()
	sbIniReader.load(path)
	httpNum = int(sbIniReader.getValue("thread", "http_num"))
	queueCapactiy = int(sbIniReader.getValue("thread", "queue_capacity"))
	urlFile = sbIniReader.getValue("output", "fail_dir") + '/url'
	logFile = sbIniReader.getValue("output", "fail_dir") + '/log'
	logfd = open(logFile, 'a')
	urlfd = open(urlFile, 'a')
	consumerSize = 1
	producerSize = 1 
	consumerArray =  {}
	producerArray =  {}
	urlHasVisit = {}
	urlMutex = threading.Lock()
	htmlMutex = threading.Lock()
	urlLogMutex = threading.Lock()
	urlQueue = Queue.Queue()	
	htmlQueue = Queue.Queue()

	filters = sbIniReader.getItems("filters")
	kwagrs = {'urlMap' : urlHasVisit, 'urlQueue' : urlQueue, 'htmlQueue' : htmlQueue, 'urlJoinCount':0, 'htmlJoinCount':0, 'urlMutex' : urlMutex, 'htmlMutex' : htmlMutex, 'urlLogMutex' : urlLogMutex, 'urlfd' : urlfd, 'filters' : filters}

	initUrls = sbIniReader.getItems("url_entry")
	for urlInit in initUrls :
		spiderUrlTmp = SB_Spider_Url()
		if spiderUrlTmp.preUrlForQueue(urlInit[1], urlInit[0], 0, urlHasVisit, filters) :
			urlQueue.put(spiderUrlTmp)
	
	ssp = SB_Spider_Producer("Test_Producer_0", kwagrs)
	ssc = SB_Spider_Consumer("Test_Consumer_0", kwagrs)

	
	for i in range(0, consumerSize) :
		consumerArray[i] = SB_Spider_Consumer("Test-Consumer-" + str(i), kwagrs)
		consumerArray[i].start()

	for j in range(0, producerSize) :
		producerArray[j] = SB_Spider_Producer("Test-Producer-" + str(j), kwagrs)
		producerArray[j].start()


	exitCount = 0	
	if consumerSize == kwagrs['urlJoinCount']:
		for i in consumerArray :
			consumerArray[i].join()
		exitCount += 1

		
	if producerSize == kwagrs['htmlJoinCount'] :
		exitCount += 1
		for i in producerArray :
			producerArray[i].join()

	print "Total Records : " + str(len(urlHasVisit))
	print "urlQueue Records : " + str(urlQueue.qsize())
	print "html Records : " + str(htmlQueue.qsize())
	if 2 == exitCount :
		logfd.close()
		urlfd.close()
		
		for strMd5 in urlHasVisit :
			print strMd5
			urlHasVisit[strMd5].showInfo()

