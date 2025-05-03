from .items import Icon, Canvas, Connection
from .layout import BaseLayoutManager, RolCol
from .layout.channel.utils import func2getitem
from dsp import Item, Recipe, dsp_recipes
from matplotlib import pyplot as plt
from typing import Any, Callable


class Poster: 
    def __init__(self, 
                icon_pos: dict[Item, RolCol], 
                manager: BaseLayoutManager[Recipe], 
                targets: list[Item] = [], 
            ):
        self.icon_pos = icon_pos
        self.manager = manager
        self.icons = {
            it: Icon(
                it.icon
            ) for it in icon_pos.keys()
        }
        self.connections = {
            Connection(*manager.connect[(s, a), rcp]): rcp
            for rcp, (setouts, arrives) in manager.con_sets.items()
            for s in setouts
            for a in arrives
        }
        self.canvases = [
            (
                Canvas(
                    *self.manager.layout.canvas[
                        self.region(tg)
                    ]
                ), tg
            ) for tg in targets
        ]
    
    @property
    def items(self): 
        return set(self.icon_pos.keys())
    
    @property
    def recipes(self): 
        return set(self.manager.con_sets.keys())
    
    def depends(self, item: Item): 
        """返回指定物品的依赖树

        Args:
            item (Item): 被检索物品
        """
        from_tos = [
            (
                set(rcp.items.keys()), 
                set(rcp.results.keys())
            ) for rcp in self.manager.con_sets
        ]
        if item not in self.icon_pos: 
            return set()
        depends = set()
        tmp, tmp_ = set(), {item}
        while tmp_: 
            depends |= tmp
            tmp = tmp_ | tmp_
            tmp_.clear()
            for f, t in from_tos: 
                if t & tmp: 
                    tmp_ |= f - depends
        return depends | tmp
    
    def region(self, item: Item): 
        """返回指定物品依赖树的范围

        Args:
            item (Item): 被检索物品
        """
        r, c = tuple(
            zip(
                *[
                    self.icon_pos[it] for it in self.depends(item)
                ]
            )
        )
        return min(r), max(r), min(c), max(c)
    
    def draw(self, 
                rcp_colors: dict[Recipe, Any]
            ): 
        fs = self.manager.layout.fig_size
        plt.figure(figsize = fs)
        for item, icon in self.icons.items(): 
            icon.draw(
                *self.manager.icon[self.icon_pos[item]], 
                self.manager.layout.cfg.icon_size
            )
        for con, rcp in self.connections.items(): 
            con.draw(
                2., 
                rcp_colors[rcp], 
                -rcp.id / 10000. - 5
            )
        ncv = len(self.canvases)
        for i, (cv, tg) in enumerate(self.canvases): 
            cv.draw(
                self.icons[tg].bg_color / 255., 
                - (i + .5) / ncv - 10.
            )
        plt.axis([0, fs[0], -fs[1], 0])
        plt.axis("off")
    
    def grid_y(self): 
        """横向栅格辅助线"""
        layout = self.manager.layout
        fs = layout.fig_size
        for i in range(layout.nrow): 
            clu = layout.con_pos_y[i]
            for j in range(layout.inner_con_cap[1]): 
                plt.plot([0, fs[0]], [clu[j], clu[j]], color = "black", linewidth=0.5)



__default_rcp_filter: Callable[[Recipe], bool] = lambda rcp: len(rcp.items) and set(rcp.items.keys()) != set(rcp.results.keys()) and not (rcp.id >= 1000 and rcp.id < 3000)
@func2getitem
def PosterConstructor(ManagerClass: type[BaseLayoutManager]): 
    def manager_initer(
                rcp_filter: Callable[[Recipe], bool] = __default_rcp_filter, 
                **manager_kwargs
            ): 
        def poster_initer(
                icon_pos: dict[Icon, RolCol], 
                **poster_kwargs
            ): 
            recipes = {
                rcp for rcp in dsp_recipes.values() if rcp.all_objs_satisfies(
                    lambda item: item in icon_pos.keys()
                ) and rcp_filter(rcp)
            }
            con_sets = {
                rcp: (
                    set(icon_pos[iidx] for iidx in rcp.items.keys()), 
                    set(icon_pos[iidx] for iidx in rcp.results.keys())
                ) for rcp in recipes
            }
            return Poster(
                icon_pos, 
                ManagerClass(
                    con_sets, 
                    **manager_kwargs
                ), 
                **poster_kwargs
            )
        return poster_initer
    return manager_initer
