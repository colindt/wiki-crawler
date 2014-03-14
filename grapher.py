#!/usr/bin/python

import io
import requests
from lxml import etree


def main():
	input = io.open("articles.txt", "r")

	linkToName = {}
	links = {}

	for line in input:
		sp = line.strip().split("\t")
		assert len(sp) == 2
		link = sp[0]
		name = sp[1]
		linkToName[link] = name
	input.close()

	i = 1
	print "Number\tLinks\tTitle"
	for link in linkToName:
		linkList = listLinks("http://www.internetsafetyproject.org" + link)
		print "%d\t%d\t%s" % (i, len(linkList), linkToName[link])
		links[link] = linkList
		i += 1

	makeGraph(linkToName, links)


def listLinks(url):
	resp = requests.get(url)
	if resp.status_code == 200:
		result = []
		doc = etree.HTML(resp.text)
		links = doc.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' pane-node-field-article-body ')]//a")
		for i in range(0, len(links)):
			if links[i].attrib.get("href","")[:6] == "/wiki/":
				result.append(links[i].attrib["href"])
		return list(set(result))
	else:
		return []


def makeGraph(l2n, links):
	output = io.open("graph.dot", "w")
	output.write(u"digraph {\n")

	for link in l2n:
		output.write(u"%s [label=\"%s\"];\n" % (nodeName(link), nodeLabel(l2n[link])))

	for page in links:
		for link in links[page]:
			output.write(u"%s -> %s;\n" % (nodeName(page), nodeName(link)))

	output.write(u"}")
	output.close()


def nodeName(wikiLink):
	return "node_" + wikiLink.replace("/","_").replace("-","_").replace(".","_").replace("%","_").lower()


def nodeLabel(title):
	return title.replace("\"","\\\"")


if __name__ == "__main__":
	main()
