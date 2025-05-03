from ..channel import FromChannel
from .type import *
from typing import Hashable



T = TypeVar("T", bound = Hashable)
FromAllocator: TypeAlias = ChannelAllocator[FromChannel[T], T]
class _Base(FromAllocator[T]): pass
class _Global(_Base[T]): 
    def _alloc(self) -> list[T]: 
        r = self.channel.r
        def rank_value(t: T): 
            c = max(c_ for r_, c_ in self.con_map[t][0] if r_ == r)
            rc = min(self.con_map[t][1])
            return(
                rc[0] != r, rc[0] <= r, 
                c if rc[0] >= r else -c, 
                - rc[0] if rc[0] >= r else rc[0], 
                - rc[1] if rc[0] == r else rc[1],
                t.__hash__()
            )
        return sorted(self.channel.cons, key = rank_value)



_from_alloc_dict: AllocDict[FromAllocator] = {
    DFT: _Base, 
    DRC: _Base, 
    GLB: _Global
}