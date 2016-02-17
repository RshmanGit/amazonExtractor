from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import urllib2

proxy=urllib2.ProxyHandler({})
opener=urllib2.build_opener(proxy)
opener.addheaders=[('User-agent','Mozilla/5.0')]
urllib2.install_opener(opener)

client = MongoClient()
db = client["motherboard"]
collection = db['results']

def linkExtractor(urltoopen, tag1, attrib1, attrib1value, tag2 ,attrib2, attrib2value, finalAttrib):
	url = urllib2.urlopen(urltoopen).read()
	soup = bs(url)
	lastPageTag = soup.find("span",{"class":"pagnDisabled"})
	lastPage = int(lastPageTag.getText())

	apple = []

	#inside the loop
	for j in range(0,lastPage):

		result = soup.findAll(tag1,{attrib1:attrib1value})

		for i in range(0,len(result)):
			resultDetails = result[i].find(tag2,{attrib2:attrib2value})
			link = resultDetails[finalAttrib]
			apple.append(link)

		nextLinkATag = soup.find("span",{"class":"pagnRA"})
		nextLink =  "http://www.amazon.com"+nextLinkATag.a['href']
		url = urllib2.urlopen(nextLink).read()
		soup = bs(url)

	#the loop ends

	return apple

def forPrinter(x):
	for i in range(1,len(x)):
		print i
		#print x[i]

def pageProductExtractor(linkArray):
	entry = {}
	for i in range(0,len(linkArray)):
		url2 = urllib2.urlopen(linkArray[i]).read()
		soup2 = bs(url2)
		mainContent = soup2.find("div",{"class":"centerColAlign"})

		#Finding the name
		nameDiv = mainContent.find(id="title_feature_div")
		nameSpan = nameDiv.find("span",{"class":"a-size-large"})
		entry["srNo"] = i
		entry["name"] = nameSpan.getText()
		
		#finding the price
		try:
			priceDiv = mainContent.find(id="price_feature_div")
			priceSpan = priceDiv.find("span",{"class":"a-size-medium"})
			price = priceSpan.getText()
			entry["price"] = priceSpan.getText()
		except:
			priceDiv = mainContent.find(id="olp_feature_div")
			priceSpan = priceDiv.find("span",{"class":"a-color-price"})
			price = priceSpan.getText()
			entry["price"] = priceSpan.getText()

		#finding the details
		feature = []
		detailsDiv = mainContent.find(id="featurebullets_feature_div")
		detailsSpan = detailsDiv.findAll("span",{"class":"a-list-item"})
		for j in range(0,len(detailsSpan)):
			feature.append(detailsSpan[j].getText())
		entry["details"] = feature

		db.results.insert(entry)
		entry = {}

url = "http://www.amazon.com/s/ref=nb_sb_ss_c_0_7?url=search-alias%3Delectronics&field-keywords=motherboard&sprefix=motherboard%2Cundefined%2C417"
links = linkExtractor(url,"li","class","s-result-item","a","class","a-link-normal","href")
#forPrinter(links)
pageProductExtractor(links)