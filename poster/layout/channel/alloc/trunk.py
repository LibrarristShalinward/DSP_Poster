from ..channel import TrunkChannel
from .type import *
from typing import Hashable



T = TypeVar("T", bound = Hashable)
TrunkAllocator: TypeAlias = ChannelAllocator[TrunkChannel[T], T]
class _Base(TrunkAllocator[T]): pass



_trunk_alloc_dict: AllocDict[TrunkAllocator] = {
    DFT: _Base, 
    DRC: _Base
}