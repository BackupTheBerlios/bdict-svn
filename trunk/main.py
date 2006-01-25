#! /usr/bin/python
#
#      main.py version 0.0.1
#         (c) 2005 Blug.in
#
#	Insert GPL Here
#
#		This is Part of BDict
#	ChangeLog:
#		Demo By Tejas Dinkar <tejasdinkar AT gmail DOT com>
#

line_length = 54 

def format_text(text):
	text = text.split("\n\n")[0] # Just take the 1st Paragraph
	replacements = {
		'[[':"",
		']]':"",
	}
	for i in replacements.keys():
		text = text.replace(i,replacements[i])
	# next we make sure there is 80 chars or less / line
	words = text.split()
	lines = []
	tmp = []
	tmp_len = 0
	for i in words:
		if (tmp_len + len(i) + 1) <= line_length:
			tmp.append(i)
			tmp_len += len(i) + 1
		else:
			lines.append(" ".join(tmp))
			tmp = [i]
			tmp_len = len(i) + 1

	if lines[-1] != tmp:
		lines.append(" ".join(tmp))

	text = "\n".join(lines)		
	
	return text

import sys

try:
	from wikiparser import tell_me_about
	from display import message
except:
	print "Please Get The BLUG.in's Modules"

try:
	word = sys.argv[1]
except:
	word = raw_input("Please Enter A Word To Look Up")

entry = tell_me_about(word)

if entry:
	message("BDict - " + entry.title, format_text(entry.data))
else:
	message("Sorry","I do not know what %s means" % word)
