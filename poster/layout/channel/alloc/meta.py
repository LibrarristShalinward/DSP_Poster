from ..channel import MetaChannel
from .type import *
from typing import Hashable



T = TypeVar("T", bound = Hashable)
MetaAllocator: TypeAlias = ChannelAllocator[MetaChannel[T], T]
class _Base(MetaAllocator[T]): pass



_meta_alloc_dict: AllocDict[MetaAllocator] = {
    DFT: _Base, 
    DRC: _Base
}