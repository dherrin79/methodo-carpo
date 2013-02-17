import sublime, sublime_plugin
import re
import os



class methodgrabberCommand(sublime_plugin.EventListener):

	

	def on_query_completions(self, view, prefix, locations):
		mg = methodgrabberCommand
		phpVariable = False
		words = set()
		#Get the Current Directory
		fileDir = os.path.dirname(view.file_name())
		
		#Get the Active Views File Name
		fileName= os.path.basename(view.file_name())
		
		phpfiles = []

		
		#Only build list if defining/typing a variable
		if view.substr(locations[0] - 2) == ">" and view.substr(locations[0] - 3) == "-":
			phpVariable = True

		line =  view.line(locations[0])

		lineStr = view.substr(line)
		#print lineStr

		str = lineStr.strip()

		

		if str.startswith('$'):
			print str
			if "->" in str:
				print "str contains the characters: ->"
			else:
				print "str is not object"
		else:
			print "Not a Variable"
		

		#Build a list of all the php files in directory where active file resides.
		if phpVariable == True:
			for fn in os.listdir(fileDir):

				fName, ext = os.path.splitext(fn)
			
				if ext == ".php" and fn != fileName:
					phpfiles.append(fn)

		phpfiles = set(phpfiles)

		words.update(phpfiles)

		matches = [(f,f) for f in words]
		#print locations

		
		return matches

