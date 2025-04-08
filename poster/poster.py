import os, sys
sys.path.append(
    os.path.join(
        os.path.abspath(__file__), 
        "../"
    )
)

from .items import Icon, Connection
from .layout import BaseLayoutManager, RolCol
from dsp import Recipe
from matplotlib import pyplot as plt
from typing import Any


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