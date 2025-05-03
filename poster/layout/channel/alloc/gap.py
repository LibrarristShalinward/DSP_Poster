from ..channel import GapChannel
from .type import *
from typing import Hashable



T = TypeVar("T", bound = Hashable)
GapAllocator: TypeAlias = ChannelAllocator[GapChannel[T], T]
class _Base(GapAllocator[T]): pass



_gap_alloc_dict: AllocDict[GapAllocator] = {
    DFT: _Base, 
    DRC: _Base, 
    GLB: _Base
}