from .round import Round, EllipseRound
from matplotlib.colors import Colormap, Normalize
from typing import Union
import matplotlib.pyplot as plt
import numpy as np



class Canvas: 
    def __init__(self, 
        xmin: float, 
        xmax: float, 
        ymin: float, 
        ymax: float, 
    ):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def nodes(self, r: float): 
        xs = [self.xmin - r, self.xmax + r, self.xmin - r]
        ys = [self.ymin - r, self.ymax + r, self.ymin - r, self.ymax + r]
        return np.array(
            [
                [xs, ys[:-1]], 
                [xs, ys[1:]], 
            ]
        ).transpose(2, 0, 1).reshape(-1, 2)
    
    def draw(self, 
            color: Union[str, tuple, Colormap, Normalize, None] = None, 
            zorder: int = 0, 
            round: Round = EllipseRound()
        ) -> None: 
        plt.fill(
            *round(self.nodes(round.r))[1:-1].T, 
            linewidth = 0., 
            color = color, 
            zorder = zorder, 
            capstyle = "round", 
            joinstyle = "round", 
        )