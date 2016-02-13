# tempy
Parser which converts python templating file to it's corresponding html file. It's exactly similar to [Jade](http://jade-lang.com/)
but for the one who loves python's indentation.

First you need to create a `.pyt` file which looks like a regular python file.

#### A sample `pyt` looks like below.

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
`html`, brother `head` and a child tag called `h1`.


### How to run?

1. Clone or download this repository. 
2. Move into the cloned `tempy` folder from terminal.
3. Then run the below command.

```bash
$ python src/parser.py pytemp.pyt > ~/Desktop/out.html
```
Resultant `out.html` file is stored on your desktop. Note that you may store `.pyt` file anywhere but you need to call that file by specifying it's full path. And also you may change the destination file path.
