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

        self.cm = ChannelManager(
            self.collector, 
            con_sets
        )
    
    @property
    @method2geitem
    def icon(self, rc: RolCol) -> tuple[float, float]: 
        return self.layout.icon_pos[rc]
    
    @property
    @method2geitem
    def connect(self, con: Con[T]) -> tuple[list[float], list[float]]: 
        ((rs, cs), (ra, ca)), r = con
        xs, ys = self.layout.con_start[rs, cs][self.cm.setout_path[con]]
        xa, ya = self.layout.con_end[ra, ca][self.cm.arrive_path[con]]
        yto = self.layout.con_pos_y[ra - 1][- self.cm.to_path[con] - 1]
        if rs > ra: 
            xt = self.layout.con_pos_x[self.layout.ncol][self.cm.cross_path[con]]
        elif rs == ra: 
            xt = self.layout.con_pos_x[cs][self.cm.cross_path[con]]
        elif rs == ra - 1: 
            return [xs, xa], [ys, yto, ya]
        else: 
            xt = self.layout.con_pos_x[-1][self.cm.cross_path[con]]
        return (
            [xs, xt, xa], 
            [
                ys, 
                self.layout.con_pos_y[rs][self.cm.from_path[con]], 
                yto, 
                ya
            ]
        )