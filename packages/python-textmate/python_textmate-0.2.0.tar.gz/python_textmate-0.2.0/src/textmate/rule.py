from .source import RegexSourceStart, RegexSourceEnd


class Rule:
    def __init__(self, pattern: dict):
        """Represents a single rule in the TextMate grammar.

        Args:
            pattern (dict): A dictionary containing the rule pattern.
        """
        self.pattern: dict = pattern
        self.name: str = pattern.get("name")
        self.match: str = pattern.get("match")
        self.begin: str = pattern.get("begin")
        self.end: str = pattern.get("end")
        self.include: str = pattern.get("include")
        self.patterns: str = pattern.get("patterns")
        self.captures: str = pattern.get("captures")
        self.begin_captures: str = pattern.get("beginCaptures")
        self.end_captures: str = pattern.get("endCaptures")
        self.content_name: str = pattern.get("contentName")

        if self.match:
            self.match_regex: RegexSourceStart = RegexSourceStart(self.match)
        if self.begin:
            self.begin_regex: RegexSourceStart = RegexSourceStart(self.begin)
        if self.end:
            self.end_regex: RegexSourceEnd = RegexSourceEnd(self.end)
