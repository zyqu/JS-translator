#!/usr/bin/python

import os, sys, time, re

PROJ_DIR = os.path.abspath(os.path.dirname(__file__))
JS_DIR = os.path.join(PROJ_DIR, "nodejs_parser")

filter_re = re.compile("\{.*?\}")

SSA_NAME = "ssa"
SSA_EXT = ".%s"%SSA_NAME

def sanity_txt(txt):
	txt = txt.replace('"',"'")
	txt = filter_re.sub('', txt)
	return txt 

def translate(fromtext, fromlang, newlang):
	os.chdir(JS_DIR)
	to_txt = os.popen("casperjs --ignore-ssl-errors=yes translate.js --text=\"%s\" --source=\"%s\" --target=\"%s\""%(fromtext, fromlang, newlang)).read().strip()
	os.chdir(PROJ_DIR)
	if to_txt != "ERROR":
		return to_txt
	else:
		return fromtext
	

def ssa_file(filepath, fromlang, newlang):
	if os.path.isfile(filepath) == False:
		print "%s not exist"%filepath
		exit(-1)

	orig_obj = open(filepath, 'r')
	newfilepath = filepath.replace(SSA_EXT, "") + "_%s%s"%(newlang, SSA_EXT)
	if os.path.isfile(newfilepath):
		os.system("rm %s"%newfilepath)
	new_obj = open(newfilepath, 'w')
	isEventStart = False
	num_tokens = -1
	for l in orig_obj.readlines():
		l = l.strip()
		newline = l+"\n"
		if l=="[Events]":
			isEventStart = True
		elif isEventStart and l.find(":")>0:
			tokens = l.split(',')
			if l.startswith("Format:"):
				num_tokens = len(tokens)
			else:
				if num_tokens < 0:
					continue
				else:
					if len(tokens) > num_tokens - 1:
						diag_txt = ",".join(tokens[num_tokens - 1:])
						diag_txt = sanity_txt(diag_txt)
						to_txt = translate(diag_txt, fromlang, newlang)
						newline = ",".join(tokens[:num_tokens - 1])+",%s\n"%to_txt
		new_obj.write(newline)
	orig_obj.close()
	new_obj.close()

if __name__=="__main__":
	if len(sys.argv) != 5:
		print "python subtitle_translate.py [format] [filepath] [from-lang] [new-lang]"
		exit(-1)
	format = sys.argv[1]
	filepath = sys.argv[2]
	fromlang = sys.argv[3]
	newlang = sys.argv[4]
	if format == SSA_NAME:
		ssa_file(filepath, fromlang, newlang)
	