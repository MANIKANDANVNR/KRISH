from agent.intent import IntentRouter


def test_calculator_intent():

    router = IntentRouter()

    intent = router.detect(
        "add 4 and 5 then multiply it with 557 "
        "then divide it with 4"
    )

    assert intent.name == "calculator"

    assert (
        intent.arguments["expression"]
        == "((4 + 5) * 557) / 4"
    )


def test_open_calculator_intent():

    router = IntentRouter()

    intent = router.detect(
        "open calculator"
    )

    assert (
        intent.name
        == "system.open_calculator"
    )


def test_python_intent():

    router = IntentRouter()

    intent = router.detect(
        "python sqrt(144)"
    )

    assert intent.name == "python"


def test_normal_conversation():

    router = IntentRouter()

    intent = router.detect(
        "Tell me about KRISH"
    )

    assert intent.name == "conversation"