'''
pytemplate parser which converts python like code to html
'''
import re
from itertools import groupby

if __name__ == '__main__' and __package__ is None:
    from os import sys, path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Helpers.helpers import ParseHelper

file_name = sys.argv[1]


def find_tag_content(tags, lis):
    l = {}
    for tag in tags:
        for index, ta in enumerate(lis):
            converted_tag = re.sub(r'\.(.*)', r'(\1)', tag)
            if ta.endswith(converted_tag + ':'):
                content = ParseHelper.remove_quotes(lis[index + 1])
                l.update({tag: content})
                break

    return l


with open(file_name) as fil:
    temp_file = fil.read()
    temp_file = re.sub('#.*\n?', '', temp_file)
    temp_file = temp_file.replace('"', "'")
    temp_file = re.sub(r"(?m)^'''[\s\S]*?'''", '', temp_file)
    temp_file = re.sub(r'(?m)^[ \t]+$\n?', '', temp_file)
    temp_file = re.sub(r'\n\n+', '\n', temp_file)
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

    #print tag_seperation
    tags = [i for i in tag_seperation if i.endswith(':')]
    tags_and_spaces = []
    for tag in tags:
        tags_and_spaces.extend(re.findall(r'^(\s*)(.*)', tag))

    tags_and_spaces = [(len(i[0]), i[1]) for i in tags_and_spaces]
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
            out_html_diag += '->' + tag

    # print tag_seperation
    print out_html_diag
    #print tags_and_spaces
    tags_in_same_depth = [(key, [i[1] for i in group]) for key, group in
                          groupby(sorted(tags_and_spaces, key=lambda x: x[0]), lambda x: x[0])][::-1]

    '''Finding the parent tags'''
    ptag_tag = []
    for index, tags in tags_in_same_depth:

        for tag in tags:
            ptag_tag.append((ParseHelper.find_parent(tag, out_html_diag), tag, index))
    # Main change
    tags_having_common_parent = [(key, [str(i[2]) + i[1] for i in group]) for key, group in groupby(ptag_tag, lambda x: x[0])]
    tags_having_common_parent_with_spaces = [(i[1], i[2]) for key, group in groupby(ptag_tag, lambda x: x[0]) for i in group]
    #print tags_having_common_parent_with_spaces

    '''Building the final html'''
    final_html_dict = {}
    for parent, tags in tags_having_common_parent[:-1]:
        final_html = ''
        for tag in tags:
            final_html += ParseHelper.extract_attributes(tag)
        if parent:
            parent_html = ParseHelper.extract_attributes(parent)
            final_html = re.sub(r'\{\[ .*? \]\}', final_html, parent_html)
            final_html_dict[parent] = final_html

    tags_in_same_depth_r = tags_in_same_depth[::-1]
    root_tag = tags_in_same_depth_r[0][1][0]
    root_html = final_html_dict[root_tag]

    final_result = re.sub(r'\{\[ (.*?) \]\}', lambda m: final_html_dict[m.group(1) + ':'], root_html)

    remove_redundant_tags = re.sub(r'(\n? *)<(\w[^>]*)>\s*<\2>', r'\1<\2>', final_result)
    remove_redundant_tags = re.sub(r'(\n?) *<(/\w[^>]*)>(\s*)<\2>', r'\1\3<\2>', remove_redundant_tags)

    remove_redundant_tags = re.sub(r'\n\n+', r'\n', remove_redundant_tags)
    remaining_tags = re.findall(r'\{\[ (.*?) \]\}', remove_redundant_tags)
    tag_contents = find_tag_content(remaining_tags, tag_seperation)

    resultant_html = re.sub(r'\{\[ (.*?) \]\}', lambda m: tag_contents[m.group(1)], remove_redundant_tags)
    #print resultant_html

