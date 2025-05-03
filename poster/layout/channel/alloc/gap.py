from ..channel import GapChannel
from .base import ChannelAllocator
from typing import Hashable, TypeAlias, TypeVar



T = TypeVar("T", bound = Hashable)
GapAllocator: TypeAlias = ChannelAllocator[GapChannel[T], T]
class _Base(GapAllocator[T]): pass



_gap_alloc_dict: dict[str, type[GapAllocator]] = {
    "": _Base, 
    "direct": _Base
}