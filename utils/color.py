from dsp import Item, Recipe
from numpy.typing import NDArray
from poster import Icon
from typing import Callable, Iterable, Literal, TypeAlias
import numpy as np



Color: TypeAlias = np.ndarray[tuple[Literal[3]], np.dtype[np.float_]]
Colors: TypeAlias = np.ndarray[tuple[int, Literal[3]], np.dtype[np.float_]]

def get_rcp_colors(
            it_color_getter: Callable[[Item], Color]
        ): 
    def getter(
                recipes: Iterable[Recipe], 
                items_pooling: Callable[[Colors], Color] = lambda x: x.mean(0)
            ) -> dict[Recipe, Color]: 
        return {
            rcp: items_pooling(
                np.stack([
                    it_color_getter(it) for it in rcp.results.keys()
                ])
            ) for rcp in set(recipes)
        }
    return getter

def icon_color_aranger(icons: dict[Item, Icon]): 
    @get_rcp_colors
    def getter(item: Item) -> Color: 
        return icons[item].main_color / 255.
    return getter