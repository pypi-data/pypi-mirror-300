#!/usr/bin/env python3

"""
Adds a mark at the end of line of "codebinField"

"""
import sys
args = sys.argv

inputFilename = args [1]
lines = open (inputFilename).readlines ()

newlines = []
for line in lines:
	if "codebinField" in line:
		if not "," in line:
			line = line.strip() + ",\n"

		newlines.append (line)

outFilename = inputFilename.split (".")[0] + "-NEW.json" 
open (outFilename, "w").writelines (newlines)
