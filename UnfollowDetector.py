#!/usr/bin/python

import sys, os, xml.dom.minidom, urllib, cPickle

# usage: ./UnfollowDetector.py screen_name=... out_file=...
def main(args):
	screenName = "0x17"
	dumpFilename = "TwitterFollowersDump"
	for arg in args:
		if(arg.startswith("screen_name=")):
			screenName = arg.split("=")[1]
		if(arg.startswith("out_file")):
			dumpFilename = arg.split("=")[1]
	
	if(os.path.exists(dumpFilename)):
		prevFollowers = loadFollowerIdsFromFile(dumpFilename)
		curFollowers = getFollowerIds(screenName)
		prevFollowers = filter(lambda id: not id in curFollowers, prevFollowers)
		if len(prevFollowers) == 0:
			print "Nobody unfollowed " + screenName
		else:
			print "Unfollowers (" + str(len(prevFollowers)) + "):"
			for unfollower in prevFollowers:
				print userIdToScreenName(unfollower)
	
	saveFollowerIdsToFile(screenName, dumpFilename)

def getFollowerIds(screenName):
	urlBase = "https://api.twitter.com/1/followers/ids.xml?cursor=-1&screen_name="
	f = urllib.urlopen(urlBase + screenName)
	dom = xml.dom.minidom.parseString(f.read())
	f.close()
	followerIds = map(lambda elem: elem.firstChild.nodeValue, dom.getElementsByTagName("id"))
	return followerIds

def userIdToScreenName(userId):
	print "Looking up: " + str(userId)
	try:
		url = "https://api.twitter.com/1/users/show.xml?user_id="+userId+"&include_entities=false"
		f = urllib.urlopen(url)
		dom = xml.dom.minidom.parseString(f.read())
		f.close()
		return dom.getElementsByTagName("screen_name")[0].firstChild.nodeValue
	except IndexError:
		return "Unknown"

def saveFollowerIdsToFile(screenName, filename):
	cPickle.dump(getFollowerIds(screenName), open(filename, "wb"))

def loadFollowerIdsFromFile(filename):
	return cPickle.load(open(filename, "rb"))

if __name__ == "__main__":
	main(sys.argv[1:])
