from types import UnionType
from typing import Any

from hypothesis import strategies as st


def everything_except(
    excluded_types: tuple[type | UnionType, ...],
) -> st.SearchStrategy[Any]:
    """Generate arbitrary values excluding instances of specified types.

    Args:
        excluded_types: A type or tuple of types to exclude from generation.

    Returns:
        A strategy that generates values not matching the excluded type(s).
    """
    return (
        st.from_type(object)
        .map(type)
        .filter(lambda x: not isinstance(x, excluded_types))
    )
