import sys
sys.path.append('../src')

from html_parser import HTMLParser

def main():
    raw_text = r"""
    <!-- hello, world --    >
    <div class="my_class1 my_class2" data-intent="hello">
    </head>
    """

    parser = HTMLParser()
    parser.load_text(raw_text)
    parser.run()

if __name__ == '__main__':
    main()

    