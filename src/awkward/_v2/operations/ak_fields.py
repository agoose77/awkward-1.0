# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import awkward as ak

np = ak.nplike.NumpyMetadata.instance()


def fields(array):
    """
    Extracts record fields or tuple slot numbers from `array` (many types
    supported, including all Awkward Arrays and Records).

    If the array contains nested records, only the outermost record is
    queried. If it contains tuples instead of records, this function outputs
    string representations of integers, such as `"0"`, `"1"`, `"2"`, etc.
    The records or tuples may be within multiple layers of nested lists.

    If the array contains neither tuples nor records, this returns an empty
    list.
    """
    with ak._v2._util.OperationErrorContext(
        "ak._v2.fields",
        dict(array=array),
    ):
        return _impl(array)


def _impl(array):
    layout = ak._v2.operations.to_layout(array, allow_record=True, allow_other=False)
    return layout.fields
