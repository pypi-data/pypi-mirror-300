from .rule import Rule

class TextMateGrammar:
    def __init__(self, grammar: dict) -> None: ...
    def parse(
        self, line: str, rules: list[Rule] | None = None, add: int = 0
    ) -> list[tuple[str, tuple[int, int]]]: ...
