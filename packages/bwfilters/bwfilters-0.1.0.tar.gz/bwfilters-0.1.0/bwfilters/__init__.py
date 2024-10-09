"""
bwfilters
"""

# Copyright (C) 2024, Jacob Sánchez Pérez

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

from fnmatch import fnmatch
from dataclasses import dataclass
from typing import TypeVar, Generic
from collections.abc import Sequence, Iterable, Callable

T = TypeVar('T')
SearchT = TypeVar('SearchT')


def _filter(f: Callable[[T], SearchT | None],
            items: Sequence[T],
            search: Callable[[SearchT | None, Sequence[SearchT]], bool], *,
            blacklist: Sequence[SearchT] | None = None,
            whitelist: Sequence[SearchT] | None = None) -> Iterable[T]:
    """
    Filter a list of items by a whitelist or blacklist
    Whitelist takes priority

    :param items: The sequence containing the items to filter
    :param f: A function that processes the item in the sequence
              before filtering (e.g. filtering by attribute)
    :param search: A search function
    :param blacklist: Items that will be filtered out
    :param whitelist: Only these items will be allowed
    """
    filter_f = None
    if f is None:
        f = lambda x: x

    if whitelist is not None:
        filter_f = lambda x: search(f(x), whitelist)
    elif blacklist is not None:
        filter_f = lambda x: not search(f(x), blacklist)

    return filter(filter_f, items)


@dataclass
class BWFilter(Generic[T]):
    """Represents a blacklist/whitelist filter.

    If a whitelist exists it will take precedence.
    """
    blacklist: list[str] | None = None
    whitelist: list[str] | None = None

    def filter(self, f: Callable[[T], str | None],
               items: Sequence[T]) -> Iterable[T]:
        """
        Filters a list of items with either a blacklist or whitelist.

        :param f: A function that can process the items on the list
                  before comparing to the filters
        :param items: A list of items to use the filter onn
        """
        return _filter(f, items, lambda x, seq: x in seq,
                       blacklist=self.blacklist, whitelist=self.whitelist)

    def filter_wc(self, f: Callable[[T], str | None],
                  items: Sequence[T]) -> Iterable[T]:
        """
        The same as filter except items are matched with wildcards.

        :see `filter`:
        """
        return _filter(
            f, items,
            lambda x, seq: (x is not None) and any(fnmatch(s, x) for s in seq),
            blacklist=self.blacklist, whitelist=self.whitelist
        )


__all__ = ['BWFilter']
