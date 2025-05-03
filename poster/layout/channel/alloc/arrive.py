from ..channel import ArriveChannel
from .type import *
from typing import Hashable



T = TypeVar("T", bound = Hashable)
ArriveAllocator: TypeAlias = ChannelAllocator[ArriveChannel[T], T]
class _Base(ArriveAllocator[T]): pass
class _Direct(_Base[T]): 
    def _alloc(self) -> list[T]: 
        r, c = self.channel.rc
        def rank_value(t: T): 
            rc = max(self.con_map[t][0])
            return(
                max(rc[0] - r + 1, 0), 
                (-rc[0], rc[1]) if rc[1] > c and rc[0] < r else (), 
                rc, 
                t.__hash__()
            )
        return sorted(self.channel.cons, key = rank_value)



_arrive_alloc_dict: AllocDict[ArriveAllocator] = {
    DFT: _Base, 
    DRC: _Direct
}