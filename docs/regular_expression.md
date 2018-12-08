
# Useful Regular Expression
copy part of code from https://github.com/python/cpython/blob/3.7/Lib/html/parser.py
the standar is too complex to learn, so I write a simple regular rule.
the following is some knowledge about regular expression
you can pratice regular expresiion on https://regex101.com/

* '^':    matches the start of the string
* '$':    matches the end of the string
* '&':    the whole matched string
* [^abc]: a character except a, b, c
* '\s':   [ \r\t\n\f] space character (I don't know the meaning of '\f')
* '\w':   [a-zA-Z0-9_]
* '\W':   [^a-zA-Z0-9_]
* '\x00': a kind of space character
* '?:':   text: "Chung-Yi, Chi"  pattern: "Chung-Yi, (?:Chi)"   Ans: "Chung-Yi, Chi"
* '?=':   text: "Chung-Yi, Chi"  pattern: "Chung-Yi, (?=Chi)"   Ans: "Chung-Yi, "
* '?!':   text: "Chung-Yi, Wu"   pattern: "Chung-Yi, (?!Chi)"   Ans: "Chung-Yi, "
* '?<=':  text: "Chung-Yi, Chi"  pattern: "(?<=Chung-Yi, )Chi"  Ans: "Chi"