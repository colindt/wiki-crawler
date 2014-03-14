#!/usr/bin/python

import requests
import string
from lxml import etree
import sys
import io


def main():
	baseURL = "http://www.internetsafetyproject.org"
	indexURL = baseURL + "/wiki/glossary/%s?page=%d"

	chars = string.lowercase + string.digits + string.punctuation

	articles = {}
	for c in chars:
		if c == '#' or c == '?': #special url characters
			continue

		print
		print c,
		sys.stdout.flush()

		articles.update(doChar(c, indexURL))

	output = io.open("articles.txt", "w", encoding="utf8")
	for title in articles:
		output.write(u"%s\t%s\n" % (articles[title], title))
	output.close()



def doChar(c, indexURL):
	articles = {}
	page = 0
	while True:
		print page,
		sys.stdout.flush()

		resp = requests.get(indexURL % (c, page))
		if resp.status_code == 200:
			doc = etree.HTML(resp.text)
			links = doc.xpath("//table/tbody/tr/td/a")

			if len(links) == 0:
				break

			for i in range(0, len(links)):
				articles[links[i].text] = links[i].attrib["href"]

			page += 1
		else:
			break

	return articles



if __name__ == "__main__":
	main()
