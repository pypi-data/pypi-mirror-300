# Copyright 2021 The OpenXLA Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from typing import (Any, Callable, Hashable, Iterable, List, Optional, Sequence,
                    Tuple, Type, TypeVar)

_T = TypeVar("_T")

version: int

class PyTreeRegistry:
  def __init__(self, *, enable_none: bool = ..., enable_tuple: bool = ...,
               enable_namedtuple: bool = ..., enable_list: bool = ...,
               enable_dict: bool = ...): ...
  def flatten(
      self,
      tree: Any,
      leaf_predicate: Optional[Callable[[Any], bool]] = ...,
  ) -> Tuple[List[Any], PyTreeDef]: ...
  def flatten_one_level(
      self, tree: Any
  ) -> Optional[Tuple[Iterable[Any], Any]]: ...
  def register_node(
      self,
      __type: Type[_T],
      to_iterable: Callable[[_T], Tuple[_Children, _AuxData]],
      from_iterable: Callable[[_AuxData, _Children], _T]) -> Any: ...
  def register_dataclass_node(
      self,
      __type: Type[_T],
      meta_fields: List[str],
      data_fields: List[str]) -> Any: ...


def default_registry() -> PyTreeRegistry: ...

def tuple(registry: PyTreeRegistry, arg0: Sequence[PyTreeDef]) -> PyTreeDef: ...
def all_leaves(registry: PyTreeRegistry, arg0: Iterable[Any]) -> bool: ...

class PyTreeDef:
  def unflatten(self, __leaves: Iterable[Any]) -> Any: ...
  def flatten_up_to(self, __xs: Any) -> List[Any]: ...
  def compose(self, __inner: PyTreeDef) -> PyTreeDef: ...
  def walk(self,
           __f_node: Callable[[Any, Any], Any],
           __f_leaf: Optional[Callable[[_T], Any]],
           leaves: Iterable[Any]) -> Any: ...
  def from_iterable_tree(self, __xs: Any): ...
  def node_data(self) -> Optional[Tuple[Type, Any]]: ...
  def children(self) -> List[PyTreeDef]: ...
  @staticmethod
  def make_from_node_data_and_children(
      registry: PyTreeRegistry,
      node_data: Optional[Tuple[Type, Any]],
      children: Iterable[PyTreeDef],
  ) -> PyTreeDef:
    ...

  num_leaves: int
  num_nodes: int
  def __repr__(self) -> str: ...
  def __eq__(self, __other: PyTreeDef) -> bool: ...
  def __ne__(self, __other: PyTreeDef) -> bool: ...
  def __hash__(self) -> int: ...
  def __getstate__(self) -> Any: ...
  def __setstate__(self, state: Any): ...
  def serialize_using_proto(self) -> bytes: ...
  @staticmethod
  def deserialize_using_proto(
      registry: PyTreeRegistry, data: bytes
  ) -> PyTreeDef:
    ...

_Children = TypeVar("_Children", bound=Iterable[Any])
_AuxData = TypeVar("_AuxData", bound=Hashable)
