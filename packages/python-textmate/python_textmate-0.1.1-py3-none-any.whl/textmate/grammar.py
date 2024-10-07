import onigurumacffi

from .rule import Rule


class TextMateGrammar:
    def __init__(self, grammar: dict):
        self._grammar = grammar
        self._language = grammar["scopeName"][0]
        self._rules = [Rule(pattern) for pattern in grammar["patterns"]]
        self._repository = {
            name: Rule(rule) for name, rule in grammar.get("repository", {}).items()
        }

    def parse(
        self, line: str, rules: list[Rule] | None = None, add: int = 0
    ) -> list[tuple[str, tuple[int, int]]]:
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
                    self.parse(line, [Rule(p) for p in rule.patterns], add)
                )

        return expressions

    def _handle_include(
        self, line: str, include: str, add: int
    ) -> list[tuple[str, tuple[int, int]]]:
        if include.startswith("#"):
            return self.parse(line, [self._repository[include[1:]]], add)
        elif include in self._grammar:
            return self.parse(line, [Rule(self._grammar[include])], add)
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
                    self.parse(
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
            begin = rule.begin_regex.match(line, last)
            if not begin:
                break

            end = rule.end_regex.match(line, begin.end(0), begin)
            if not end:
                break

            expressions.extend(self._handle_captures(rule.begin_captures, begin, add))
            expressions.extend(self._handle_captures(rule.end_captures, end, add))

            if rule.content_name:
                expressions.append(
                    (rule.content_name, (begin.end(0), end.start(0) + add))
                )

            if rule.name:
                expressions.append(
                    (rule.name, (begin.start(0) + add, end.end(0) + add))
                )

            if rule.patterns:
                expressions.extend(
                    self.parse(
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
