from dsp import Item, Recipe
from poster import Icon
from poster.layout.channel.utils import func2getitem
from typing import Callable, Hashable, Iterable, Literal, TypeAlias, TypeVar
import colorsys
import numpy as np



Color: TypeAlias = np.ndarray[tuple[Literal[3]], np.dtype[np.float_]]
Colors: TypeAlias = np.ndarray[tuple[int, Literal[3]], np.dtype[np.float_]]
ColorMapping: TypeAlias = Callable[[Color], Color]
ColorsMapping: TypeAlias = Callable[[Colors], Colors]



K = TypeVar("K", bound = Hashable)
@func2getitem
def colordict_mapper(
            mappings: ColorsMapping | Iterable[ColorsMapping]
        ) -> Callable[[dict[K, Color]], dict[K, Color]]: 
    if callable(mappings): 
        mappings = [mappings]
    def mapper(cd: dict[K, Color]) -> dict[K, Color]: 
        ks, cs = zip(*cd.items())
        cs_: Colors = np.stack(cs, 0)
        for m in mappings: 
            cs_ = m(cs_)
        return {k: c for k, c in zip(ks, cs_)}
    return mapper

def extend_cmapping(m: ColorMapping) -> Callable[[Colors], Colors]: 
    def colors_mapping(cs: Colors) -> Colors: 
        return np.stack(
            [
                m(c) for c in cs
            ], 0
        )
    return colors_mapping

@extend_cmapping
def rgb2hsv(rgb: Color) -> Color: 
    return np.array(colorsys.rgb_to_hsv(*rgb))

@extend_cmapping
def hsv2rgb(hsv: Color) -> Color: 
    return np.array(colorsys.hsv_to_rgb(*hsv))

@func2getitem
def in_hsv(mappings: Iterable[ColorsMapping]) -> tuple[ColorsMapping]: 
    return rgb2hsv, *mappings, hsv2rgb

@func2getitem
def hsv_equalization(random_weight: tuple[float, ...]) -> ColorsMapping: 
    rw = np.array(random_weight)
    def mapping(c: Colors) -> Colors: 
        return np.argsort(
            np.argsort(
                c + np.random.rand(*c.shape) * rw, 
                0
            ), 0
        ) / len(c)
    return mapping

@func2getitem
def hsv_linear(rg: tuple[float, ...]): 
    sb, st, vb, vt = rg
    k = np.array([[1., st - sb, vt - vb]])
    b = np.array([[0., sb, vb]])
    def mapping(c: Colors) -> Colors: 
        return k * c + b
    return mapping



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

def icon_color_aranger(
            icons: dict[Item, Icon], 
            *transformers: ColorsMapping, 
            hsv: bool = True
        ): 
    @get_rcp_colors
    def getter(item: Item) -> Color: 
        return icons[item].main_color / 255.
    if hsv: transformers = in_hsv[transformers]
    mapper = colordict_mapper[transformers]
    def caller(recipes: Iterable[Recipe]): 
        return mapper(getter(recipes))
    return caller