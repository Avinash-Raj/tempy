'''
pytemplate parser result in html
'''
import re
with open('/home/gemini/Desktop/f.py') as fil:
    temp_file = fil.read()
    temp_file = re.sub('#.*\n?', '', temp_file)
    temp_file = temp_file.replace('"', "'")
    temp_file = re.sub(r"(?m)^\s*'''[\s\S]*?'''", '', temp_file)
    temp_file = re.sub(r'(?m)^[ \t]+$\n?', '', temp_file)
    temp_file = re.sub(r'\n\n+', '\n', temp_file)
    tags = []
    code = re.split('(?<=:)\n', temp_file)
    tag_seperation = []
    for line in code:
    	if line.endswith(':'):
    		out = re.split(r'\n(?=\s*\w+(?:\(.*?\))?:$)', line)
    		if len(out) == 1:
    			tag_seperation.append(out[0])
    		else:
    			for i in out:
    			    tag_seperation.append(i)
    	else:
    		tag_seperation.append(line)
    print tag_seperation


