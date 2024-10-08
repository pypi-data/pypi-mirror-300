import re

import onigurumacffi

_CAPTURING_REGEX_SOURCE = re.compile(r"\$(\d+)|\${(\d+):\/(downcase|upcase)}")
_HAS_BACK_REFERENCES = re.compile(r"\\(\d+)")
_BACK_REFERENCING_END = re.compile(r"\\(\d+)")


class RegexSource:
    @staticmethod
    def has_captures(regex_source: str | None) -> bool:
        """Check the regex source for captrues

        Args:
            regex_source (str | None): Regex source to check.

        Returns:
            bool: Boolean value representing the state of the regex source.
        """
        if regex_source is None:
            return False
        return _CAPTURING_REGEX_SOURCE.search(regex_source) is not None

    @staticmethod
    def has_back_references(regex_source: str | None) -> bool:
        """Check the regex source for backreferences.

        Args:
            regex_source (str | None): Regex source to check.

        Returns:
            bool: Boolean value representing the state of the regex source.
        """
        if regex_source is None:
            return False
        return _HAS_BACK_REFERENCES.search(regex_source) is not None

    @staticmethod
    def replace_captures(
        regex_source: str, capture_source: str, captures: list[str]
    ) -> str:
        """Replaces captures in the regex source with captured values.

        Args:
            regex_source (str): Regex source containing captures.
            capture_source (str): Source string from which captures are made.
            captures (list[str]): List of already captured values.

        Returns:
            str: Regex source with the captures replaced.
        """

        def replace(match: re.Match) -> str:
            index = int(match.group(1) or match.group(2))
            command = match.group(3)
            if 0 <= index < len(captures):
                result = captures[index]
                while result and result[0] == ".":
                    result = result[1:]

                if command == "downcase":
                    return result.lower()
                if command == "upcase":
                    return result.upper()
                else:
                    return result
            else:
                return match.group(0)

        return _CAPTURING_REGEX_SOURCE.sub(replace, regex_source)

    @staticmethod
    def replace_back_references(
        regex_source: str, line_text: str, captures: list[str]
    ) -> str:
        """Replaces backreferences in the regex source with captured values.

        Args:
            regex_source (str): Regex source containing back references.
            capture_source (str): Source string from which captures are made.
            captures (list[str]): List of already captured values.

        Returns:
            str: Regex source with the backreferences replaced.
        """

        def replace(match: re.Match) -> str:
            index = int(match.group(1))
            return re.escape(captures[index] if 0 <= index < len(captures) else "")

        return _BACK_REFERENCING_END.sub(replace, regex_source)


class RegexSourceStart(RegexSource):
    def __init__(self, pattern: str):
        """Handles start regex patterns.

        Args:
            pattern (str): Regex pattern string to handle
        """
        self.original_pattern = pattern
        self.regex = onigurumacffi.compile(pattern)

    def search(self, line: str, start: int = 0) -> onigurumacffi._Match | None:
        """Search for the pattern in line.

        Args:
            line (str): Line to search in.
            start (int, optional): Starting positon for the search. Defaults to 0.

        Returns:
            onigurumacffi._Match | None: A match object if found, None otherwise.
        """
        return self.regex.search(line, start)


class RegexSourceEnd(RegexSource):
    def __init__(self, pattern: str):
        self.original_pattern: str = pattern
        self.regex: onigurumacffi._Pattern | None = None

    def search(
        self, line: str, start: int, begin_match: onigurumacffi._Match
    ) -> onigurumacffi._Match | None:
        """Search the end pattern, considering captures and back references.

        Args:
            line (str): Line to search in.
            start (int): Starting position for the start.
            begin_match (onigurumacffi._Match): Match object of the begin pattern.

        Returns:
            onigurumacffi._Match | None: A match object if found, None otherwise.
        """
        if self.has_captures(self.original_pattern) or self.has_back_references(
            self.original_pattern
        ):
            modified_pattern = self.original_pattern

            if self.has_captures(modified_pattern):
                captures = [begin_match.group(i) for i in range(len(begin_match._begs))]
                modified_pattern = self.replace_captures(
                    modified_pattern, line, begin_match
                )

            if self.has_back_references(modified_pattern):
                captures = [begin_match.group(i) for i in range(len(begin_match._begs))]
                modified_pattern = self.replace_back_references(
                    modified_pattern, line, captures
                )

            self.regex = onigurumacffi.compile(modified_pattern)
        elif self.regex is None:
            self.regex = onigurumacffi.compile(self.original_pattern)

        return self.regex.search(line, start)
