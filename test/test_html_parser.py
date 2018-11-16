from os.path import abspath
import sys

"""
Use os to get the absoulte path

Use sys.path.insert() instead of sys.path.append().
Because python checks in the directories in sequential order 
starting at the first directory in `sys.path` list, till find 
the `.py`.

But I don't know which is better between sys.path.insert(0) and sys.path.insert(1)
the following hyperlink is the issue
http://codewenda.com/%E4%B8%BA%E4%BB%80%E4%B9%88%E4%BD%BF%E7%94%A8sys-path-append%EF%BC%88%E8%B7%AF%E5%BE%84%EF%BC%89%E8%80%8C%E4%B8%8D%E6%98%AFsys-path-insert%EF%BC%881%EF%BC%8C%E8%B7%AF%E5%BE%84%EF%BC%89%EF%BC%9F/
"""

sys.path.insert(0, abspath('../src'))

from html_parser import HTMLParser

def main():
    raw_text = r"""
    <!-- hello, world --    >
    <head  >
    <div class="my_class1 my_class2" data-intent="jquery-data">Hello, World 1</div>
    <p class="my_class1 my_class2" data-intent="jquery-data"> outside <b>Hello, World 2</b></p>
    </head>
    """

    parser = HTMLParser()
    parser.load_text(raw_text)
    parser.run()
    parser.root.vardump()

if __name__ == '__main__':
    main()

    