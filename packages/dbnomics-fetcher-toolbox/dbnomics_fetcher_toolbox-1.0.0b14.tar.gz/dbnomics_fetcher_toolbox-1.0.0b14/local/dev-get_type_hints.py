# ruff: noqa: T201
from dataclasses import dataclass
from typing import Any, Optional, get_type_hints

import typedload
from typedload.datadumper import Dumper


@dataclass
class Node:
    value: int
    child: Optional["Node"] = None


n1 = Node(1, Node(2))

print(get_type_hints(type(n1)))
breakpoint()
print(get_type_hints(n1))
# typedload.dump(n1)


def _new_dataclassdump(d: Dumper, value, t) -> dict[str, Any]:
    t = type(value)
    cached = d._dataclasscache.get(t)
    if cached is None:
        from dataclasses import _MISSING_TYPE as DT_MISSING_TYPE

        fields = set(value.__dataclass_fields__.keys())
        field_defaults = {
            k: v.default for k, v in value.__dataclass_fields__.items() if not isinstance(v.default, DT_MISSING_TYPE)
        }
        field_factories = {
            k: v.default_factory()
            for k, v in value.__dataclass_fields__.items()
            if not isinstance(v.default_factory, DT_MISSING_TYPE)
        }
        defaults = {**field_defaults, **field_factories}  # Merge the two dictionaries
        type_hints = get_type_hints(t)
        d._dataclasscache[t] = (fields, defaults, type_hints)
    else:
        fields, defaults, type_hints = cached

    return {
        value.__dataclass_fields__[f].metadata.get(d.mangle_key, f): d.dump(getattr(value, f), type_hints.get(f, Any))
        for f in fields
        if not d.hidedefault or f not in defaults or defaults[f] != getattr(value, f)
    }


dumper = Dumper()
for index, (condition, value_dumper) in enumerate(dumper.handlers):
    if value_dumper == typedload.datadumper._dataclassdump:
        dumper.handlers[index] = (condition, _new_dataclassdump)

print(dumper.dump(n1))
