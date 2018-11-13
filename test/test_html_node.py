import sys
sys.path.append('../src')

from html_parser import HTMLParser

def main():
    raw_text = """
    <!DOCTYPE html>
    <html>

    <head>
        <title>Hello</title>
    </head>

    <body>
        <p>Hello, World!</p>
    </body>

    </html>
    """

    parser = HTMLParser()
    parser.LoadRawText(raw_text)
    parser.Parse()

if __name__ == '__main__':
    main()

    