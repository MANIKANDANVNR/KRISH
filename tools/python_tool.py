import ast
import math


class PythonTool:

    name = "python"

    permission = "tool.python"

    risk = "high"

    description = (
        "Evaluates restricted mathematical "
        "Python expressions."
    )

    ALLOWED_NAMES = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "pi": math.pi,
        "e": math.e,
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

        tree = ast.parse(
            expression,
            mode="eval",
        )

        for node in ast.walk(tree):

            if isinstance(
                node,
                (
                    ast.Import,
                    ast.ImportFrom,
                    ast.Lambda,
                    ast.FunctionDef,
                    ast.ClassDef,
                    ast.Assign,
                    ast.NamedExpr,
                    ast.Attribute,
                ),
            ):

                raise PermissionError(
                    "Python operation is "
                    "not allowed."
                )

        compiled = compile(
            tree,
            "<krish>",
            "eval",
        )

        return eval(
            compiled,
            {
                "__builtins__": {},
                **self.ALLOWED_NAMES,
            },
            {},
        )