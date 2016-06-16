#coding: utf-8

from lxml import html, etree
from lxml.html.clean import clean_html
from urllib2 import urlopen
from io import StringIO
import chardet

def get_fulltext(category, collect, title, page_url):
	print category, collect, title
	try:
		content = urlopen(page_url).read()
	except Exception as e:
		print e
		return {"title":"%s_%s_%s" % (category, collect, title), "text":""}
		
	page = html.parse(StringIO(content.decode('utf-8')))
	table = page.xpath('//td[2]/div/div[7]')
	if len(table) > 0:
		odes = table[0]
		skip_state = 0
		full_text = []
		for element in odes.getchildren():
			text = ""
			if element.tag is etree.Comment:
				continue
			if element.tag == "h2":
				skip_state += 1
			if (element.tag == "div") and skip_state == 1:
				text = element.text_content().strip()
			if (element.tag == "br") and skip_state == 1:
				if element.tail is not None:
					text = element.tail.strip()
			if text != "":
				full_text.append(text)
	return {"title":"%s_%s_%s" % (category, collect, title), "text":full_text}

url = "http://www.zwbk.org/MyLemmaShow.aspx?lid=76385"
connect = urlopen(url)

content = connect.read()
page = html.parse(StringIO(content.decode('utf-8')))
table = page.xpath("//table/tr/td[2]/div/div[7]")

collect_list = []
for links in table[0].find_class("classic"):
	title = links.text_content().split(u"·")
	if len(title) > 3:
		page_url = links.attrib.get("href")
		collect_list.append({
			"category": title[1],
			"collect": title[2],
			"title": title[3],
			"page_url": page_url
			})

result = map(lambda x: get_fulltext(**x), collect_list)

with open("fulltext.txt", "w") as f:
	for ode in result:
		f.write(ode.get("title").encode('utf-8') + "\r")
		for text in ode.get("text"):
			f.write(text.encode('utf-8') + "\r")




