# SPDX-License-Identifier: MIT
from functools import partial

from optree import register_pytree_node, tree_flatten, tree_unflatten

__all__ = ["register_ser_node", "register_de_node", "flatten", "unflatten"]

_SER_NAMESPACE = "__xattrs_ser__"
_DE_NAMESPACE = "__xattrs_der__"

register_ser_node = partial(register_pytree_node, namespace=_SER_NAMESPACE)
register_de_node = partial(register_pytree_node, namespace=_DE_NAMESPACE)

# flatten = partial(tree_flatten, namespace=_TREE_NAMESPACE)
# unflatten = tree_unflatten
