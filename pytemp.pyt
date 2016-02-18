'''
pytemplate
re.findall(r'(?=(?:^|\n) *(\w+(?:\([^)]*\))?:[\s\S]*?)(?=(?:^|\n)[^\n]*:))', s)
'''
#Hi ksjd
html(lang='en'):
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
                    '94'


