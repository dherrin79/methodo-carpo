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
			self.view.run_command('auto_complete', {
                'disable_auto_insert': True,
                'api_completions_only': True,
                'next_competion_if_showing': False
                })

			classDef = self.find_class_file(class_name)
			#print "Class definition: " + classDef
			methods = self.extract_class_methods(classDef)

			self.build_completions_list(methods)





	def get_class_name(self, obj_line, a_view):
		v = self.view # shorten call to self.view
		o_type = None
		print "obj_line: " + obj_line

		mcPatt = '\$(\w+)->'

		identifier = re.findall(mcPatt, obj_line)
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
				print "class_name is None"
				class_name = None
			print "Obj Instantiation: " + v.substr(rg)
		else:
			print "Object not instantiated!"
			class_name = None

		return class_name

	def find_class_file(self, class_name):
		fileName = ""
		v = self.view
		#Get the current directory
		fileDir = os.path.dirname(v.file_name())

		#Get the active view's file name
		fileName = os.path.basename(v.file_name())

		
		read_data = ""
		for fn in os.listdir(fileDir):
			fName, ext = os.path.splitext(fn)
			if ext == ".php":
				print class_name
				cfPatt = 'class ' + re.escape(class_name) + '\{'
				dir_len = fn.rfind('/')  # For OSX
				fileit = ""

				if dir_len > 0:
					fileit = fileDir + "\\" + fName + ext
				else:
					fileit = fileDir + "/" + fName + ext

				with open(fileit) as f:
					read_data = f.read()

				cl = re.search(cfPatt, read_data)
				
				if cl is not None:
					print "Class file located."
					return read_data
					
				else:
					print "Class File not located in " + fileDir

				
			elif ext == "":
				print "This is a directory: " + fn
			else:
				print "Other file types: " + fn

	def extract_class_methods(self, class_file):
		methods = []
		
		method_lines = re.findall('function.*|private.*|public.*|protected.*', class_file)
		comments = re.findall("/\*.*|//.*", class_file)
		

		for l in method_lines:
			
			if not "private" in l:
				s = re.search('(\w+)\s*\(.*\)(?=.*\{)', l)
				if s:
					methods.append(s.group().strip())
		
		#Remove Commented Methods		
		for c in comments:
			for m in methods:
				if m in c:
					methods.remove(m)

		return methods


	def build_completions_list(self, methods):
		meth= "not implemented"

		for m in methods:
			completions.append(m)
 




class methodgrabberCommand(sublime_plugin.EventListener):

	def on_query_completions(self, view, prefix, locations):
		comp_list = []

		for c in list(set(completions)):
			cs = c
			args = re.findall('\$\w+(?=\)|,)', cs)
			cnt = 1
			for a in args:
				b = a
				a = a.replace("$", "\$")
				snippet = "${" + str(cnt) + ":" + a + "}"
				cs = cs.replace(b, snippet)
				cnt = cnt + 1

			comp_list.append((c, cs))

		matches = []
		#print locations
		del completions[:]
		
		return sorted(comp_list)

