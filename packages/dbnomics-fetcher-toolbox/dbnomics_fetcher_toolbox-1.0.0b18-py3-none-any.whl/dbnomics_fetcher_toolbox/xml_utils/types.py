from collections.abc import Mapping
from typing import TypeAlias

__all__ = ["NamespaceDict"]

NamespaceDict: TypeAlias = Mapping[str | None, str]
