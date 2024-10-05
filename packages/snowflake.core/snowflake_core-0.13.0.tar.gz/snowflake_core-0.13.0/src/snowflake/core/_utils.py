import re

from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from snowflake.core.function import Function
    from snowflake.core.procedure import Procedure
    from snowflake.core.user_defined_function import UserDefinedFunction

def get_function_name_with_args(
    function: Union["Function", "Procedure", "UserDefinedFunction"]
) -> str:
    return f"{function.name}({','.join([str(argument.datatype) for argument in function.arguments])})"

FUNCTION_WITH_ARGS_PATTERN = re.compile(r"""^(\"([^\"]|\"\")+\"|[a-zA-Z_][a-zA-Z0-9_$]*)\(([A-Za-z,0-9_]*)\)$""")

def replace_function_name_in_name_with_args(
    name_with_args: str,
    new_name: str
) -> str:
    matcher = FUNCTION_WITH_ARGS_PATTERN.match(name_with_args)
    if not matcher:
        raise ValueError("Invalid function name with arguments")

    args = matcher.group(3)
    return f"{new_name}({args})"
