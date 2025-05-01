from .alloc import (
    ArriveAllocator, 
    ConMap, 
    FromAllocator, 
    GapAllocator, 
    MetaAllocator, 
    RolCol, 
    SetoutAllocator, 
    ToAllocator, 
    TrunkAllocator, 
)
from .collect import ChannelCollector
from .utils import method2geitem
from typing import Generic, Hashable, TypeAlias, TypeVar



T_ = TypeVar("T_", bound = Hashable)
Con: TypeAlias = tuple[tuple[RolCol, RolCol], T_]

T = TypeVar("T", bound = Hashable)
class ChannelManager(Generic[T]): 
    setouts: list[list[SetoutAllocator[T]]]
    froms: list[FromAllocator[T]]
    trunk: TrunkAllocator[T]
    gaps: list[list[GapAllocator[T]]]
    meta: MetaAllocator[T]
    tos: list[ToAllocator[T]]
    arrives: list[list[ArriveAllocator[T]]]
    def __init__(self, collector: ChannelCollector, con_map: ConMap[T]): 
        self.setouts = [
            [
                SetoutAllocator(
                    c, con_map
                ) for c in cs
            ] for cs in collector.setouts
        ]
        self.froms = [
            FromAllocator(c, con_map) for c in collector.froms
        ]
        self.trunk = TrunkAllocator(collector.trunk, con_map)
        self.gaps = [
            [
                GapAllocator(
                    c, con_map
                ) for c in cs
            ] for cs in collector.gaps
        ]
        self.meta = MetaAllocator(collector.meta, con_map)
        self.tos = [
            ToAllocator(c, con_map) for c in collector.tos
        ]
        self.arrives = [
            [
                ArriveAllocator(
                    c, con_map
                ) for c in cs
            ] for cs in collector.arrives
        ]
    
    @property
    @method2geitem
    def setout_path(self, con: Con[T]) -> RolCol: 
        ((r, c), _), it = con
        s = self.setouts[r][c]
        return s[it], len(s.channel)
    
    @property
    @method2geitem
    def from_path(self, con: Con[T]) -> int: 
        ((r, _), _), it = con
        return self.froms[r][it]

    @property
    @method2geitem
    def cross_path(self, con: Con[T]) -> int: 
        ((rs, cs), (ra, _)), it = con
        if rs > ra: 
            return self.meta[it]
        elif rs == ra: 
            return self.gaps[rs][cs][it]
        elif rs == ra - 1: 
            raise IndexError("相差一行时无需cross")
        else: 
            return self.trunk[it]
    
    @property
    @method2geitem
    def to_path(self, con: Con[T]) -> int: 
        (_, (r, _)), it = con
        return self.tos[r][it]

    @property
    @method2geitem
    def arrive_path(self, con: Con[T]) -> RolCol: 
        (_, (r, c)), it = con
        s = self.arrives[r][c]
        return s[it], len(s.channel)