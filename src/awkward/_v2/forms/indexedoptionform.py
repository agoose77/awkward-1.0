# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import awkward as ak
from awkward._v2.forms.form import Form, _parameters_equal, nonvirtual


class IndexedOptionForm(Form):
    def __init__(
        self,
        index,
        content,
        has_identifier=False,
        parameters=None,
        form_key=None,
    ):
        if not ak._util.isstr(index):
            raise TypeError(
                "{0} 'index' must be of type str, not {1}".format(
                    type(self).__name__, repr(index)
                )
            )
        if not isinstance(content, Form):
            raise TypeError(
                "{0} all 'contents' must be Form subclasses, not {1}".format(
                    type(self).__name__, repr(content)
                )
            )

        self._index = index
        self._content = content
        self._init(has_identifier, parameters, form_key)

    @property
    def index(self):
        return self._index

    @property
    def content(self):
        return self._content

    def __repr__(self):
        args = [repr(self._index), repr(self._content)] + self._repr_args()
        return "{0}({1})".format(type(self).__name__, ", ".join(args))

    def _tolist_part(self, verbose, toplevel):
        return self._tolist_extra(
            {
                "class": "IndexedOptionArray",
                "index": self._index,
                "content": self._content._tolist_part(verbose, toplevel=False),
            },
            verbose,
        )

    def __eq__(self, other):
        if isinstance(other, IndexedOptionForm):
            return (
                self._has_identifier == other._has_identifier
                and self._form_key == other._form_key
                and self._index == other._index
                and _parameters_equal(self._parameters, other._parameters)
                and self._content == other._content
            )
        else:
            return False

    def generated_compatibility(self, other):
        other = nonvirtual(other)

        if other is None:
            return True

        elif isinstance(other, IndexedOptionForm):
            return (
                self._index == other._index
                and _parameters_equal(self._parameters, other._parameters)
                and self._content.generated_compatibility(other._content)
            )

        else:
            return False

    def _getitem_range(self):
        return IndexedOptionForm(
            self._index,
            self._content,
            has_identifier=self._has_identifier,
            parameters=self._parameters,
            form_key=None,
        )

    def _getitem_field(self, where, only_fields=()):
        return IndexedOptionForm(
            self._index,
            self._content._getitem_field(where, only_fields),
            has_identifier=self._has_identifier,
            parameters=None,
            form_key=None,
        )

    def _getitem_fields(self, where, only_fields=()):
        return IndexedOptionForm(
            self._index,
            self._content._getitem_fields(where, only_fields),
            has_identifier=self._has_identifier,
            parameters=None,
            form_key=None,
        )

    def _carry(self, allow_lazy):
        return IndexedOptionForm(
            self._index,
            self._content,
            has_identifier=self._has_identifier,
            parameters=self._parameters,
            form_key=None,
        )

    @property
    def purelist_isregular(self):
        return self._content.purelist_isregular

    @property
    def purelist_depth(self):
        return self._content.purelist_depth

    @property
    def minmax_depth(self):
        return self._content.minmax_depth

    @property
    def branch_depth(self):
        return self._content.branch_depth

    @property
    def keys(self):
        return self._content.keys