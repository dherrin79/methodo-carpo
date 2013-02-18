import sublime, sublime_plugin
import re
import os

completions = []

class FindMethodsCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		sel = self.view.sel()[0]
		objIdentifier = self.view.word(sel.end()  -1)

		self.view.insert(edit, sel.begin() , "->")
		line = self.view.line(sel)

		line = self.view.substr(line).strip()
		class_name = ""
		if line.startswith("$"):
			a_view = self.view.substr(sublime.Region(0, self.view.size()))
			class_name = self.get_class_name(line,a_view)

		if not class_name:
			self.view.insert(edit, sel.begin() + 2, "Error: Identifier has not been declared!")
		else:
			self.find_class_file(class_name)



	def get_class_name(self, obj_line, a_view):
		v = self.view # shorten call to self.view
		o_type = None
		print "obj_line: " + obj_line

		mcPatt = '\$(\w+)->'

		identifier = re.findall(mcPatt, a_view)
		identifier = identifier[0]
		print "Ide: " + identifier

		oiPatt = '\$(' + re.escape(identifier) + ')\s*=\s*new\s*(\w+)\(\)'

		if v.find_all(oiPatt):
			rg = v.find_all(oiPatt)[0]
			clPatt = '\$\w+\s*=\s*new\s*(\w+)\(\)'
			objInts = v.substr(rg)
			print "Stupid: " + objInts
			class_name = re.search('\$(' + re.escape(identifier) + ')\s*=\s*new\s*(\w+)\(\)' , objInts)
			if class_name is not None:
				class_name = class_name.group(2)
			else:
				print "class_name is NoNe"
				class_name = None
			print "Obj Instantiation: " + v.substr(rg)
		else:
			print "Object not instantiated!"
			class_name = None

		return class_name

	def find_class_file(class_name):
		fileName = ""


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
			if "->" in str or ".." in str: #In the future replace ".."" with user settings for possible user snippet tabTriggers.  For example, I have a snippet that uses .. to create the -> for calling php methods.
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

