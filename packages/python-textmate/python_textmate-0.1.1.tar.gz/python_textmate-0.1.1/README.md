# TextMate grammar parser for python

## Install

`pip install python-textmate`

## Usage

The parser can parse one line, to parse multiple lines iterate over each line and call parse()

```python
>>> from textmate import TextMateGrammar
>>> import json
>>> code = "print(True) # the parser only parses one line."
>>> with open("MagicPython.tmLanguage.json", "r") as tm:
...     grammar = TextMateGrammar(json.load(tm))
...     print(grammar.parse("print(True)"))
...

[('constant.language.python', (6, 10)),
 ('punctuation.parenthesis.begin.python', (5, 6)),
 ('punctuation.parenthesis.end.python', (10, 11)),
 ('constant.language.python', (6, 10)),
 ('punctuation.definition.arguments.end.python', (10, 11)),
 ('meta.function-call.python', (0, 11)),
 ('keyword.illegal.name.python', (6, 10)),
 ('support.function.builtin.python', (0, 5)),
 ('meta.function-call.generic.python', (0, 5)),
 ('support.function.builtin.python', (0, 5))] 
```