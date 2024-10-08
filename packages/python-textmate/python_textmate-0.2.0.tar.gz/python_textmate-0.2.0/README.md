# TextMate grammar parser for python

## Install

`pip install python-textmate`

## Usage

The parser can parse one line, to parse multiple lines iterate over each line and call parse()

```python
>>> from textmate import TextMateGrammar, TextMateGrammarRepository
>>> import json
>>> 
>>> def load_json(file_path):
...     with open(file_path, "r") as f:
...         return json.load(f)
... 
>>> # Initialize the grammar repository
>>> repository = TextMateGrammarRepository([
...     load_json("MagicPython.tmLanguage.json"),
...     load_json("MagicRegExp.tmLanguage.json")
... ])
>>> 
>>> # Get the Python grammar
>>> python_grammar = repository.get_grammar_by_language("python")
>>> 
>>> if python_grammar:
...     # Initiatee the grammar parser
...     grammar = TextMateGrammar(python_grammar, repository)
...     3 Parse one line of code
...     code = "print(True) # the parser only parses one line."
...     result = grammar.parse(code)
...     print(result)
... 
[('punctuation.definition.comment.python', (12, 13)),
 ('comment.line.number-sign.python', (12, 46)),
 ('constant.language.python', (6, 10)),
 ('punctuation.parenthesis.begin.python', (5, 6)),
 ('punctuation.parenthesis.end.python', (10, 11)),
 ('constant.language.python', (6, 10)),
 ('punctuation.definition.arguments.end.python', (10, 11)),
 ('meta.function-call.python', (0, 11)),
 ('keyword.illegal.name.python', (6, 10)),
 ('support.function.builtin.python', (0, 5)),
 ('meta.function-call.generic.python', (0, 5)),
 ('meta.function-call.generic.python', (6, 10)),
 ('meta.function-call.arguments.python', (6, 10)),
 ('constant.language.python', (6, 10)),
 ('support.function.builtin.python', (0, 5)),
 ('punctuation.separator.period.python', (45, 46)),
 ('meta.member.access.python', (45, 46))]
```