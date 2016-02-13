'''
pytemplate parser which converts python like code to html
'''
import re
from itertools import groupby
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from tempy.helpers import Helpers

file_name = sys.argv[1]

def find_tag_content(tags, lis):
    l = {}
    for tag in tags:
        for index, ta in enumerate(lis):
            converted_tag = re.sub(r'\.(.*)',r'(\1)' , tag)
            if ta.endswith(converted_tag + ':'):
                l.update({tag: lis[index+1]})
                break

    return l

with open(file_name) as fil:
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

    # print tag_seperation
    # print out_html_diag
    
    tags_in_same_depth =  [(key, [i[1] for i in group]) for key, group in groupby(sorted(tags_and_spaces, key=lambda x: x[0]), lambda x: x[0])][::-1]
    


    '''Finding the parent tags'''
    ptag_tag = []
    for index, tags in tags_in_same_depth:
        
        for tag in tags:
            ptag_tag.append((Helpers.find_parent(tag, out_html_diag), tag))

    # print ptag_tag
    tags_having_common_parent = [(key, [i[1] for i in group]) for key, group in groupby(ptag_tag, lambda x: x[0])]
    #print tags_having_common_parent

    '''Building the final html'''
    final_html_dict = {}
    for parent, tags in tags_having_common_parent[:-1]:
        final_html = ''
        for tag in tags:
            final_html += Helpers.extract_attributes(tag)
        if parent:
            parent_html = Helpers.extract_attributes(parent)
            final_html = re.sub(r'\{\[ .*? \]\}', final_html, parent_html)
            final_html_dict[parent] = final_html

    #print final_html_dict
    tags_in_same_depth_r = tags_in_same_depth[::-1]
    root_tag = tags_in_same_depth_r[0][1][0]
    root_html = final_html_dict[root_tag]

    final_result = re.sub(r'\{\[ (.*?) \]\}', lambda m: final_html_dict[m.group(1) + ':'], root_html)
    remove_redundant_tags = re.sub(r'<(/?\w[^>]*)>\s*<\1>', r'<\1>', final_result)

    #print remove_redundant_tags
    remaining_tags = re.findall(r'\{\[ (.*?) \]\}', remove_redundant_tags)
    tag_contents = find_tag_content(remaining_tags, tag_seperation)

    resultant_html = re.sub(r'\{\[ (.*?) \]\}', lambda m: tag_contents[m.group(1)], remove_redundant_tags)

    print resultant_html
