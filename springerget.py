#!/usr/bin/python
# springerget.py
# DO NOT USE THIS SCRIPT TO HARM COPYRIGHT 'N STUFF. Also: THE GAME.
# copyleft by 0x17
# inb4 "chmod u+x springerget.py" as usual
# usage: ./springerget.py "urlToBookOverview"
# do not omit ticks!

import re, sys, os, subprocess

def system(cmd):
	return subprocess.call(cmd.split(" "))
	
def wgetMe(url):
	subprocess.call(["wget", "-U", "\"" + fakeUserAgent + "\"", url])

# this is neccessary because otherwise we get 403's...
fakeUserAgent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5"

# make sure index.html doesn't already exist
if os.path.exists("index.html"):
	system("rm index.html")

# download overview page html-file
#system("wget -U \"" + fakeUserAgent + "\" " + sys.argv[1])
wgetMe(sys.argv[1])

# look for url listing
p = re.compile("documentPdfDownloadUrls : \[..*\]")

try:
	f = open("index.html", "r")
except IOError:
	print("index.html not there!")
	sys.exit(1)

m = p.search(f.read())

if m:
	arrayStr = m.group().replace("documentPdfDownloadUrls : ", "")
	# make python list out of url listing
	expr = arrayStr;
	x = eval(expr)
	# download each pdf url
	for u in x:
		if u == '':
			continue
		else:
			wgetMe("http://www.springerlink.com" + u)
else:
	print("Can't match pdf urls! U mad?")
	sys.exit(1)
	
# cleanup for this step
f.close()
system("rm index.html")

# build python list out of list of filenames
fns = ['front-matter.pdf']

for fn in sorted(os.listdir(".")):
	if fn.startswith("fulltext"):
		fns.append(fn)

fns.append('back-matter.pdf')

# yea actually this really looks like I did something wrong
# in my logic.
fnstr = ""
for fn in fns:
	fnstr += (fn + " ")

# merge with ghostscript
gsBase = "gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=finished.pdf "
os.system(gsBase + fnstr)

# cleanup
#system("rm front-matter.pdf back-matter.pdf")
os.system("rm "  + fnstr)

