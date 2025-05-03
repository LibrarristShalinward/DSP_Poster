from ..channel import MetaChannel
from .base import ChannelAllocator, ConMap
from typing import Hashable, TypeVar



T = TypeVar("T", bound = Hashable)
class MetaAllocator(ChannelAllocator[MetaChannel, T]): 
    def __init__(self, channel: MetaChannel[T], con_map: ConMap[T]):
        ChannelAllocator.__init__(self, channel, con_map)
    def _alloc(self) -> list[T]:
        return ChannelAllocator._alloc(self)