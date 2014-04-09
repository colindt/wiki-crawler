#!/usr/bin/python

import io
import sys

inf = io.open(sys.argv[1], "r")
out = io.open(sys.argv[2], "w")

lines = []
for line in inf:
	lines += [line]
lines.sort()

for line in lines:
	out.write(line)

inf.close()
out.close()
