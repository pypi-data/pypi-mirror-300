from snowflake.core._utils import replace_function_name_in_name_with_args


def test_replace_function_name_in_name_with_args():
    assert replace_function_name_in_name_with_args(
        "function_name(arg1,arg2)",
        "new_function_name"
    ) == "new_function_name(arg1,arg2)"

    assert replace_function_name_in_name_with_args(
        "function_name()",
        "new_function_name"
    ) == "new_function_name()"

    assert replace_function_name_in_name_with_args(
        """\"()fun()\"()""",
        """new_function_name"""
    ) == "new_function_name()"

    assert replace_function_name_in_name_with_args(
        """\"()fun()\"(ar)""",
        """new_function_name"""
    ) == "new_function_name(ar)"

    assert replace_function_name_in_name_with_args(
        """\"()fun()\"(ar12)""",
        """new_function_name"""
    ) == "new_function_name(ar12)"

    assert replace_function_name_in_name_with_args(
        """\"()fun()\"(ar12,ar13)""",
        """\"()()()\""""
    ) == "\"()()()\"(ar12,ar13)"

    assert replace_function_name_in_name_with_args(
        """abc(ar12,ar13)""",
        """\"()()()\""""
    ) == "\"()()()\"(ar12,ar13)"

    assert replace_function_name_in_name_with_args(
        """abc()""",
        """\"()()()\""""
    ) == "\"()()()\"()"

