class Rule:
    pattern: dict
    name: str
    match: str
    begin: str
    end: str
    include: str
    patterns: str
    captures: str
    begin_captures: str
    end_captures: str
    content_name: str
    match_regex: str
    begin_regex: str
    end_regex: str
    def __init__(self, pattern: dict) -> None: ...
