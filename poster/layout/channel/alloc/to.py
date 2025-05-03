from ..channel import ToChannel
from .base import ChannelAllocator
from typing import Hashable, TypeAlias, TypeVar



T = TypeVar("T", bound = Hashable)
ToAllocator: TypeAlias = ChannelAllocator[ToChannel[T], T]
class _Base(ToAllocator[T]): pass
class _Direct(_Base[T]): 
    def _alloc(self) -> list[T]: 
        r = self.channel.r
        def rank_value(t: T): 
            c = min(c_ for r_, c_ in self.con_map[t][1] if r_ == r)
            rc = max(self.con_map[t][0])
            return(
                max(rc[0] - r + 1, 0), 
                c, 
                (-rc[0], rc[1]) if rc[1] > c and rc[0] < r else (), 
                rc, 
                t.__hash__()
            )
        return sorted(self.channel.cons, key = rank_value, reverse = True)



_to_alloc_dict: dict[str, type[ToAllocator]] = {
    "": _Base, 
    "direct": _Direct
}