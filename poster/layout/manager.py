from .channel import *
from .layout import Layout
from typing import Generic, Hashable, TypeVar



T = TypeVar("T", bound = Hashable)
class LayoutManager(Generic[T]): 
    def __init__(self, 
                con_sets: dict[T, tuple[set[RolCol], set[RolCol]]]
            ): 
        rcs: set[RolCol] = set()
        for sa in con_sets.values(): 
            rcs = rcs.union(*sa)
        self.collector = ChannelCollector(
            max(rc[0] for rc in rcs) + 1, 
            max(rc[1] for rc in rcs) + 1, 
        )
        for item, (setouts, arrives) in con_sets.items(): 
            self.collector.add_cons(setouts, arrives, item)
        
        self.layout = Layout(
            self.collector.nrow, 
            self.collector.ncol, 
            (self.collector.gap_cap, self.collector.inner_cap), 
            (self.collector.left_cap, self.collector.right_cap)
        )