# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import awkward as ak

np = ak.nplike.NumpyMetadata.instance()


def to_jax(array):
    pass


#     """
#     Converts `array` (many types supported) into a JAX array, if possible.

#     If the data are numerical and regular (nested lists have equal lengths
#     in each dimension, as described by the #type), they can be losslessly
#     converted to a CuPy array and this function returns without an error.

#     Otherwise, the function raises an error.

#     If `array` is a scalar, it is converted into a JAX scalar.

#     See also #ak.to_cupy, #ak.from_jax and #ak.to_numpy.
#     """
#     try:
#         import jax
#     except ImportError:
#         raise ImportError(
#             """to use {0}, you must install jax:

#                 pip install jax jaxlib
#             """
#         )

#     if isinstance(array, (bool, numbers.Number)):
#         return jax.numpy.array([array])[0]

#     elif isinstance(array, jax.numpy.ndarray):
#         return array

#     elif isinstance(array, np.ndarray):
#         return jax.numpy.asarray(array)

#     elif isinstance(array, ak.highlevel.Array):
#         return to_jax(array.layout)

#     elif isinstance(array, ak.highlevel.Record):
#         raise ValueError(
#             "JAX does not support record structures"
#             + ak._util.exception_suffix(__file__)
#         )

#     elif isinstance(array, ak.highlevel.ArrayBuilder):
#         return to_jax(array.snapshot().layout)

#     elif isinstance(array, ak.layout.ArrayBuilder):
#         return to_jax(array.snapshot())

#     elif (
#         ak.operations.describe.parameters(array).get("__array__") == "bytestring"
#         or ak.operations.describe.parameters(array).get("__array__") == "string"
#     ):
#         raise ValueError(
#             "JAX does not support arrays of strings"
#             + ak._util.exception_suffix(__file__)
#         )

#     elif isinstance(array, ak.partition.PartitionedArray):
#         return jax.numpy.concatenate([to_jax(x) for x in array.partitions])

#     elif isinstance(array, ak._util.virtualtypes):
#         return to_jax(array.array)

#     elif isinstance(array, ak._util.unknowntypes):
#         return jax.numpy.array([])

#     elif isinstance(array, ak._util.indexedtypes):
#         return to_jax(array.project())

#     elif isinstance(array, ak._util.uniontypes):
#         array = array.simplify()
#         if isinstance(array, ak._util.uniontypes):
#             raise ValueError(
#                 "cannot convert {0} into jax.numpy.array".format(array)
#                 + ak._util.exception_suffix(__file__)
#             )
#         return to_jax(array)

#     elif isinstance(array, ak.layout.UnmaskedArray):
#         return to_jax(array.content)

#     elif isinstance(array, ak._util.optiontypes):
#         content = to_jax(array.project())

#         shape = list(content.shape)
#         shape[0] = len(array)
#         mask0 = jax.numpy.asarray(array.bytemask()).view(np.bool_)
#         if mask0.any():
#             raise ValueError(
#                 "JAX does not support masked arrays"
#                 + ak._util.exception_suffix(__file__)
#             )
#         else:
#             return content

#     elif isinstance(array, ak.layout.RegularArray):
#         out = to_jax(array.content)
#         head, tail = out.shape[0], out.shape[1:]
#         shape = (head // array.size, array.size) + tail
#         return out[: shape[0] * array.size].reshape(shape)

#     elif isinstance(array, ak._util.listtypes):
#         return to_jax(array.toRegularArray())

#     elif isinstance(array, ak._util.recordtypes):
#         raise ValueError(
#             "JAX does not support record structures"
#             + ak._util.exception_suffix(__file__)
#         )

#     elif isinstance(array, ak.layout.NumpyArray):
#         return array.to_jax()

#     elif isinstance(array, ak.layout.Content):
#         raise AssertionError(
#             "unrecognized Content type: {0}".format(type(array))
#             + ak._util.exception_suffix(__file__)
#         )

#     elif isinstance(array, Iterable):
#         return jax.numpy.asarray(array)

#     else:
#         raise ValueError(
#             "cannot convert {0} into jax.numpy.array".format(array)
#             + ak._util.exception_suffix(__file__)
#         )