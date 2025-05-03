from .base import ChannelAllocator
from enum import Enum
from typing import TypeAlias, TypeVar



class AllocMode(Enum): 
    """放置策略"""
    DFT = 0
    """默认策略"""
    DRC = 1
    """直连策略"""
DFT = AllocMode.DFT
DRC = AllocMode.DRC



AT = TypeVar("CT", bound = ChannelAllocator)
AllocDict: TypeAlias = dict[str, type[AT]]