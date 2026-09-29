from tools.calculator import CalculatorTool
from tools.python_tool import PythonTool


def test_calculator():

    tool = CalculatorTool()

    result = tool.execute(
        "((12 + 3) * 4) / 2"
    )

    assert result == 30


def test_complex_calculation():

    tool = CalculatorTool()

    result = tool.execute(
        "(1000 + 250) * 3 - 125"
    )

    assert result == 3625


def test_python_expression():

    tool = PythonTool()

    assert tool.execute(
        "sqrt(144) + 5"
    ) == 17