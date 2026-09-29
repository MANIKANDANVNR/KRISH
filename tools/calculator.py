import ast
import math
import operator


class CalculatorTool:

    name = "calculator"

    permission = "tool.calculator"

    risk = "low"

    description = (
        "Performs safe mathematical expressions."
    )

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def execute(
        self,
        expression,
    ):

        if not isinstance(
            expression,
            str,
        ):
            raise TypeError(
                "Expression must be text."
            )

        expression = expression.strip()

        if not expression:
            raise ValueError(
                "Expression cannot be empty."
            )

        if len(expression) > 500:
            raise ValueError(
                "Expression too long."
            )

        tree = ast.parse(
            expression,
            mode="eval",
        )

        def evaluate(node):

            if isinstance(
                node,
                ast.Expression,
            ):
                return evaluate(
                    node.body
                )

            if (
                isinstance(
                    node,
                    ast.Constant,
                )
                and isinstance(
                    node.value,
                    (int, float),
                )
            ):

                if not math.isfinite(
                    float(node.value)
                ):
                    raise ValueError(
                        "Non-finite number."
                    )

                return node.value

            if (
                isinstance(
                    node,
                    ast.BinOp,
                )
                and type(node.op)
                in self.OPERATORS
            ):

                left = evaluate(
                    node.left
                )

                right = evaluate(
                    node.right
                )

                if (
                    isinstance(
                        node.op,
                        ast.Pow,
                    )
                    and abs(right) > 100
                ):
                    raise ValueError(
                        "Exponent too large."
                    )

                operation = (
                    self.OPERATORS[
                        type(node.op)
                    ]
                )

                result = operation(
                    left,
                    right,
                )

                if isinstance(
                    result,
                    float,
                ) and not math.isfinite(
                    result
                ):
                    raise ValueError(
                        "Result is not finite."
                    )

                return result

            if (
                isinstance(
                    node,
                    ast.UnaryOp,
                )
                and type(node.op)
                in self.OPERATORS
            ):

                return self.OPERATORS[
                    type(node.op)
                ](
                    evaluate(
                        node.operand
                    )
                )

            raise ValueError(
                "Unsupported expression."
            )

        return evaluate(tree)