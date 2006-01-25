#! /usr/bin/python
#
#      Wikiparser.py version 0.0.1
#         (c) 2005 Tejas Dinkar
#
#	Insert GPL Here
#


user_agent = "Wikiparser - by BLUG.in"


class wikipedia_entry:
	'''This is an Object which will contain all useful data
	The Data can be easily gotten by simply saying: obj.title ...'''
	
	def __init__(self, title = "", data = "", time = "",error = 0):
		self.error = error
		self.title = title
		self.data = data
		self.time = time
		
	def modify(self, title = None, data = None, time = None, error = None):
		'''This Lets you Modify This Object'''
		if title != None: self.title = title
		if data != None: self.data = data
		if time != None: self.time = time
		if error != None: self.error = time
	
	def __nonzero__(self):
		'''This is a Function you would use to determine a valid obj'''
		if self.error: 
			return False
		elif self.title:
			return True
		else:
			return False
	
	def __repr__(self):
		'''This is just a bit of eye candy'''
		return "<A Wikipedia Article about %s>" % self.title


def get_wiki_entry(item, modify_title = 1):
	'''This is a Function that Gets Data from Wikipedia and Returns it
	In the Form of an instance of class wikipedia_entry.'''
	
	import urllib2
	
	# This Next Block Makes the item in Wikimedia format... ex: Main_Page
	# But only if it is allowed
	if modify_title:
		item = item.title()
	item = item.replace(" ","_")
	
	
	# This sets the URL where the wikipedia entry is found
	url = 'http://en.wikipedia.org/wiki/Special:Export/' + item
	
	request = urllib2.Request(url)
	opener = urllib2.build_opener()
	
	# This next one sets a custom header so that wikipedia doesn't reject
	request.add_header('User-Agent',user_agent)

	# This Next Line Gets the XML Document into a File-Like Object
	xmlfile = opener.open(request)
	
	# The Next Line Translates the XML Document into a Wikipedia Entry
	# By OutSourcing it to the Function translate_xmldoc
	entry = translate_xml(xmlfile)
	
	# This sends the Entry Back
	return entry


def translate_xml(xmlfile):
	'''This Translates the XML Document'''
	
	# These next two lines parse the xmlfile to get an xml document
	from xml.dom import minidom
	xmldoc = minidom.parse(xmlfile)
	
	# The Two Block gets various Data Elements from the XML document
	# To Understand these next two blocks, you must know the heirarchy
	# of how data is stored in wikipedia.
	# Check Out http://en.wikipedia.org/wiki/Special:Export/Main_Page
	# for a good Idea of what it looks like
	
	# The try, except is for pages that are not there
	try:
		page = xmldoc.getElementsByTagName("page")[0]
		revision = page.getElementsByTagName("revision")[0]
	except IndexError:
		return wikipedia_entry(error = 1)
	
	title = page.getElementsByTagName("title")[0].firstChild.data
	data = revision.getElementsByTagName("text")[0].firstChild.data
	date = page.getElementsByTagName("timestamp")[0].firstChild.data
	
	# This Next Line Creates a wikipedia entry
	entry = wikipedia_entry(title,data,date)
	
	# Go Back to Whence you came from
	return entry


def follow_redirect(entry):
	'''This Function Follows Redirects if wikipedia throws them at you'''
	
	# Next Line Check for A Redirect
	if entry.data.startswith("#REDIRECT"):
		# This gets the destination of redirect
		item = entry.data.split("[[")[-1].split("]]")[0]
		
		# This follows the redirect
		entry = get_wiki_entry(item,modify_title = 0)
		
		# Recursion
		entry = follow_redirect(entry)
		
	return entry
	

def tell_me_about(item):
	'''This is the Nicest User Inteface you can Define! Just tell me
	what to Look For, and it will search, and follow Redirects, if asked'''
	
	# This Block gets wiki item
	entry = get_wiki_entry(item)
	
	# This Block Follows all Redirects
	if entry:
		entry = follow_redirect(entry)
		
	# This returns entry, or an error Message	
	if entry:
		return entry
	else:
		return wikipedia_entry(title = "Sorry", 
			data = "That Page Wasn't Found", error = 1)
	

# The Next Block of Code is only for Testing Purposes
if __name__ == '__main__':
	item = raw_input("What Article Do You Want to Learn About? ")
	entry = tell_me_about(item)
	if entry:
		print "Page Found"
	else:
		print "Sorry, That Page Was Not Found"
	print entry.title
	print entry.data
	print entry.time
