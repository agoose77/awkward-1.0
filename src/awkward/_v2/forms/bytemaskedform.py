# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import awkward as ak
from awkward._v2.forms.form import Form, _parameters_equal, nonvirtual


class ByteMaskedForm(Form):
    def __init__(
        self,
        mask,
        content,
        valid_when,
        has_identifier=False,
        parameters=None,
        form_key=None,
    ):
        if not ak._util.isstr(mask):
            raise TypeError(
                "{0} 'mask' must be of type str, not {1}".format(
                    type(self).__name__, repr(mask)
                )
            )
        if not isinstance(content, Form):
            raise TypeError(
                "{0} all 'contents' must be Form subclasses, not {1}".format(
                    type(self).__name__, repr(content)
                )
            )
        if not isinstance(valid_when, bool):
            raise TypeError(
                "{0} 'valid_when' must be bool, not {1}".format(
                    type(self).__name__, repr(valid_when)
                )
            )

        self._mask = mask
        self._content = content
        self._valid_when = valid_when
        self._init(has_identifier, parameters, form_key)

    @property
    def mask(self):
        return self._mask

    @property
    def content(self):
        return self._content

    @property
    def valid_when(self):
        return self._valid_when

    def __repr__(self):
        args = [
            repr(self._mask),
            repr(self._content),
            repr(self._valid_when),
        ] + self._repr_args()
        return "{0}({1})".format(type(self).__name__, ", ".join(args))

    def _tolist_part(self, verbose, toplevel):
        return self._tolist_extra(
            {
                "class": "ByteMaskedArray",
                "mask": self._mask,
                "valid_when": self._valid_when,
                "content": self._content._tolist_part(verbose, toplevel=False),
            },
            verbose,
        )

    def __eq__(self, other):
        if isinstance(other, ByteMaskedForm):
            return (
                self._has_identifier == other._has_identifier
                and self._form_key == other._form_key
                and self._mask == other._mask
                and self._valid_when == other._valid_when
                and _parameters_equal(self._parameters, other._parameters)
                and self._content == other._content
            )
        else:
            return False

    def generated_compatibility(self, other):
        other = nonvirtual(other)

        if other is None:
            return True

        elif isinstance(other, ByteMaskedForm):
            return (
                self._mask == other._mask
                and self._valid_when == other._valid_when
                and _parameters_equal(self._parameters, other._parameters)
                and self._content.generated_compatibility(other._content)
            )

        else:
            return False

    def _getitem_range(self):
        return ByteMaskedForm(
            self._mask,
            self._content._getitem_range(),
            self._valid_when,
            has_identifier=self._has_identifier,
            parameters=self._parameters,
            form_key=None,
        )

    def _getitem_field(self, where, only_fields=()):
        return ByteMaskedForm(
            self._mask,
            self._content._getitem_field(where, only_fields),
            self._valid_when,
            has_identifier=self._has_identifier,
            parameters=None,
            form_key=None,
        )

    def _getitem_fields(self, where, only_fields=()):
        return ByteMaskedForm(
            self._mask,
            self._content._getitem_fields(where, only_fields),
            self._valid_when,
            has_identifier=self._has_identifier,
            parameters=None,
            form_key=None,
        )

    def _carry(self, allow_lazy):
        return ByteMaskedForm(
            self._mask,
            self._content._carry(allow_lazy),
            self._valid_when,
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