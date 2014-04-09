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

	in0 = io.open("in0.txt", "w")
	out0 = io.open("out0.txt", "w")
	zero = io.open("zero.txt", "w")
	twoway = io.open("twoway.txt", "w")

	title = generate_titles(edges)

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
			in0.write("%s\n" % title[node])
		if outd == 0:
			out0_num += 1
			out0.write("%s\n" % title[node])
		if ind == 0 and outd == 0:
			zero_num += 1
			zero.write("%s\n" % title[node])
		if ind != 0 and outd != 0:
			two_num += 1
			twoway.write("%s\n" % title[node])
		#print "%d\t%d\t%s" % (ind, outd, node)

	print "In0\tOut0\tBoth0\tTwo Way"
	print "%d\t%d\t%d\t%d" % (in0_num, out0_num, zero_num, two_num)

	in0.close()
	out0.close()
	zero.close()
	twoway.close()

	#make_graph(edges, indegree, outdegree, title, sys.argv[1], int(sys.argv[2]))

	non_adj(edges, indegree, outdegree, title, sys.argv[1], sys.argv[2], sys.argv[3])



def generate_titles(all):
	result = {}
	input = io.open("articles.txt", "r")

	for line in input:
		sp = line.strip().split("\t")
		link = sp[0]
		name = sp[1]
		result[grapher.nodeName(link)] = name

	input.close()

	for node in all:
		if not node in result:
			result[node] = node

	return result


def non_adj(edges, indegree, outdegree, title, startnode, fname_un, fname_re):
	used = set()
	unused = set(edges.keys())

	dfs(edges, startnode, used, unused)

	unreachable = []
	for node in unused:
		unreachable += [title[node]]
	unreachable.sort()

	reachable = []
	for node in used:
		reachable += [title[node]]
	reachable.sort()

	out = io.open(fname_un, "w")
	for article in unreachable:
		out.write("%s\n" % article)
	out.close()

	out = io.open(fname_re, "w")
	for article in reachable:
		out.write("%s\n" % article)
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
