from ..channel import TrunkChannel
from .base import ChannelAllocator, ConMap
from typing import Hashable, TypeVar



T = TypeVar("T", bound = Hashable)
class TrunkAllocator(ChannelAllocator[TrunkChannel, T]): 
    def __init__(self, channel: TrunkChannel[T], con_map: ConMap[T]):
        ChannelAllocator.__init__(self, channel, con_map)
    def _alloc(self) -> list[T]:
        return ChannelAllocator._alloc(self)