from typing import Any, Dict, List, Union

from pytoniq_core import Cell, Slice


def parse_stack(stack: List[Dict[str, Any]]) -> List[Union[int, Cell, Slice]]:
    result: List[Union[int, Cell, Slice]] = []

    handlers = {
        "num": lambda v: int(v, 16),
        "cell": Slice.one_from_boc,
        "slice": Slice.one_from_boc,
    }

    for item in stack:
        item_type = item.get("type")
        item_value = item.get("value")

        if item_value is None:
            item_value = item.get(item_type)

        result.append(handlers[item_type](item_value))

    return result
