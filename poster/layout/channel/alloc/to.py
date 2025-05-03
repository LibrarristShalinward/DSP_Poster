from ..channel import ToChannel
from .type import *
from typing import Hashable



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
class _Global(_Base[T]): 
    def _alloc(self) -> list[T]: 
        r = self.channel.r
        def rank_value(t: T): 
            c = max(c_ for r_, c_ in self.con_map[t][1] if r_ == r)
            r_, c_ = min((i, -j) for i, j in self.con_map[t][0])
            c_ = -c_
            if r_ < r - 1: 
                group = 0
                rc_ = r_, c_
            elif r_ == r - 1: 
                if c_ <= c: 
                    group = 1
                    rc_ = r_, c_
                else: 
                    group = 4
                    rc_ = r_, -c_
            elif r_ == r: 
                if c_ < c: 
                    group = -1
                    rc_ = r_, c_
                else: 
                    group = 3
                    rc_ = r_, -c_
            else: 
                group = 2
                rc_ = -r_, c_
            return(
                group != -1, group in [1, 3, 4], 
                c, group, 
                rc_, 
                t.__hash__()
            )
        return sorted(self.channel.cons, key = rank_value)



_to_alloc_dict: AllocDict[ToAllocator] = {
    DFT: _Base, 
    DRC: _Direct, 
    GLB: _Global
}