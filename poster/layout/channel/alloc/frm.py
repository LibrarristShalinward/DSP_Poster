from ..channel import FromChannel
from .type import *
from typing import Hashable



T = TypeVar("T", bound = Hashable)
FromAllocator: TypeAlias = ChannelAllocator[FromChannel[T], T]
class _Base(FromAllocator[T]): pass



_from_alloc_dict: AllocDict[FromAllocator] = {
    DFT: _Base, 
    DRC: _Base
}