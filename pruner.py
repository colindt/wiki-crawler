#!/usr/bin/python

import io
import grapher
import sys

def main():
	input = io.open("graph.dot", "r")

	edges = {}
	indegree = {}
	outdegree = {}

	for line in input:
		if line.strip()[:2] == "//":
			continue
		elif "[label=" in line:
			node = line.split()[0].lower()
			edges[node] = set()
			indegree[node] = 0
			outdegree[node] = 0
		elif "->" in line:
			sp = line.split()
			start = sp[0].lower()
			end = sp[2][:-1].lower()
			if end == "node__wiki_how_3f":
				end = "node__wiki_how"

			if not start in edges:
				edges[start] = set()
			if not end in edges:
				edges[end] = set()
			if not start in outdegree:
				outdegree[start] = 0
			if not start in indegree:
				indegree[start] = 0
			if not end in indegree:
				indegree[end] = 0
			if not end in outdegree:
				outdegree[end] = 0

			edges[start].add(end)
			outdegree[start] += 1
			indegree[end] += 1

	input.close()

	in0 = io.open("in0.htm", "w")
	out0 = io.open("out0.htm", "w")
	zero = io.open("zero.htm", "w")
	twoway = io.open("twoway.htm", "w")

	title, n2l = generate_stuff(edges)

	in0_num = 0
	out0_num = 0
	zero_num = 0
	two_num = 0

	#print "Indegree\tOutdegree\tNode"
	for node in edges:
		ind = indegree[node]
		outd = outdegree[node]
		if ind == 0:
			in0_num += 1
			if node in n2l:
				in0.write("<li><a href=\"%s\">%s</a></li>\n" % (n2l[node], title[node]))
			#else:
				#in0.write("<li>%s</li>\n" % (node))
		if outd == 0:
			out0_num += 1
			if node in n2l:
				out0.write("<li><a href=\"%s\">%s</a></li>\n" % (n2l[node], title[node]))
			#else:
				#out0.write("<li>%s</li>\n" % (node))
		if ind == 0 and outd == 0:
			zero_num += 1
			if node in n2l:
				zero.write("<li><a href=\"%s\">%s</a></li>\n" % (n2l[node], title[node]))
			#else:
				#zero.write("<li>%s</li>\n" % (node))
		if ind != 0 and outd != 0:
			two_num += 1
			if node in n2l:
				twoway.write("<li><a href=\"%s\">%s</a></li>\n" % (n2l[node], title[node]))
			#else:
				#twoway.write("<li>%s</li>\n" % (node))
		#print "%d\t%d\t%s" % (ind, outd, node)

	print "In0\tOut0\tBoth0\tTwo Way"
	print "%d\t%d\t%d\t%d" % (in0_num, out0_num, zero_num, two_num)

	in0.close()
	out0.close()
	zero.close()
	twoway.close()

	#make_graph(edges, indegree, outdegree, title, sys.argv[1], int(sys.argv[2]))

	non_adj(edges, indegree, outdegree, title, sys.argv[1], sys.argv[2], sys.argv[3], n2l)


def generate_stuff(all):
	titles = {}
	n2l = {}
	input = io.open("articles.txt", "r")

	for line in input:
		sp = line.strip().split("\t")
		link = sp[0]
		name = sp[1]
		node = grapher.nodeName(link)
		titles[node] = name
		n2l[node] = link

	input.close()

	for node in all:
		if not node in titles:
			titles[node] = node

	return titles, n2l


def non_adj(edges, indegree, outdegree, title, startnode, fname_un, fname_re, n2l):
	used = set()
	unused = set(edges.keys())

	dfs(edges, startnode, used, unused)

	unreachable = list(unused)
	unreachable.sort()
	reachable = list(used)
	reachable.sort()

	out = io.open(fname_un, "w")
	for node in unreachable:
		if node in n2l.keys():
			out.write("<li><a href=\"%s\">%s</a></li>\n" % (n2l[node], title[node]))
		#else:
			#out.write("<li>%s</li>\n" % node)
	out.close()

	out = io.open(fname_re, "w")
	for node in reachable:
		if node in n2l.keys():
			out.write("<li><a href=\"%s\">%s</a></li>\n" % (n2l[node], title[node]))
		#else:
			#out.write("<li>%s</li>\n" % node)
	out.close()


def dfs(edges, startnode, used, unused):
	for node in edges[startnode]:
		if node in unused:
			unused -= set([node])
			used |= set([node])
			dfs(edges, node, used, unused)


def make_graph(edges, indegree, outdegree, title, root, depth):
	output = io.open(sys.argv[3], "w")
	output.write(u"digraph {\n")

	#for node in edges:
	#	if indegree[node] > 0 and outdegree[node] > 0:
	#		output.write(u"%s [label=\"%s\"];\n" % (node, grapher.nodeLabel(title[node])))
    #
	#for start in edges:
	#	for end in edges[start]:
	#		if indegree[start] > 0 and outdegree[start] > 0 and indegree[end] > 0 and outdegree[end] > 0:
	#			output.write(u"%s -> %s;\n" % (start, end))

	include = set([root])
	l = 0
	level = set([root])
	while l < depth:
		newlevel = set()
		for node in level:
			for end in edges[node]:
				newlevel.add(end)
				include.add(end)
		l += 1
		level = newlevel

	for node in include:
		output.write(u"%s [label=\"%s\"];\n" % (node, grapher.nodeLabel(title[node])))

	for start in edges:
		for end in edges[start]:
			if start in include and end in include:
				output.write(u"%s -> %s;\n" % (start, end))

	output.write(u"}")
	output.close()


if __name__ == "__main__":
	main()
