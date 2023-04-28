from typing import Any


def is_non_empty_string_list(data: Any):
    if not isinstance(data, list):
        return False
    if len(data) == 0:  # type: ignore
        return False
    return True
