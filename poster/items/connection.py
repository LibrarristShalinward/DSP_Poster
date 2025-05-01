from .round import Round, EllipseRound
from matplotlib.colors import Colormap, Normalize
from typing import Iterable, Union
import matplotlib.pyplot as plt
import numpy as np



class Connection: 
    """各段依次与x和y坐标轴平行的折线段"""
    x: list[float]
    y: list[float]
    def __init__(self, x_coords: Iterable[float], y_coords: Iterable[float]):
        self.x = list(x_coords)
        self.y = list(y_coords)
        
        assert len(self.x) + 1 == len(self.y), "The number of x-coordinates must be one more than the number of y-coordinates"
    
    @property
    def nodes(self): 
        return np.array(
            [
                [self.x, self.y[:-1]], 
                [self.x, self.y[1:]], 
            ]
        ).transpose(2, 0, 1).reshape(-1, 2)
    
    def draw(self, 
            thickness: float, 
            color: Union[str, tuple, Colormap, Normalize, None] = None, 
            zorder: int = 0, 
            round: Round = EllipseRound()
        ) -> None: 
        plt.plot(
            *round(self.nodes).T, 
            linewidth = thickness, 
            color = color, 
            zorder = zorder, 
            solid_capstyle = "round", 
            solid_joinstyle = "round", 
        )