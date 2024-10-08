import onigurumacffi

class RegexSource:
    @staticmethod
    def has_captures(regex_source: str | None) -> bool: ...
    @staticmethod
    def has_back_references(regex_source: str | None) -> bool: ...
    @staticmethod
    def replace_captures(
        regex_source: str, capture_source: str, captures: list[str]
    ) -> str: ...
    @staticmethod
    def replace_back_references(
        regex_source: str, line_text: str, captures: list[str]
    ) -> str: ...

class RegexSourceStart(RegexSource):
    original_pattern: str
    regex: onigurumacffi._Pattern
    def __init__(self, pattern: str) -> None: ...
    def match(self, line: str, start: int = 0) -> onigurumacffi._Match | None: ...
    def search(self, line: str, start: int = 0) -> onigurumacffi._Match | None: ...

class RegexSourceEnd(RegexSource):
    original_pattern: str
    regex: onigurumacffi._Pattern
    def __init__(self, pattern: str) -> None: ...
    def match(
        self, line: str, start: int, begin_match: onigurumacffi._Match
    ) -> onigurumacffi._Match | None: ...
