from .channel import *
from .layout import Layout
from functools import cache
from typing import Generic, Hashable, TypeVar
import numpy as np



T = TypeVar("T", bound = Hashable)
class BaseLayoutManager(Generic[T]): 
    def __init__(self, 
                con_sets: dict[T, tuple[set[RolCol], set[RolCol]]], 
            ): 
        self.con_sets = con_sets
        self._icons: set[RolCol] = set()
        for sa in con_sets.values(): 
            self._icons = self._icons.union(*sa)
        self.collector = ChannelCollector(
            max(rc[0] for rc in self._icons) + 1, 
            max(rc[1] for rc in self._icons) + 1, 
            self.allow_direct
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
    
    def allow_direct(self, con: Con[T]) -> bool: 
        return False
    
    @property
    @method2geitem
    def icon(self, rc: RolCol) -> tuple[float, float]: 
        return self.layout.icon_pos[rc]
    
    @property
    @method2geitem
    def connect(self, con: Con[T]) -> tuple[list[float], list[float]]: 
        ((rs, cs), (ra, ca)), _ = con
        xs, ys = self.layout.con_start[rs, cs][self.cm.setout_path[con]]
        xa, ya = self.layout.con_end[ra, ca][self.cm.arrive_path[con]]
        yto = self.layout.con_pos_y[ra - 1][- self.cm.to_path[con] - 1]
        if rs == ra - 1 or self.allow_direct(con): 
            return [xs, xa], [ys, yto, ya]
        elif rs > ra: 
            xt = self.layout.con_pos_x[self.layout.ncol][self.cm.cross_path[con]]
        elif rs == ra: 
            xt = self.layout.con_pos_x[cs][self.cm.cross_path[con]]
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



class ExemptionLayoutManager(BaseLayoutManager[T]): 
    def __init__(self, 
                con_sets: dict[T, tuple[set[RolCol], set[RolCol]]], 
                exemptions: dict[T, set[int]]
            ):
        self.exem = exemptions
        BaseLayoutManager.__init__(self, con_sets)
    
    def allow_direct(self, con): 
        ((_, cs), _), t = con
        return t in self.exem.keys() and cs in self.exem[t]



class BlankDirectLayoutManager(BaseLayoutManager[T]): 
    def __init__(self, 
                con_sets: dict[T, tuple[set[RolCol], set[RolCol]]]
            ): 
        BaseLayoutManager.__init__(self, con_sets)
    
    @cache
    def check_occupation(self) -> None: 
        self._occuoation = np.zeros((self.collector.nrow, self.collector.ncol))
        self._occuoation[tuple(list(i) for i in zip(*self._icons))] = True
    
    def allow_direct(self, con): 
        self.check_occupation()
        ((rs, cs), (ra, _)), _ = con
        if ra <= rs: return False
        return not self._occuoation[rs + 1:ra, cs].any()