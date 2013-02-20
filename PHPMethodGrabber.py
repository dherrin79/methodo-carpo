import sublime, sublime_plugin
import re
import os

completions = []

class FindMethodsCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		print "run"
		sel = self.view.sel()[0]
		objIdentifier = self.view.word(sel.end()  -1)

		

		mcPatt = '\$(\w+)'

		line = self.view.line(sel)

		line = self.view.substr(line)
		lineCk = line
		line = line.strip()
		check = re.search(mcPatt, lineCk)

		


		class_name = ""
		if line.startswith("$"):
			a_view = self.view.substr(sublime.Region(0, self.view.size()))
			class_name = self.get_class_name(line,a_view)


		if not class_name:
			self.view.insert(edit, sel.end() , ".")
		else:
			self.view.insert(edit, sel.begin() , "->")

			#UGLY!!! Work around for having to pres ".."
			lineR = self.view.line(sel)
			line = self.view.substr(lineR)
			first_arrow = re.findall("->", line)
			if len(first_arrow) > 1:
				lineR = self.view.line(sel)
				line = line.replace("->->", "->")
				self.view.replace(edit, lineR, line)

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

		mcPatt = '\$(\w+)'

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

	def walk(self, dir_name, cfPatt):
		print dir_name
		for (path, dirs, files) in os.walk(dir_name):
			for fil in files:
				fn, ext = os.path.splitext(fil)
				if ext == ".php":
					with open(os.path.join(path, fil)) as f:
						read_data = f.read()
						cl = re.search(cfPatt, read_data)
						if cl:
							return read_data
						else:
							return False

	def find_class_file(self, class_name):
		print "find_class_file"
		fileName = ""
		v = self.view
		#Step 1:Check active file for Class
		a_view = v.substr(sublime.Region(0, self.view.size()))
		cfPatt = 'class\s*' + re.escape(class_name) + '\{[\s\S]+\}'
		
		clnm = re.search(cfPatt, a_view)
		if clnm is not None:
			print "Class file found"
			return clnm.group()

		#Step 2: Check current directory
		curr_dir = os.path.dirname(v.file_name())
		for php in os.listdir(curr_dir):
			fn, ext = os.path.splitext(php)
			if ext == ".php":
				with open(os.path.join(curr_dir, php)) as f:
					read_data = f.read()
					cl = re.search(cfPatt, read_data)
					if cl:
						return read_data

		
		#Step 2: Check PHP includes paths
		inclPatt = 'include\s*"(\S+?)";'
		stepUp = '\.\./'

		foldPatt = '(\w+)/'
		
		clPath = re.findall(inclPatt, a_view)
		
		if len(clPath) > 0:
			print "Include found."
			for i in clPath:

				#Check for '/'
				if i.startswith("/"):
					
					folders = re.findall(foldPatt, i)
					
					fCnt = 0
					d = os.path.dirname(v.file_name())
					for g in folders:
						
						d = os.path.join(d, folders[fCnt])
						fCnt = fCnt + 1

					for php in os.listdir(d):
						fn, ext = os.path.splitext(php)
						if ext == ".php":
							with open(os.path.join(d, php)) as f:
								read_data = f.read()
								cl = re.search(cfPatt, read_data)
								if cl:
									return read_data
				
				#Check for '../'
				if i.startswith("../"):
					pardir = re.findall(stepUp, i)
					
					newDir = ""
					rec_dir = os.path.dirname(v.file_name())
					if len(pardir) > 0:
						cnt = 0
						for p in pardir:
							head, tail = os.path.split(rec_dir)
							newDir = head
							cnt = cnt + 1
							
							rec_dir = head
						print newDir
						fCnt = 0
						d = newDir
						folders = re.findall(foldPatt, i)
						for g in folders:
							d = os.path.join(d, folders[fCnt])
							fCnt = fCnt + 1

						for php in os.listdir(d):
							fn, ext = os.path.splitext(php)
							if ext == ".php":
								with open(os.path.join(d, php)) as f:
									read_data = f.read()
									cl = re.search(cfPatt, read_data)
									if cl:
										return read_data

		#Step 3: Check .sublime-project paths

		fileDir = os.path.dirname(v.file_name())
		rec_fileDir = fileDir
		projectFilePath= ""
		foundPrjFile = False
		while not foundPrjFile:
			for (path, dirs, files) in os.walk(rec_fileDir):
				for fil in files:
					
					fn, ex = os.path.splitext(fil)
					if ex == '.sublime-project':
						
						projectFilePath = path
						foundPrjFile = True

				
			head, tail = os.path.split(fileDir)
			rec_fileDir = head
			

		print "Project File: " + projectFilePath
		projFilePath = os.path.dirname(projectFilePath)
		
		#Get the active view's file name
		fileName = os.path.basename(v.file_name())

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
			return True

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


