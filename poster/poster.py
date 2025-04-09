from .items import Icon, Connection
from .layout import BaseLayoutManager, RolCol
from .layout.channel.utils import func2getitem
from dsp import Recipe, dsp_recipes
from matplotlib import pyplot as plt
from typing import Any, Callable


class Poster: 
    def __init__(self, 
                icon_pos: dict[Icon, RolCol], 
                manager: BaseLayoutManager[Recipe]
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
    
    @property
    def items(self): 
        return set(self.icon_pos.keys())
    
    @property
    def recipes(self): 
        return set(self.manager.con_sets.keys())
    
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
                -rcp.id - 5
            )
        plt.axis([0, fs[0], -fs[1], 0])
        plt.axis("off")



__default_rcp_filter: Callable[[Recipe], bool] = lambda rcp: len(rcp.items) and set(rcp.items.keys()) != set(rcp.results.keys()) and not (rcp.id >= 1000 and rcp.id < 3000)
@func2getitem
def PosterConstructor(ManagerClass: type[BaseLayoutManager]): 
    def manager_initer(
                rcp_filter: Callable[[Recipe], bool] = __default_rcp_filter, 
                **manager_kwargs
            ): 
        def poster_initer(
                icon_pos: dict[Icon, RolCol], 
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
                )
            )
        return poster_initer
    return manager_initer
