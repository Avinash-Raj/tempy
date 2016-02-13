import re

class Helpers:
	

	def __init__(self):
		pass

	@classmethod
	def build_tag(*args):
		if len(args) > 2:
			x, tag, argumnets = args
			splitted_args = re.split(r"\s*,\s*(?=\w+='.*?')", argumnets)
			if len(splitted_args) == 1:
				return '<' + tag + ' '  + splitted_args[0] + '>\n' + '{[ ' + tag + '.' + splitted_args[0] + ' ]}' + '\n</' + tag + '>\n'
			return '<' + tag + ' ' + ' '.join(splitted_args) + '>\n' + '{[ ' + tag + '.' + ','.join(splitted_args) + ' ]}' + '\n</' + tag + '>\n'

		return '<' + args[1] + '>\n' + '{[ ' + args[1] + ' ]}' + '\n</' + args[1] + '>\n'

	@classmethod
	def extract_attributes(cls, st):
		if st.endswith('):'):
			tag, arguments = re.findall(r'^(\w+)\((.+?)\):', st)[0]
			return cls.build_tag(tag, arguments)
		else:
			return cls.build_tag(st.rstrip(':'))

	@classmethod
	def find_parent(cls, tag, diag):
		m = re.search(r'(\w+(?:\([^()]*\))?:)->(?:(?!->|\|).)*' + re.escape(tag), diag)
		if m:
			return m.group(1)
		return None
