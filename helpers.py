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
				return '<' + tag + ' '  + splitted_args[0] + '>' + '{[ ' + tag + '.' + splitted_args[0] + ' ]}' + '</' + tag + '>'
			return '<' + tag + ' ' + ' '.join(splitted_args) + '>' + '{[ ' + tag + '.' + ','.join(splitted_args) + ' ]}' + '</' + tag + '>'

		return '<' + args[1] + '>' + '{[ ' + args[1] + ' ]}' + '</' + args[1] + '>'

	@classmethod
	def extract_attributes(cls, st):
		if st.endswith('):'):
			tag, arguments = re.findall(r'^(\w+)\((.+?)\):', st)[0]
			return cls.build_tag(tag, arguments)
		else:
			return cls.build_tag(st.rstrip(':'))
