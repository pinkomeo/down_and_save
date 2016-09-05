#-*- coding: utf-8 -*-

import requests
import os
import time
import urlparse
from bs4 import BeautifulSoup
from contextlib import closing
import sys
import random
import string

user_agents = [  
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
	'Opera/9.25 (Windows NT 5.1; U; en)',
	'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
	'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
	'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
	'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
	"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
	"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
]
agent = random.choice(user_agents)

headers = {     
	'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
	'Host': 'soft.duote.com.cn',
	'Connection': 'keep-alive',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0,    unit='', sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep


    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status, self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info())
        #print(end_str)


def main():

	links = []
	folder = ""

	for line in open('links.txt'):
		links.append(line)
		print line
	print len(links)
	if len(links):
		uid = 1
		for trydownloadlink in links:
			try:
				trydownloadlink = string.strip(trydownloadlink)
				print "[=] "+str(uid)+"====="
				print "[+] "+trydownloadlink
				with closing(requests.get(trydownloadlink,timeout=30, stream=True,headers=headers)) as response:
					chunk_size = 1024*1024
					#print response
					# quit()
					content_size = int(response.headers['content-length'])
					#print int(content_size/chunk_size)
					if int(content_size/chunk_size) < 120:
						filenamelist = trydownloadlink.split("/")
						filename = filenamelist[-1]
						print filename
						folder = filename.split(".")[0]
						progress = ProgressBar(filename, total=content_size, unit="MB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")

						# chunk_size = chunk_size < content_size and chunk_size or content_size
						if os.path.exists(r'downloadres/'+str(folder)+"/"):
							with open("./downloadres/"+str(folder)+"/"+filename, "wb") as file:
								for data in response.iter_content(chunk_size=chunk_size):
									file.write(data)
									progress.refresh(count=len(data))
						else:
							if not os.path.exists("downloadres/"):
								os.mkdir("downloadres/")
							if not os.path.exists("downloadres/"+str(folder)+"/"):
								os.mkdir("downloadres/"+str(folder)+"/")
							with open("./downloadres/"+str(folder)+"/"+filename, "wb") as file:
								for data in response.iter_content(chunk_size=chunk_size):
									file.write(data)
									progress.refresh(count=len(data))
				uid += 1
			except requests.HTTPError,e:
				print e.reason
	else:
		print "nothing found in links.txt!"



if __name__ == '__main__':
	main()