# HTMLViewer

## Overview

It's a "toy" to learn browser, and I would focus on render engine first.

I would implement a simple version in python3. Because I am not sure how much difficulty ahead, python is a flexible programming language to solve various cases, and it's easy to make a prototype product.

Maybe I would develope in other programming language in the future. Anyway, just do it!

* Tutorial
    * [來做個網路瀏覽器吧！Let's build a web browser! 系列](https://ithelp.ithome.com.tw/users/20103745/ironman/1270)
    * [Let's build a browser engine!](https://limpet.net/mbrubeck/2014/08/08/toy-layout-engine-1.html)

* Code
    * [mbrubeck/robinson (Rust)](https://github.com/mbrubeck/robinson): A toy web rendering engine
    * [reesmichael1/WebWhir (c++)](https://github.com/reesmichael1/WebWhir/): A simple HTML rendering engine
    * [FATESAIKOU/QueriableHtml (golang)](https://github.com/FATESAIKOU/QueriableHtml): A simple HTML parser

## Workflow

- [ ] Parse HTML
- [ ] Parse CSS
- [ ] Combined with the HTML DOM tree and CSS attributes to generate the style tree
- [ ] Convert the style tree into layout
- [ ] Draw GUI