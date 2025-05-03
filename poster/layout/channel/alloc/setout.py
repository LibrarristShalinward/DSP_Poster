from ..channel import SetoutChannel
from .base import ChannelAllocator
from typing import Hashable, TypeAlias, TypeVar



T = TypeVar("T", bound = Hashable)
SetoutAllocator: TypeAlias = ChannelAllocator[SetoutChannel[T], T]
class _Base(SetoutAllocator[T]): pass
class _Direct(_Base[T]): 
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



_setout_alloc_dict: dict[str, type[SetoutAllocator]] = {
    "": _Base, 
    "direct": _Direct
}