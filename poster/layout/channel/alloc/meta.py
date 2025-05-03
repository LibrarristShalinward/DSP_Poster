from ..channel import MetaChannel
from .base import ChannelAllocator
from typing import Hashable, TypeAlias, TypeVar



T = TypeVar("T", bound = Hashable)
MetaAllocator: TypeAlias = ChannelAllocator[MetaChannel[T], T]
class _Base(MetaAllocator[T]): pass



_meta_alloc_dict: dict[str, type[MetaAllocator]] = {
    "": _Base, 
    "direct": _Base
}