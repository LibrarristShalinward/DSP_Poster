from ..channel import ToChannel
from .base import ChannelAllocator, ConMap
from typing import Hashable, TypeVar



T = TypeVar("T", bound = Hashable)
class ToAllocator(ChannelAllocator[ToChannel, T]): 
    def __init__(self, channel: ToChannel[T], con_map: ConMap[T]):
        ChannelAllocator.__init__(self, channel, con_map)
    def _alloc(self) -> list[T]: 
        r = self.channel.r
        def rank_value(t: T): 
            c = min(c_ for r_, c_ in self.con_map[t][1] if r_ == r )
            rc = max(self.con_map[t][0])
            return(
                max(rc[0] - r + 1, 0), 
                c, 
                (-rc[0], rc[1]) if rc[1] > c and rc[0] < r else (), 
                rc, 
                t.__hash__()
            )
        return sorted(self.channel.cons, key = rank_value, reverse = True)