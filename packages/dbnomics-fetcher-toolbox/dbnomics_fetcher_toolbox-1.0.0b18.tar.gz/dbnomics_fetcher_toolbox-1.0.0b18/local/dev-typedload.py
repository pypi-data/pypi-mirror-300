# ruff: noqa: INP001, T201, UP006, UP035
# %%

import json
from dataclasses import dataclass
from typing import List, Optional, TypeAlias, get_type_hints

import msgspec
import typedload

# %%


@dataclass(kw_only=True)
class DatasetReference:
    code: str


@dataclass(kw_only=True)
class Category:
    code: str
    children: List["CategoryNode"]


CategoryNode: TypeAlias = Category | DatasetReference


@dataclass(kw_only=True)
class CategoryTree:
    children: List[CategoryNode]


# %%


c11 = Category(code="C11", children=[])
d1 = DatasetReference(code="C1")
c1 = Category(code="C1", children=[c11, d1])
ct1 = CategoryTree(children=[c1])
ct1

# %%

c1s = typedload.dump(c1)
# NameError: name 'Category' is not defined
c1s

# %%

get_type_hints(c1, localns={"CategoryNode": CategoryNode})

# %%

ct1s = msgspec.json.encode(ct1).decode("utf-8")
ct1s

# %%

ct1d = json.loads(ct1s)
ct1d

# %%

ct1_loaded = typedload.load(ct1d, type_=CategoryTree, frefs={"CategoryNode": CategoryNode})
ct1_loaded


# %%

# msgspec.json.decode(ct1s, type=CategoryTree)
# TypedloadValueError: ForwardRef 'Category | DatasetReference' unknown

# %%


@dataclass
class Node:
    value: int
    child: Optional["Node"] = None


n1 = Node(1, Node(2))

# %%

get_type_hints(n1)
# typedload.dump(n1)

# %%
