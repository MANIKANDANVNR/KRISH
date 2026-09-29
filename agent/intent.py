import re
from dataclasses import dataclass


@dataclass
class Intent:
    name: str
    arguments: dict
    confidence: float = 1.0
    requires_tool: bool = False


class IntentRouter:

    CALCULATOR_PATTERNS = (
        r"\bcalculate\b",
        r"\bcompute\b",
        r"\bsolve\b",
        r"\badd\b",
        r"\bsubtract\b",
        r"\bmultiply\b",
        r"\bdivide\b",
        r"\bplus\b",
        r"\bminus\b",
        r"\btimes\b",
    )

    PYTHON_PATTERNS = (
        r"^import\s+",
        r"^from\s+\w+\s+import\s+",
        r"^print\s*\(",
        r"^def\s+",
        r"^class\s+",
        r"^python\s+",
        r"^run\s+python\s+",
    )

    def detect(self, text):

        normalized = text.lower().strip()

        if not normalized:
            return Intent(
                "conversation",
                {},
                1.0,
                False,
            )

        # ---------------------------------------------------------
        # SYSTEM
        # ---------------------------------------------------------

        if any(
            phrase in normalized
            for phrase in (
                "open calculator",
                "launch calculator",
                "start calculator",
            )
        ):
            return Intent(
                "system.open_calculator",
                {},
                0.95,
                True,
            )

        # ---------------------------------------------------------
        # PYTHON
        # ---------------------------------------------------------

        if self._looks_like_python(normalized):

            expression = re.sub(
                r"^(run\s+python|python)\s*",
                "",
                normalized,
            ).strip()

            return Intent(
                "python",
                {
                    "expression": expression
                },
                0.95,
                True,
            )

        # ---------------------------------------------------------
        # CALCULATOR
        # ---------------------------------------------------------

        expression = self._extract_calculation(normalized)

        if expression:

            return Intent(
                "calculator",
                {
                    "expression": expression
                },
                0.95,
                True,
            )

        # ---------------------------------------------------------
        # FILE READ
        # ---------------------------------------------------------

        if normalized.startswith(
            ("read file ", "read the file ")
        ):

            path = normalized.split(
                "file",
                1
            )[1].strip()

            return Intent(
                "file.read",
                {
                    "path": path
                },
                0.90,
                True,
            )

        # ---------------------------------------------------------
        # FILE WRITE
        # ---------------------------------------------------------

        if normalized.startswith(
            ("write file ", "write to file ")
        ):

            remainder = normalized.split(
                "file",
                1
            )[1].strip()

            parts = remainder.split(
                " ",
                1,
            )

            if len(parts) == 2:

                return Intent(
                    "file.write",
                    {
                        "path": parts[0],
                        "content": parts[1],
                    },
                    0.90,
                    True,
                )

        # ---------------------------------------------------------
        # WEB
        # ---------------------------------------------------------

        if normalized.startswith(
            (
                "open url ",
                "get url ",
                "fetch url ",
            )
        ):

            url = re.sub(
                r"^(open url|get url|fetch url)\s+",
                "",
                normalized,
            ).strip()

            return Intent(
                "web.get",
                {
                    "url": url
                },
                0.90,
                True,
            )

        # ---------------------------------------------------------
        # NORMAL CONVERSATION
        # ---------------------------------------------------------

        return Intent(
            "conversation",
            {},
            0.75,
            False,
        )

    def _looks_like_python(self, text):

        return any(
            re.search(pattern, text)
            for pattern in self.PYTHON_PATTERNS
        )

    def _extract_calculation(self, text):

        numbers = re.findall(
            r"-?\d+(?:\.\d+)?",
            text,
        )

        if not numbers:
            return None

        has_math_word = any(
            re.search(
                pattern,
                text,
            )
            for pattern in self.CALCULATOR_PATTERNS
        )

        if not has_math_word:
            return None

        # ---------------------------------------------------------
        # MULTI STEP CALCULATION
        # ---------------------------------------------------------

        if (
            "add" in text
            and "multiply" in text
            and "divide" in text
            and len(numbers) >= 4
        ):

            a, b, multiplier, divisor = numbers[:4]

            return (
                f"(({a} + {b}) * "
                f"{multiplier}) / {divisor}"
            )

        # ---------------------------------------------------------
        # TWO NUMBER OPERATIONS
        # ---------------------------------------------------------

        if len(numbers) == 2:

            if "add" in text or "plus" in text:
                return (
                    f"{numbers[0]} + "
                    f"{numbers[1]}"
                )

            if (
                "subtract" in text
                or "minus" in text
            ):
                return (
                    f"{numbers[0]} - "
                    f"{numbers[1]}"
                )

            if (
                "multiply" in text
                or "times" in text
            ):
                return (
                    f"{numbers[0]} * "
                    f"{numbers[1]}"
                )

            if "divide" in text:
                return (
                    f"{numbers[0]} / "
                    f"{numbers[1]}"
                )

        return None