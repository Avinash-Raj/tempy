# tempy
Parser which converts python templating file to it's corresponding html file. It's exactly similar to [Jade](http://jade-lang.com/)
but for the one who loves python's indentation.

First you need to create a `.pyt` file which looks like a regular python file.

## A sample `pyt` looks like below.

```Python
'''
tempy -> Python template file.
'''

html(lang='en'):
    head:
        title:
            "Hi , How are you?"
        script(type='text/javascript'):
            if (foo) {
                bar(1 + 5)
             }
    body:
        h1:
            'Pytemplate - template engine'
```

From the above file you may able to find out all the relationships of a particular tag. Lets take, `body` tag. Parent of this tag is 
`html` and the brother of this tag is `head`. It has one child tag called `h1`.





