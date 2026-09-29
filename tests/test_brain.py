from brain.context import ContextBuilder
from brain.validation import ResponseValidator


def test_context():

    builder = ContextBuilder()

    messages = builder.build(
        "You are KRISH.",
        [],
        [],
        "Hello",
    )

    assert messages[-1]["content"] == "Hello"


def test_validation():

    validator = ResponseValidator()

    assert validator.validate(
        "  hello  "
    ) == "hello"