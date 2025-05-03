from ..channel import GapChannel
from .base import ChannelAllocator, ConMap
from typing import Hashable, TypeVar



T = TypeVar("T", bound = Hashable)
class GapAllocator(ChannelAllocator[GapChannel, T]): 
    def __init__(self, channel: GapChannel[T], con_map: ConMap[T]):
        ChannelAllocator.__init__(self, channel, con_map)
    def _alloc(self) -> list[T]:
        return ChannelAllocator._alloc(self)