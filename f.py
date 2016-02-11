'''
pytemplate
'''
#Hi ksjd
html(lang='en'):
    head:
        title = "Hi , How are you?"
        script(type='text/javascript'):
            if (foo) {
                bar(1 + 5)
             }
    body:
        h1 = 'Pytemplate - template engine'
