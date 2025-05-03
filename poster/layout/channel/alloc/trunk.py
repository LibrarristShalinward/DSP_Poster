from ..channel import TrunkChannel
from .base import ChannelAllocator
from typing import Hashable, TypeAlias, TypeVar



T = TypeVar("T", bound = Hashable)
TrunkAllocator: TypeAlias = ChannelAllocator[TrunkChannel[T], T]
class _Base(TrunkAllocator[T]): pass



_trunk_alloc_dict: dict[str, type[TrunkAllocator]] = {
    "": _Base, 
    "direct": _Base
}