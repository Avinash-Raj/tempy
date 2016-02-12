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
    out_html_diag = ''
    i = 0
    for index, tag in tags_and_spaces:
        if index == i:
            out_html_diag += ',' + tag
        elif index < i:
            i = index
            out_html_diag += '|' + [i[1] for i in tags_and_spaces if i[0] < index][-1] + '->' + tag
        else:
            i = index
            out_html_diag += '->'  + tag

    print out_html_diag
    print tags_and_spaces


    '''After sorting'''
    tags_and_spaces = sorted(tags_and_spaces, key=lambda x: x[0])
    d = []
    for key, group in groupby(tags_and_spaces, lambda x: x[0]):
        d.append((key, [i[1] for i in group]))

    tag_only_html = ''
    previous_tag = ''
    for index, tags in d:
        print index
        for i,tag in enumerate(tags):
            if i == 0:
                out_tag = Helpers.extract_attributes(tag)
                previous_tag = re.sub(r'\.(.*)', r'(\1):', re.search(r'\{\[ (.*?) \]\}', out_tag).group(1))
                tag_only_html = out_tag
            elif re.search(re.escape(previous_tag) + '->'  + re.escape(tag), out_html_diag):
                print 'Direct child'
                tag_only_html.replace(previous_tag, tag)
            elif re.search(re.escape(previous_tag) + '->[^|]*->'  + re.escape(tag), out_html_diag):
                print 'Indirect Child'



    print tag_only_html


