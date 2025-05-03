from ..channel import SetoutChannel
from .base import ChannelAllocator, ConMap
from typing import Hashable, TypeVar



T = TypeVar("T", bound = Hashable)
class SetoutAllocator(ChannelAllocator[SetoutChannel, T]): 
    def __init__(self, channel: SetoutChannel[T], con_map: ConMap[T]):
        ChannelAllocator.__init__(self, channel, con_map)
    def _alloc(self) -> list[T]: 
        r, c = self.channel.rc
        def rank_value(t: T): 
            rc = max(self.con_map[t][1])
            return(
                max(r - rc[0] + 1, 0), 
                (-rc[0], rc[1]) if rc[1] > c and rc[0] > r else (), 
                rc, 
                t.__hash__()
            )
        return sorted(self.channel.cons, key = rank_value)