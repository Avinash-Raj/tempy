import re


class ParseHelper:
    def __init__(self):
        pass

    @classmethod
    def build_tag(*args):
        if len(args) > 2:
            x, tags, argumnets = args
            space = 0
            tag = ''
            if re.findall(r'^(\d+)(.+)', tags):
                space, tag = re.findall(r'^(\d+)(.+)', tags)[0]
            else:
                space = 0
                tag = tags
            space = int(space)
            splitted_args = re.split(r"\s*,\s*(?=\w+='.*?')", argumnets)
            if len(splitted_args) == 1:
                return ' ' * space + '<' + tag + ' ' + splitted_args[0] + '>\n' + '{[ ' + tag + '.' + splitted_args[
                    0] + ' ]}' + '\n' + ' ' * space + '</' + tag + '>\n'
            return ' ' * space + '<' + tag + ' ' + ' '.join(splitted_args) + '>\n' + '{[ ' + tag + '.' + ','.join(
                splitted_args) + ' ]}' + '\n' + ' ' * space + '</' + tag + '>\n'

        if re.findall(r'^(\d+)(.+)', args[1]):
            space, tag = re.findall(r'^(\d+)(.+)', args[1])[0]
            space = int(space)
            return ' ' * space + '<' + tag + '>\n' + '{[ ' + tag + ' ]}' + '\n' + ' ' * space + '</' + tag + '>\n'

        return '<' + args[1] + '>\n' + '{[ ' + args[1] + ' ]}' + '\n' + ' ' + '</' + args[1] + '>\n'

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

    @classmethod
    def remove_quotes(cls, content):
        cont = re.sub(r'(?s)^(\s*)(\'\'\'|"""|[\'"])(.*?[^\\])\2\s*$', r'\1\3', content)
        return cont
