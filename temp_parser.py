'''
pytemplate parser result in html
'''
import re
from itertools import groupby
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from tempy.helpers import Helpers


with open('/home/gemini/projects/tempy/f.py') as fil:
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

    tags = [i for i in tag_seperation if i.endswith(':')]
    tags_and_spaces = []
    for tag in tags:
        tags_and_spaces.extend(re.findall(r'^(\s*)(.*)', tag))

    tags_and_spaces = [(len(i[0]),i[1]) for i in tags_and_spaces]
    out_html = ''
    i = 0
    for index, tag in tags_and_spaces:
        if index == i:
            out_html += ',' + tag
        elif index < i:
            i = index
            out_html += '|' + [i[1] for i in tags_and_spaces if i[0] < index][-1] + '->' + tag
        else:
            i = index
            out_html += '->'  + tag

    print out_html


    '''After sorting'''
    tags_and_spaces = sorted(tags_and_spaces, key=lambda x: x[0])
    d = []
    for key, group in groupby(tags_and_spaces, lambda x: x[0]):
        d.append((key, [i[1] for i in group]))

    tag_only_html = ''
    num = 0
    for index, tags in d:
        print index
        for tag in tags:
            print Helpers.extract_attributes(tag)


