# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import awkward as ak
from awkward._v2.forms.form import Form, _parameters_equal, nonvirtual


class RegularForm(Form):
    def __init__(
        self, content, size, has_identifier=False, parameters=None, form_key=None
    ):
        if not isinstance(content, Form):
            raise TypeError(
                "{0} all 'contents' must be Form subclasses, not {1}".format(
                    type(self).__name__, repr(content)
                )
            )
        if not ak._util.isint(size):
            raise TypeError(
                "{0} 'size' must be of type int, not {1}".format(
                    type(self).__name__, repr(size)
                )
            )

        self._content = content
        self._size = int(size)
        self._init(has_identifier, parameters, form_key)

    @property
    def content(self):
        return self._content

    @property
    def size(self):
        return self._size

    def __repr__(self):
        args = [repr(self._content), repr(self._size)] + self._repr_args()
        return "{0}({1})".format(type(self).__name__, ", ".join(args))

    def _tolist_part(self, verbose, toplevel):
        return self._tolist_extra(
            {
                "class": "RegularArray",
                "size": self._size,
                "content": self._content._tolist_part(verbose, toplevel=False),
            },
            verbose,
        )

    def __eq__(self, other):
        if isinstance(other, RegularForm):
            return (
                self._has_identifier == other._has_identifier
                and self._form_key == other._form_key
                and self._size == other._size
                and _parameters_equal(self._parameters, other._parameters)
                and self._content == other._content
            )
        else:
            return False

    def generated_compatibility(self, other):
        other = nonvirtual(other)

        if other is None:
            return True

        elif isinstance(other, RegularForm):
            return (
                self._size == other._size
                and _parameters_equal(self._parameters, other._parameters)
                and self._content.generated_compatibility(other._content)
            )

        else:
            return False

    def _getitem_range(self):
        return RegularForm(
            self._content._getitem_range(),
            self._size,
            has_identifier=self._has_identifier,
            parameters=self._parameters,
            form_key=None,
        )

    def _getitem_field(self, where, only_fields=()):
        return RegularForm(
            self._content._getitem_field(where, only_fields),
            self._size,
            has_identifier=self._has_identifier,
            parameters=None,
            form_key=None,
        )

    def _getitem_fields(self, where, only_fields=()):
        return RegularForm(
            self._content._getitem_fields(where, only_fields),
            self._size,
            has_identifier=self._has_identifier,
            parameters=None,
            form_key=None,
        )

    def _carry(self, allow_lazy):
        return RegularForm(
            self._content._carry(allow_lazy),
            self._size,
            has_identifier=self._has_identifier,
            parameters=self._parameters,
            form_key=None,
        )

    @property
    def purelist_isregular(self):
        return self._content.purelist_isregular

    @property
    def purelist_depth(self):
        if self.parameter("__array__") in ("string", "bytestring"):
            return 1
        else:
            return self._content.purelist_depth + 1

    @property
    def minmax_depth(self):
        if self.parameter("__array__") in ("string", "bytestring"):
            return (1, 1)
        else:
            mindepth, maxdepth = self._content.minmax_depth
            return (mindepth + 1, maxdepth + 1)

    @property
    def branch_depth(self):
        if self.parameter("__array__") in ("string", "bytestring"):
            return (False, 1)
        else:
            branch, depth = self._content.branch_depth
            return (branch, depth + 1)

    @property
    def keys(self):
        return self._content.keys