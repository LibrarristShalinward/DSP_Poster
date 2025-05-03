from ..channel import Channel, RolCol
from abc import ABC, abstractmethod
from typing import Generic, Hashable, TypeAlias, TypeVar



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