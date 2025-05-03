from .arrive import ArriveAllocator, _arrive_alloc_dict
from .base import ChannelAllocator
from .frm import FromAllocator, _from_alloc_dict
from .gap import GapAllocator, _gap_alloc_dict
from .meta import MetaAllocator, _meta_alloc_dict
from .setout import SetoutAllocator, _setout_alloc_dict
from .to import ToAllocator, _to_alloc_dict
from .trunk import TrunkAllocator, _trunk_alloc_dict
from typing import TypeVar



CT = TypeVar("CT", bound = ChannelAllocator)
class AllocPolicy: 
    def __init__(self, tag: str):
        self.tag = tag
    
    def __getitem__(self, channel: type[CT]) -> type[CT]: 
        if channel == ArriveAllocator: 
            return _arrive_alloc_dict[self.tag]
        elif channel == FromAllocator: 
            return _from_alloc_dict[self.tag]
        elif channel == GapAllocator: 
            return _gap_alloc_dict[self.tag]
        elif channel == MetaAllocator: 
            return _meta_alloc_dict[self.tag]
        elif channel == SetoutAllocator: 
            return _setout_alloc_dict[self.tag]
        elif channel == ToAllocator: 
            return _to_alloc_dict[self.tag]
        elif channel == TrunkAllocator: 
            return _trunk_alloc_dict[self.tag]
        else: 
            assert False, "Invalid channel type"