import onigurumacffi

from typing import Union
from .rule import Rule


class TextMateGrammarRepository:
    def __init__(self, grammars: list[dict]) -> None:
        self.grammars: dict = {grammar["scopeName"]: grammar for grammar in grammars}
        self.loaded_grammars: dict = {}

    def get_grammar(self, scope_name: str) -> Union["TextMateGrammar", None]:
        if scope_name in self.loaded_grammars:
            return self.loaded_grammars[scope_name]

        if scope_name in self.grammars:
            grammar = TextMateGrammar(self.grammars[scope_name], self)
            self.loaded_grammars[scope_name] = grammar
            return grammar

        return None

    def get_grammar_by_language(
        self, languag_id: str
    ) -> Union["TextMateGrammar", None]:
        return self[f"source.{languag_id}"]

    def __getitem__(self, key: str) -> dict:
        return self.grammars[key]

    def __iter__(self):
        return iter(self.grammars)

    def __len__(self):
        return len(self.grammars)

    def keys(self):
        return self.grammars.keys()

    def values(self):
        return self.grammars.values()

    def items(self):
        return self.grammars.items()


class TextMateGrammar:
    def __init__(self, grammar: dict, grammar_repository: TextMateGrammarRepository):
        """Loads and parses a grammar definition

        Args:
            grammar (dict):  A dictionary containing the default grammar.
            grammarRepository (TextMateGrammarRepository): Grammar repository used to parse source includes.
        """
        self._grammar_repository = grammar_repository
        self._grammar = grammar
        self._scope_name = grammar["scopeName"]
        self._rules = [Rule(pattern) for pattern in grammar["patterns"]]
        self._repository = {
            name: Rule(rule) for name, rule in grammar.get("repository", {}).items()
        }

    def parse(self, line: str) -> list[tuple[str, tuple[int, int]]]:
        """Parse a line of text using the grammar rules.

        Args:
            line (str): The line of text to parse.

        Returns:
            list[tuple[str, tuple[int, int]]]: A list of tuples containing the matched scopes and their positions in format of (scope_name, (start,end)).
        """
        return self._parse(line)

    def _parse(
        self, line: str, rules: list[Rule] | None = None, add: int = 0
    ) -> list[tuple[str, tuple[int, int]]]:
        """Parse a line of text using the grammar rules.

        Args:
            line (str): The line of text to parse.
            rules (list[Rule] | None, optional): The rules to apply. If None, use the default rules.
            add (int, optional): Offset to add to the start and end positions.

        Returns:
            list[tuple[str, tuple[int, int]]]: A list of tuples containing the matched scopes and their positions in format of (scope_name, (start,end)).
        """
        if rules is None:
            rules = self._rules

        expressions: list[tuple[str, tuple[int, int]]] = []
        for rule in rules:
            if rule.include:
                expressions.extend(self._handle_include(line, rule.include, add))
            elif rule.match:
                expressions.extend(self._handle_match(line, rule, add))
            elif rule.begin and rule.end:
                expressions.extend(self._handle_begin_end(line, rule, add))
            elif rule.patterns:
                expressions.extend(
                    self._parse(line, [Rule(p) for p in rule.patterns], add)
                )

        return expressions

    def _handle_include(
        self, line: str, include: str, add: int
    ) -> list[tuple[str, tuple[int, int]]]:
        if include.startswith("#"):
            return self._parse(line, [self._repository[include[1:]]], add)
        elif include.startswith("source."):
            parts = include.split("#")
            grammar_scope = parts[0]
            rule = parts[1] if len(parts) > 1 else None

            external_grammar = self._grammar_repository.get_grammar(grammar_scope)
            if not external_grammar:
                return []
            if rule:
                if rule in external_grammar._repository:
                    return external_grammar._parse(
                        line, [external_grammar._repository[rule]], add
                    )
            return external_grammar._parse(line, add=add)
        elif include in ["$self", "$base"]:
            return self._parse(line, self._rules, add)
        elif include in self._grammar:
            return self._parse(line, [Rule(self._grammar[include])], add)
        else:
            return []

    def _handle_match(
        self, line: str, rule: Rule, add: int
    ) -> list[tuple[str, tuple[int, int]]]:
        expressions: list[tuple[str, tuple[int, int]]] = []
        position: int = 0
        while position < len(line):
            search = rule.match_regex.search(line, position)
            if not search:
                break

            if rule.name:
                start = search.start(0) + add
                end = search.end(0) + add
                if start != end:
                    expressions.append((rule.name, (start, end)))

            if rule.patterns:
                expressions.extend(
                    self._parse(
                        line[search.start(0) : search.end(0)],
                        [Rule(p) for p in rule.patterns],
                        add + search.start(0),
                    )
                )

            if rule.captures:
                expressions.extend(self._handle_captures(rule.captures, search, add))

            if search.end(0) > position:
                position = search.end(0)
            else:
                position += 1

        return expressions

    def _handle_begin_end(
        self, line: str, rule: Rule, add: int
    ) -> list[tuple[str, tuple[int, int]]]:
        expressions: list[tuple[str, tuple[int, int]]] = []
        last: int = 0
        while True:
            begin = rule.begin_regex.search(line, last)
            if not begin:
                break
            end_pos = len(line)
            end = rule.end_regex.search(line, begin.end(0), begin)
            if not end:
                end_pos = len(line)
                if rule.content_name:
                    expressions.append(
                        (rule.content_name, (begin.end(0) + add, end_pos + add))
                    )
                if rule.name:
                    expressions.append(
                        (rule.name, (begin.start(0) + add, end_pos + add))
                    )

                if rule.patterns:
                    expressions.extend(
                        self._parse(
                            line[begin.end(0) :],
                            [Rule(p) for p in rule.patterns],
                            add + begin.end(0),
                        )
                    )

                break

            expressions.extend(self._handle_captures(rule.begin_captures, begin, add))
            expressions.extend(self._handle_captures(rule.end_captures, end, add))

            if rule.content_name:
                expressions.append(
                    (rule.content_name, (begin.end(0) + add, end.start(0) + add))
                )

            if rule.name:
                expressions.append(
                    (rule.name, (begin.start(0) + add, end.end(0) + add))
                )

            if rule.patterns:
                expressions.extend(
                    self._parse(
                        line[begin.end(0) : end.start(0)],
                        [Rule(p) for p in rule.patterns],
                        add + begin.end(0),
                    )
                )

            last = end.end(0)

        return expressions

    def _handle_captures(
        self, captures: dict | None, match: onigurumacffi._Match, add: int
    ) -> list[tuple[str, tuple[int, int]]]:
        expressions: list[tuple[str, tuple[int, int]]] = []
        if captures:
            for i, capture in captures.items():
                if name := capture.get("name"):
                    try:
                        start = match.start(int(i))
                        end = match.end(int(i))

                        if start != end:
                            expressions.append((name, (start + add, end + add)))
                    except IndexError:
                        pass
        return expressions
