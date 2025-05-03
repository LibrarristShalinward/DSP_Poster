from ..channel import FromChannel
from .base import ChannelAllocator
from typing import Hashable, TypeAlias, TypeVar



T = TypeVar("T", bound = Hashable)
FromAllocator: TypeAlias = ChannelAllocator[FromChannel[T], T]
class _Base(FromAllocator[T]): pass



_from_alloc_dict: dict[str, type[FromAllocator]] = {
    "": _Base, 
    "direct": _Base
}