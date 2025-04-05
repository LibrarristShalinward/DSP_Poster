from typing import Generic, Hashable, TypeAlias, TypeVar
from abc import ABC, abstractmethod
from .channel import (
    ArriveChannel, 
    Channel, 
    FromChannel, 
    GapChannel, 
    MetaChannel, 
    RolCol, 
    SetoutChannel, 
    ToChannel, 
    TrunkChannel, 
)



T_ = TypeVar("T_", bound = Hashable)
ConMap: TypeAlias = dict[T_, tuple[set[RolCol], set[RolCol]]]

T = TypeVar("T", bound = Hashable)
CT = TypeVar("CT", bound = Channel[T])
class ChannelAllocator(ABC, Generic[CT, T]): 
    def __init__(self, channel: CT, con_map: ConMap[T]):
        self.channel = channel
        self.con_map = con_map
        self.order = {
            it: i for i, it in enumerate(self._alloc())
        }
    
    @abstractmethod
    def _alloc(self) -> list[T]: 
        return list(self.channel.cons)
    
    def __getitem__(self, idx: T) -> int: 
        return self.order[idx]

class ArriveAllocator(ChannelAllocator[ArriveChannel, T]): 
    def __init__(self, channel: ArriveChannel[T], con_map: ConMap[T]):
        ChannelAllocator.__init__(self, channel, con_map)
    def _alloc(self) -> list[T]:
        return ChannelAllocator._alloc(self)

class FromAllocator(ChannelAllocator[FromChannel, T]): 
    def __init__(self, channel: FromChannel[T], con_map: ConMap[T]):
        ChannelAllocator.__init__(self, channel, con_map)
    def _alloc(self) -> list[T]:
        return ChannelAllocator._alloc(self)

class GapAllocator(ChannelAllocator[GapChannel, T]): 
    def __init__(self, channel: GapChannel[T], con_map: ConMap[T]):
        ChannelAllocator.__init__(self, channel, con_map)
    def _alloc(self) -> list[T]:
        return ChannelAllocator._alloc(self)

class MetaAllocator(ChannelAllocator[MetaChannel, T]): 
    def __init__(self, channel: MetaChannel[T], con_map: ConMap[T]):
        ChannelAllocator.__init__(self, channel, con_map)
    def _alloc(self) -> list[T]:
        return ChannelAllocator._alloc(self)

class SetoutAllocator(ChannelAllocator[SetoutChannel, T]): 
    def __init__(self, channel: SetoutChannel[T], con_map: ConMap[T]):
        ChannelAllocator.__init__(self, channel, con_map)
    def _alloc(self) -> list[T]:
        return ChannelAllocator._alloc(self)

class ToAllocator(ChannelAllocator[ToChannel, T]): 
    def __init__(self, channel: ToChannel[T], con_map: ConMap[T]):
        ChannelAllocator.__init__(self, channel, con_map)
    def _alloc(self) -> list[T]:
        return ChannelAllocator._alloc(self)

class TrunkAllocator(ChannelAllocator[TrunkChannel, T]): 
    def __init__(self, channel: TrunkChannel[T], con_map: ConMap[T]):
        ChannelAllocator.__init__(self, channel, con_map)
    def _alloc(self) -> list[T]:
        return ChannelAllocator._alloc(self)