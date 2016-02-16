from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import urllib2

proxy=urllib2.ProxyHandler({})
opener=urllib2.build_opener(proxy)
opener.addheaders=[('User-agent','Mozilla/5.0')]
urllib2.install_opener(opener)

client = MongoClient()
db = client["motherboard"]
collection = db['links']

def linkExtractor(urltoopen, tag1, attrib1, attrib1value, tag2 ,attrib2, attrib2value, finalAttrib):
	url = urllib2.urlopen(urltoopen).read()
	soup = bs(url)

	result = soup.findAll(tag1,{attrib1:attrib1value})
	apple = []

	for i in range(0,len(result)):
		resultDetails = result[i].find(tag2,{attrib2:attrib2value})
		link = resultDetails[finalAttrib]
		apple.append(link)

	return apple

def forPrinter(x):
	for i in range(1,len(x)):
		print x[i]

def pageProductExtractor(linkArray):
	for i in range(1,len(linkArray)):
		url2 = urllib2.urlopen(linkArray[i]).read()
		soup2 = bs(url2)
		mainContent = soup2.find("div",{"class":"centerColAlign"})
		nameDiv = mainContent.find(id="title_feature_div")
		nameSpan = nameDiv.find("span",{"class":"a-size-large"})
		name = nameSpan.getText()
		print name
	

url = "http://www.amazon.com/s/ref=nb_sb_ss_c_0_7?url=search-alias%3Delectronics&field-keywords=motherboard&sprefix=motherboard%2Cundefined%2C417"
links = linkExtractor(url,"li","class","s-result-item","a","class","a-link-normal","href")
#forPrinter(links)
pageProductExtractor(links)