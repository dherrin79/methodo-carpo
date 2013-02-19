import sublime, sublime_plugin
import re
import os

completions = []

class FindMethodsCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		print "run"
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
			print "Line: " + line

			#UGLY!!! Work around for having to pres ".."
			lineR = self.view.line(sel)
			line = self.view.substr(lineR)
			first_arrow = re.findall("->", line)
			if len(first_arrow) > 1:
				lineR = self.view.line(sel)
				line = line.replace("->->", "->")
				self.view.replace(edit, lineR, line)


			print "Class name: " + class_name
			classDef = self.find_class_file(class_name)
			#print "Class definition: " + classDef
			methods = self.extract_class_methods(classDef)

			if self.build_completions_list(methods):
				self.view.run_command('auto_complete', {
                'disable_auto_insert': True,
                'api_completions_only': True,
                'next_competion_if_showing': False
                })
			else:
				f = ""

	def get_class_name(self, obj_line, a_view):
		print "get_class_name"
		v = self.view # shorten call to self.view

		mcPatt = '\$(\w+)->'

		identifier = re.findall(mcPatt, obj_line)
		identifier = identifier[0]

		oiPatt = '\$(' + re.escape(identifier) + ')\s*=\s*new\s*(\w+)\(\)'

		if v.find_all(oiPatt):
			rg = v.find_all(oiPatt)[0]
			clPatt = '\$\w+\s*=\s*new\s*(\w+)\(\)'
			objInts = v.substr(rg)
			class_name = re.search('\$(' + re.escape(identifier) + ')\s*=\s*new\s*(\w+)\(\)' , objInts)
			if class_name is not None:
				class_name = class_name.group(2)
			else:
				
				class_name = None
			
			return class_name
		else:
			
			class_name = None

		return class_name

	def find_class_file(self, class_name):
		print "find_class_file"
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
				
				cfPatt = 'class ' + re.escape(class_name) + '\{*'
				dir_len = fn.rfind('/')  # For OSX
				fileit = ""

				if dir_len > 0:
					fileit = fileDir + "\\" + fName + ext
				else:
					fileit = fileDir + "/" + fName + ext

				with open(fileit, 'r') as f:
					read_data = f.read()

				cl = re.search(cfPatt, read_data)

				if cl is not None:
					return read_data

	def extract_class_methods(self, class_file):
		print "extract_class_methods"
		methods = []

		method_lines = re.findall('function.*|private.*|public.*|protected.*', class_file)
		comments = re.findall("/\*.*|//.*", class_file)

		for l in method_lines:
			if not "private" in l:
				s = re.search('(\w+)\s*\(.*\)(?=.*\{*)', l)
				if s:
					methods.append(s.group().strip())

		#Remove Commented Methods		
		for c in comments:
			for m in methods:
				if m in c:
					methods.remove(m)

		return methods


	def build_completions_list(self, methods):
		print "build_completions_list"
		meth= "not implemented"

		for m in methods:
			completions.append(m)

		if methods:
			print "true"
			return True

		print "false"
		return False
 




class MethodGrabberComplete(sublime_plugin.EventListener):

	def on_query_completions(self, view, prefix, locations):
		print "on_query_completions"
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
			
		del completions[:]

		return sorted(comp_list)


