import re

s = """html(lang='en'):
    head:
        title:
            "Hi , How are you?"
        script(type='text/javascript'):
            '''if (foo) {
                bar(1 + 5)
             }'''
    body:
        h1:
            'Pytemplate - template engine'
        table(style='width:100%'):
            tr:
                td:
                    'Jill'
                td:
                    'Smith'
                td:
                    '50'
            tr:
                td:
                    'Eve'
                td:
                    'Jackson'
                td:
                    '94'"""

def build_tag(tag, arguments):
    splitted_args = re.split(r"\s*,\s*(?=\w+='.*?')", arguments)
    if len(splitted_args) == 1:
        return  '<' + tag + ' ' + splitted_args[0] + '>\n' + '{[ ' + tag + '.' + splitted_args[
                    0] + ' ]}' + '\n' + '</' + tag + '>\n'
    return  '<' + tag + ' ' + ' '.join(splitted_args) + '>\n' + '{[ ' + tag + '.' + ','.join(
                splitted_args) + ' ]}' + '\n' + '</' + tag + '>\n'

def extract_attributes(st):
    if st.endswith('):'):
        tag, arguments = re.findall(r'^(\w+)\((.+?)\):', st)[0]
        return build_tag(tag, arguments)
    st = st.rstrip(':')
    return '<' + st + '>\n{[ ' + st + ' ]}\n</' + st + '>'


def parse(string):
    lis = re.findall(r'(?=(?:^|\n) *(\w+(?:\([^)]*\))?:[\s\S]*?)(?=(?:^|\n)[^\n]*:|(?s)$))', s)
    html = ''
    tags = []
    tags_with_contents = []
    other = []
    for item in lis:
        if item.endswith(':'):
            tags.append(item)
            tag_html = extract_attributes(item)
            if html == '':
                html = tag_html
            else:
                html = re.sub(r'\{\[ .*? \]\}', tag_html, html)

        elif re.search(r'(?s)[\'"]$', item):
            tags_with_contents.append(item)
            tag, content = re.split(':', item, 1)
            tag = tag + ':'
            tag_html = extract_attributes(tag)
            if html == '':
                html = tag_html
            else:
                html = re.sub(r'\{\[ .*? \]\}', tag_html, html)
            html = re.sub(r'\{\[ .*? \]\}(\s*\n\s*</\w+>)', content + r'\1' + '\n{[ tag ]}\n', html)
        else:
            other.append(item)

    print html



parse(s)