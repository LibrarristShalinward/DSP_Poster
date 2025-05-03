from ..channel import TrunkChannel
from .type import *
from typing import Hashable



T = TypeVar("T", bound = Hashable)
TrunkAllocator: TypeAlias = ChannelAllocator[TrunkChannel[T], T]
class _Base(TrunkAllocator[T]): pass
class _Global(_Base[T]): 
    def _alloc(self) -> list[T]: 
        def rank_value(t: T): 
            rcf = min((i, -j) for i, j in self.con_map[t][0])
            rct = max(self.con_map[t][1])
            return(
                (rcf[0], -rcf[1]), 
                (- rct[0], rct[1]),
            )
        return sorted(self.channel.cons, key = rank_value)



_trunk_alloc_dict: AllocDict[TrunkAllocator] = {
    DFT: _Base, 
    DRC: _Base, 
    GLB: _Global
}